# 如果你下载了很多二次元图片，那么这个适合你用）

import asyncio, os
from PicImageSearch import Ascii2D, Network
from PicImageSearch.model import Ascii2DResponse
from loguru import logger
from fake_useragent import UserAgent

logger.add("err.log", rotation="10 MB", level="ERROR")

def get_default_folder():
    current_directory = os.path.dirname(__file__)
    new_folder_path = os.path.join(current_directory, "download")
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path

def show_result(resp: Ascii2DResponse=True) -> None:
    logger.info(resp.url)  # 搜索结果链接
    selected = next((i for i in resp.raw if i.title or i.url_list), resp.raw[0])
    logger.info(selected.title)
    logger.info(selected.author)
    logger.info(selected.url)
    logger.info(selected.detail)
    logger.info("-" * 100)
    return selected.author, selected.author_url, selected.url, selected.hash, selected.detail
    
async def main() -> None:
    with open('image_details.csv', mode='w', encoding='utf-8') as file:
        file.write('path,author,author_url,url,hash,detail\n')
    bovw = False # 不使用特征检索
    verify_ssl = True # 验证 ssl 证书
    user_agent = UserAgent()
    ran_user_agent = user_agent.random
    headers = {'User-Agent': ran_user_agent}
    async with Network(headers=headers, verify_ssl=verify_ssl) as client:
        for folder_path, _, files in os.walk(get_default_folder()):
            for file in files:
                try:
                    if ".gif" in file:
                        logger.info(f"Skip: {file}")
                        continue
                    file_path = os.path.join(folder_path, file)
                    relative_path = os.path.relpath(file_path, get_default_folder())
                    ascii2d = Ascii2D(client=client, bovw=bovw)
                    resp = await ascii2d.search(file=file_path)
                    author, author_url, url, hash, detail = show_result(resp)
                    data = '"{}","{}","{}","{}","{}","{}"'.format(relative_path, author, author_url, url, hash, detail)
                    with open("image_details.csv", mode="a", newline='', encoding="utf-8") as file:
                        file.write(data+'\n')
                except Exception as e:
                    logger.error(f"{file_path} is skipped due to network error!,{e}")
                    await asyncio.sleep(10)
                    continue

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
