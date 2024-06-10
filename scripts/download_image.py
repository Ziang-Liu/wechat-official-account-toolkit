import asyncio
import csv
import os
import re
from typing import List, Any
from urllib.parse import urlparse, parse_qs

import aiofiles
from fake_useragent import UserAgent
from httpx import AsyncClient, Response, URL

from ._logger import logger


class ImageDownloader:
    def __init__(
            self,
            total_tasks: int = -1,
            start_from: int = 0,
            filter_small_image: bool = False,
            filter_image_list: bool = False,
            filter_gif: bool = False,
            thread: int = 1,
            base_url: str = "mmbiz.qpic.cn"
    ) -> None:
        """
        Read results.csv and get images from collected urls
        :param total_tasks: how many urls used, if specified,
        tasks will be limited to this number in descending order
        :param start_from: which url to start downloading from
        :param filter_small_image: filter photos smaller than 100KB
        :param filter_image_list: filter image_list which length is less than 5
        :param filter_gif: do you need gif? It concerns to you
        :param thread: how many download threads to use in a single task queue
        """
        if not os.path.exists('result.csv'):
            raise FileNotFoundError("No result.csv found.")

        self._base_url = base_url
        self._headers = {'User-Agent': UserAgent().random}
        self._thread = thread
        self._start_from = start_from
        self._filter_photo_size = filter_small_image
        self._filter_photo_list = filter_image_list
        self._need_gif = filter_gif
        self._download_limit = total_tasks
        self._working_dir = os.getcwd()
        os.makedirs("images", exist_ok = True)

        self._tasks = []
        with open("result.csv", mode = "r", encoding = "utf-8") as f:
            reader = csv.reader(f)
            [self._tasks.append({'title': row[0], 'url': row[2]}) for row in reader]

        self._tasks.pop(0)

    async def _get_image_urls(self, url: URL) -> list[list[Any] | None]:
        async with AsyncClient(headers = self._headers, follow_redirects = True) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
                raise ConnectionError(f"Status code: {resp.status_code}") if resp.status_code == 200 else None

            return re.compile(r'src="([^"]*mmbiz\.qpic\.cn[^"]*)"').findall(resp.text)

    async def _download_image(self, img_list: List) -> None:
        async def image_handler(client: AsyncClient, url, image_path):
            async def write_image(response: Response, target_path) -> None:
                if os.path.exists(target_path) and os.path.getsize(target_path) != 0:
                    return

                content_length = response.headers.get('Content-Length')
                if content_length and int(content_length) < 100 * 1024 and self._filter_photo_size:
                    return

                async with aiofiles.open(target_path, 'wb') as f:
                    await f.write(await response.aread())

            try:
                resp = await client.get(url, headers = self._headers)
                await write_image(resp, image_path) if resp.status_code == 200 else None
            except Exception:
                raise Exception(f"Failed to download image {url}")

        async def create_queue():
            async def worker(queue: asyncio.Queue, client: AsyncClient):
                while True:
                    img_num, url = await queue.get()
                    if url is None:
                        break

                    ext_type = parse_qs(urlparse(url).query)['wx_fmt'][0]
                    await image_handler(client, url, f'{img_num}.{ext_type}') \
                        if ext_type != 'gif' and not self._need_gif else None
                    queue.task_done()

            fixed_length_rank = asyncio.Queue()
            [fixed_length_rank.put_nowait((i, img_url)) for i, img_url in enumerate(img_list)]

            async with AsyncClient(timeout = 10, follow_redirects = True, headers = self._headers) as c:
                tasks = []
                [tasks.append(asyncio.create_task(worker(fixed_length_rank, c))) for _ in range(self._thread)]
                await fixed_length_rank.join()
                [fixed_length_rank.put_nowait((None, None)) for _ in range(self._thread)]
                await asyncio.gather(*tasks)

        await create_queue()

    async def start(self):
        logger.info("Start downloading images...")
        logger.info("If you encounter error message, record the task number and restart from there")

        for i, task in enumerate(self._tasks):
            if i < self._start_from:
                continue

            url_list = await self._get_image_urls(URL(url = task["url"]))
            if len(url_list) <= 5 and self._filter_photo_list:
                continue

            _title = re.sub(
                r'[*|? /:]',
                lambda x: {'*': '٭', '|': '丨', '?': '？', ' ': '', '/': 'ǀ', ':': '∶'}[x.group()],
                task["title"]
            )
            target_path = os.path.join("images", _title)
            os.makedirs(target_path, exist_ok = True)
            os.chdir(target_path)

            try:
                await self._download_image(url_list)
                logger.info(f"Task {i}, {_title} finished")
            except Exception as exc:
                logger.warning(f"Task {i}, {_title} failed: {exc}")
                logger.info("Retry in 10 seconds")
                await asyncio.sleep(10)
                try:
                    await self._download_image(url_list)
                except Exception as retry_exc:
                    logger.error(f"Retry failed, error {retry_exc}")
                    raise
            finally:
                os.chdir(self._working_dir)
                self._download_limit -= 1

            if self._download_limit == 0:
                logger.info("Task accomplished")
                return
