import asyncio
import json
from random import randint
from urllib.parse import urlparse, parse_qs

from fake_useragent import UserAgent
from httpx import AsyncClient


class WechatOfficialAccountFetcher:
    def __init__(self, cookie: str, appmsgpublish_url: str) -> None:
        self.base_url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
        self.headers = {'Cookie': cookie, 'User-Agent': UserAgent().random}
        self.params = parse_qs(urlparse(appmsgpublish_url).query)

        with open("result.csv", "w", encoding = "utf-8") as f:
            f.write("title,cover,link,author_name\n")

    async def get_published_articles(self) -> None:
        async with AsyncClient(headers = self.headers, verify = False, timeout = 30) as client:
            page = 0
            while True:
                resp = await client.get(params = self.params, url = self.base_url)
                result = resp.json()
                if result['base_resp']['ret'] == 200013:
                    print("触发反爬限制，等半个小时再继续")
                    await asyncio.sleep(1800)
                    continue
                elif "publish_page" in result:
                    publish_list = json.loads(result["publish_page"])["publish_list"]
                    for pl in publish_list:
                        appmsgex = json.loads(pl["publish_info"])["appmsgex"]
                        for ame in appmsgex:
                            with open("result.csv", 'a', encoding = 'utf-8') as f:
                                f.write(f"{ame['title']},{ame['cover']},{ame['link']},{ame['author_name']}\n")

                    page += 1
                    self.params['begin'] = [str(page * 5)]
                    print(f"目前爬取的页数: {page}, 文章数量: {page * 5}")
                    await asyncio.sleep(randint(30, 60))
                else:
                    break
