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
        self._active_page = start_page
        self._target_page = end_page
        self._fetched_pages = 0

        with open("result.csv", "w", encoding = "utf-8") as f:
            f.write("title,cover,link,author_name\n")

    async def get_published_articles(self) -> None:
        async with AsyncClient(headers = self._headers, verify = False, timeout = 10) as client:
            while self._active_page != self._target_page:
                self._params['begin'] = [str(self._active_page * 5)]
                resp = (await client.get(params = self._params, url = self._base_url)).json()
                if resp['base_resp']['ret'] == 200013:
                    logger.warning("触发反爬限制，暂停半小时")
                    await asyncio.sleep(1800)
                    await self.get_published_articles()
                elif "publish_page" not in resp:
                    logger.info("获取完毕")
                    return

                for i in json.loads(resp["publish_page"])["publish_list"]:
                    with open("result.csv", 'a', encoding = 'utf-8') as f:
                        for j in json.loads(i["publish_info"])["appmsgex"]:
                            f.write(f"{j['title']},{j['cover']},{j['link']},{j['author_name']}\n")
                            self._fetched_pages += 1

                    self._active_page += 1
                    logger.info(f"第 {self._active_page} 页, 总共 {self._fetched_pages} 篇文章")
                    await asyncio.sleep(randint(30, 60))
