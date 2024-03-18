class DomainError(Exception): ...


class RepositoryError(Exception): ...


# TODO:
# 本来はもう少し細かい粒度で定義するのがベター。
# ケース独自のエラーペイロードを明確に運搬できるようにするべき。
# 例えば RepositoryError は GetError/SaveError/DeleteError などに分割し、
# エラーの付加情報として、ストア上に存在しない識別子が何であったかなどの情報を持たせる。
