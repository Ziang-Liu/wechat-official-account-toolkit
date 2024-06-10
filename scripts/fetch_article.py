import asyncio
import json
from random import randint
from urllib.parse import urlparse, parse_qs

from fake_useragent import UserAgent
from httpx import AsyncClient

from ._logger import logger


class WechatOfficialAccountFetcher:
    def __init__(
            self,
            cookie: str,
            url: str,
            start_page: int = 0,
            end_page: int = -1
    ) -> None:
        self._base_url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
        self._headers = {'Cookie': cookie, 'User-Agent': UserAgent().random}
        self._params = parse_qs(urlparse(url).query)
        self._page = start_page
        self._end_page = end_page

        with open("result.csv", "w", encoding = "utf-8") as f:
            f.write("title,cover,link,author_name\n")

    async def get_published_articles(self) -> None:
        async with AsyncClient(headers = self._headers, verify = False, timeout = 10) as client:
            while self._page != self._end_page:
                self._params['begin'] = [str(self._page * 5)]
                result = (await client.get(params = self._params, url = self._base_url)).json()
                if result['base_resp']['ret'] == 200013:
                    logger.warning("触发反爬限制，等半个小时再继续")
                    await asyncio.sleep(1800)
                    await self.get_published_articles()

                if "publish_page" in result:
                    publish_list = json.loads(result["publish_page"])["publish_list"]
                    for pl in publish_list:
                        appmsgex = json.loads(pl["publish_info"])["appmsgex"]
                        for ame in appmsgex:
                            with open("result.csv", 'a', encoding = 'utf-8') as f:
                                f.write(f"{ame['title']},{ame['cover']},{ame['link']},{ame['author_name']}\n")

                    self._page += 1
                    logger.info(f"目前爬取的页: {self._page}, 爬取的文章数量: {self._page * 5}")
                    await asyncio.sleep(randint(30, 60))
