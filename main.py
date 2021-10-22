# %%
import json
from urllib.parse import urlparse

from TikTokApi import TikTokApi

api = TikTokApi.get_instance()
# %%
with open('url.txt', 'r') as f:
    user_url = f.read().split('\n')
    user_id = list(map(lambda _: urlparse(_).path[2:], user_url))

search_results = []
for i in user_id:
    data = api.by_username(username=i, count=9999999)
    for x in data:
        search_results.append(x)

with open("data.json", "w") as outfile:
    json.dump(search_results, outfile)