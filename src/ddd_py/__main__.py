import ddd_py
import sys

from ddd_py.domain.post import post
from ddd_py.domain.user import user

print(post.Post(post.Id(1), user.Id(2), post.Content("just make sure to run away.")))

sys.exit(ddd_py.main())