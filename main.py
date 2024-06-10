import asyncio
import os

from scripts import WechatOfficialAccountFetcher, ImageDownloader


async def download_images_from_result():
    try:
        os.chdir(f"{os.getcwd()}/workdir")
    except Exception:
        raise FileNotFoundError("没有找到 result.csv")

    filter_small_image = input("\n是否过滤小图片(<=100KB)\n"
                               "1代表True, 0代表False:")
    filter_image_list = input("是否过滤掉图片少于五张的公众号文章\n"
                              "1代表True, 0代表False:")
    filter_gif = input("是否需要 gif\n"
                       "1代表True, 0代表False:")
    start_from = input("需要从result.csv的第几行开始呢(不输入保持默认0):")
    total_task = input("从指定位置的地方开始后，限定任务的长度(比如指定从之后的100个链接中下载图片)\n"
                       "不输入保持默认-1(起始位置之后的所有文章):")
    download_thread = input("下载线程数量(别太离谱，会被反爬限制的, 留空默认4):")

    await ImageDownloader(
        thread = int(download_thread) if download_thread else 4,
        start_from = int(start_from) if start_from else 0,
        total_tasks = int(total_task) if total_task else -1,
        filter_small_image = True if filter_small_image == "1" else False,
        filter_image_list = True if filter_image_list == "1" else False,
        filter_gif = True if filter_gif == "1" else False
    ).start()


async def get_official_account_publish():
    print("\n查看一下 README.md 上的教程再开始使用哦")
    url = input("URL:")
    cookie = input("Cookie:")

    print("\n输入起始页与终止页（如第0页代表最新的文章，数字越大文章发布时间时间越早\n"
          "获取的文章数量是 (终止页 - 起始页) * 5), 不输入保持默认")
    start_page = input("起始页(默认0):")
    end_page = input("终止页(默认-1):)")

    os.makedirs(f"{os.getcwd()}/workdir", exist_ok = True)
    os.chdir(f"{os.getcwd()}/workdir")

    await WechatOfficialAccountFetcher(
        cookie, url,
        start_page = int(start_page) if start_page else 0,
        end_page = int(end_page) if end_page else -1
    ).get_published_articles()


if __name__ == '__main__':
    print("输入序号选择一个你想使用的功能：\n"
          "(1): 获取微信公众号文章\n"
          "(2): 通过微信公众号文章获取其中的图片")
    choice = input()
    if choice == '1':
        asyncio.run(get_official_account_publish())
    elif choice == '2':
        asyncio.run(download_images_from_result())
    else:
        print("Wrong choice")
