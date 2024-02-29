import ddd_py
import sys

from ddd_py.domain.post import post

print(post.Post(post.ID(1), post.Content("ほああああああああん")))

sys.exit(ddd_py.main())