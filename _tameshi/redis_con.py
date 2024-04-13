import asyncio
import json

import httpx
import redis


async def tameshi():
    key = "google_discovery_doc"

    # decode_responses=True にするとデータ取得時 bytes ではない基底型にデコードしてくれるようになる
    r = redis.Redis(host="localhost", port=6379, db=0)

    doc = httpx.get("https://accounts.google.com/.well-known/openid-configuration")
    print(doc.status_code)

    r.set(key, doc.content)
    ll = r.get(key)
    if isinstance(ll, bytes):
        # res = ast.literal_eval(ll.decode("utf-8"))
        res = json.loads(ll.decode("utf-8"))
        print(res)


t = asyncio.run(tameshi())
