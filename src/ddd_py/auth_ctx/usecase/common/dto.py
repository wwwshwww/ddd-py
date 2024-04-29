from dataclasses import dataclass

import jwt

# 将来的にスケールさせたくなったとき、セッション管理機構をJWTベースに切り替える
ServiceAccessToken = jwt.PyJWT()
