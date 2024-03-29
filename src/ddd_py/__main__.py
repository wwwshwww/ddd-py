import sys
import uuid
from datetime import datetime

import ulid

import ddd_py
from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.user import user

print(
    post.Post(
        post.Id(ulid.new().uuid),
        user.Id(uuid.uuid4()),
        post.Content("just make sure to run away."),
        datetime.now(),
    )
)

sys.exit(ddd_py.main())
