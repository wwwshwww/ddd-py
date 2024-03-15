from datetime import datetime

from ddd_py.auth_ctx.domain.auth_session import auth_session, auth_session_finder
from ddd_py.auth_ctx.domain.user import user, user_finder
from ddd_py.auth_ctx.domain.user_session import user_session, user_session_finder

from .dto import LoginInput, LoginOutput, StartInput, StartOutput
from .error import DomainError, PortError, RepositoryError, UnauthorizedError
from .port import Port


class Usecase:
    def __init__(
        self,
        up: Port,
        asr: auth_session.Repository,
        asf: auth_session_finder.Finder,
        usr: user_session.Repository,
        usf: user_session_finder.Finder,
        ur: user.Repository,
        uf: user_finder.Finder,
    ) -> None:
        self.usecase_port = up
        self.auth_session_repository = asr
        self.auth_session_finder = asf
        self.user_session_repository = usr
        self.user_session_finder = usf
        self.user_repository = ur
        self.user_finder = uf

    def start(self, si: StartInput) -> StartOutput:
        try:
            aus = auth_session.generate_auth_session(
                auth_session.ClientState(si.client_state),
                datetime.now(),
            )
            self.auth_session_repository.bulk_save([aus])

        except auth_session.DomainError as e:
            raise DomainError() from e
        except auth_session.RepositoryError as e:
            raise RepositoryError() from e

        return StartOutput(aus.id)

    def login(self, li: LoginInput) -> LoginOutput:
        now = datetime.now()

        try:
            aus_ids = self.auth_session_finder.find(
                auth_session_finder.FilteringOptions(id_in=[li.auth_session_id])
            )
            if len(aus_ids) == 0:
                raise UnauthorizedError("auth session is invalid")

            aus = self.auth_session_repository.bulk_get(aus_ids)[0]
            if aus.is_expired(now):
                raise UnauthorizedError("auth session is expired")

            idp_resp = self.usecase_port.code2token(li.code)

            # TODO: verify id token
            found_user_ids = self.user_finder.find(
                user_finder.FilteringOptions(
                    provider_subject_google=idp_resp.sub,
                )
            )

            # user が存在しなければ新規登録
            u: user.User
            if len(found_user_ids) == 0:
                ui = self.user_repository.new_ids(1)[0]
                ugp = user.GoogleProfile(user.ProviderSubject(idp_resp.sub))
                u = user.User(ui, ugp)
                self.user_repository.bulk_save([u])
            else:
                u = self.user_repository.bulk_get(found_user_ids)[0]

            us, us_token = user_session.generate(u.id, now)
            self.user_session_repository.bulk_save([us])

        except auth_session.DomainError as e:
            raise DomainError() from e
        except auth_session.RepositoryError as e:
            raise RepositoryError() from e
        except PortError as e:
            raise e

        return LoginOutput(ui.value, us.id.value, us_token.value)
