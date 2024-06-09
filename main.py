import asyncio
import os

from scripts import WechatOfficialAccountFetcher, ImageDownloader


async def download_images_from_result():
    try:
        os.chdir(f"{os.getcwd()}/workdir")
    except Exception:
        raise FileNotFoundError

    await ImageDownloader(
        download_thread = 4,
        start_from_which_link = 30,
        filter_small_photo = True,
        filter_small_image_list = True,
        need_gif = False
    ).start()


async def get_official_account_publish():
    url = input("粘贴你在控制台找到的含有'appmsgpublish'json的链接:\n")
    cookie = input("粘贴你从这个json得到的cookie:\n")
    print("如果你觉得获取得差不多了直接ctrl+c中断运行即可")
    os.makedirs(f"{os.getcwd()}/workdir", exist_ok = True)
    os.chdir(f"{os.getcwd()}/workdir")
    await WechatOfficialAccountFetcher(cookie, url).get_published_articles()


if __name__ == '__main__':
    # 两个选一个 c:
    # asyncio.run(get_official_account_publish())
    asyncio.run(download_images_from_result())
    pass
