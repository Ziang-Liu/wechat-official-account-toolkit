import requests, os, concurrent.futures, csv, re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# 公众号的大部分图片应该可以下载到

def get_default_folder() -> str:
    current_directory = os.path.dirname(__file__)
    new_folder_path = os.path.join(current_directory, "download")
    os.makedirs(new_folder_path, exist_ok=True)
    return new_folder_path

def create_valid_folder_name(folder_name) -> str:
    invalid_chars = r'[\\/:*?"<>|]' # 保证文件夹里没有非法符号
    valid_folder_name = re.sub(invalid_chars, '', folder_name)
    return valid_folder_name

def get_pictures(url, file_path) -> None:
    if not os.path.exists(file_path):
        requested_url = requests.get(url)
        with open(file_path, 'wb') as f:
            for chunk in requested_url.iter_content(chunk_size=128):
                f.write(chunk)

        if os.path.getsize(file_path) < 90 * 1024: # 文件大小小于 90KB 就跳过下载，不需要就删掉这个逻辑
            os.remove(file_path)
    else:
        return

def get_file_extension_from_url(url) -> str: # 公众号存在的图片格式，按需增减
    if "jpeg" in url:
        return ".jpg"
    elif "jpg" in url:
        return ".jpg"
    elif "png" in url:
        return ".png"
    elif "gif" in url:
        return ".gif"
    else:
        pass

def get_pictures_urls(text) -> list:
    urls = []
    start_tag = 'src="'
    end_quote = '"'
    target_domain = 'mmbiz.qpic.cn' # 目标域名，按需修改
    start = 0
    while True:
        start = text.find(start_tag, start)
        if start == -1:
            break 
        start += len(start_tag)
        end = text.find(end_quote, start)
        if end == -1:
            break
        url = text[start:end]
        if target_domain in url:
            urls.append(url)
        start = end
    
    return urls

def start_download():
    user_agent = UserAgent()
    ran_user_agent = user_agent.random
    headers = {'User-Agent': ran_user_agent}
    
    with open('app_msg_list.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']
            if "mp.weixin.qq.com" not in url:
                print('Detect wrong links %s' % url)
                continue
            
            requested_url = requests.get(url, headers=headers)
            image_urls = get_pictures_urls(requested_url.text)
        
            # 获取标题，出问题的话审查网页源代码看标题所在标签和类
            soup = BeautifulSoup(requested_url.text, 'html.parser')
            title_tag = soup.find("h1", class_="rich_media_title")

            if title_tag is not None:
                title = title_tag.get_text(strip=True)
                converted_title = create_valid_folder_name(title)

                address = get_default_folder()
                target_path = os.path.join(address, converted_title)
                os.chdir(address)
                if not os.path.exists(target_path):
                    os.mkdir(target_path)
                else:
                    pass
                os.chdir(target_path)

                with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor: # 按需修改线程下载，不建议太高
                    future_to_url = {executor.submit(get_pictures, url, f'img{i}{get_file_extension_from_url(url)}'): url for i, url in enumerate(image_urls)}
                    for future in concurrent.futures.as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            future.result()
                        except Exception as e:
                            print(f"Failed to download {url}: {e}")
            else:
                print("Title not found. Skipping the download process.")


if __name__ == "__main__":
    start_download()