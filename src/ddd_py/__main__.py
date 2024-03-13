import ddd_py
import sys

from ddd_py.app_ctx.domain.post import post
from ddd_py.app_ctx.domain.user import user

print(post.Post(post.Id(1), user.Id(2), post.Content("just make sure to run away.")))

sys.exit(ddd_py.main())