import json, requests, time, random

# note: 微信公众号有较强的反爬措施，如果公众号列表很长的话爬取时间会很长，
#       而且大概率会被风控，仅作学习参考使用。
#       同时，获取列表的方法具有时效性，可能某个时间点此方法就失效了。

# 获取模拟请求参数
def get_params(cookie, user_agent, fakeid, token) -> str:

    headers = {
        "Cookie": str(cookie),
        "User-Agent": str(user_agent)
    }

    # 参数，可能要按需修改，详见 request url
    params = {
        "sub": "list",
        "begin": "0", # 默认第 0 页开始 fetch
        "count": "5",
        "fakeid": str(fakeid),
        "type": "101_1",
        "free_publish_type": "1",
        "sub_action": "list_ex",
        "token": str(token),
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

    with open("app_msg_list.csv", "w",encoding='utf-8') as file:
        file.write("title,url\n")
    
    return headers, params

def get_page_list(cookie, user_agent, fakeid, token) -> str:
    
    url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
    headers,params=get_params(cookie, user_agent, fakeid, token)
    i = 0

    while True:
        
        begin = i * 5
        params["begin"] = str(begin)
        
        # 随机暂停，模拟用户请求
        time.sleep(random.randint(5,30))
        
        # 获取的返回内容
        resp = requests.get(url, headers=headers, params = params, verify=False) # str
        
        # 反爬风控
        if resp.json()['base_resp']['ret'] == 200013:
            print("frequencey control, stop at {}".format(str(begin)))
            time.sleep(3600)
            continue
        '''
        # 如果返回的内容中为空则结束
        if len(resp.json()['app_msg_list']) == 0:
            print("all ariticle parsed")
            break
        '''
        msg = resp.json() # dict

        if "publish_page" in msg:
            publish_page = json.loads(msg["publish_page"]) # dict -> str -> dict
            publish_list = publish_page["publish_list"] # dict -> list
            for list_item in publish_list:
                publish_info = json.loads(list_item["publish_info"]) # list -> dict -> str -> dict
                appmsgex = publish_info["appmsgex"] # dict -> list
                for item in appmsgex: # list -> dict
                    info = '"{}","{}"'.format(item['title'], item['link']) # dict -> str
                    with open("app_msg_list.csv", "a",encoding='utf-8') as f:
                        f.write(info+'\n')
                    print(f'写入链接，标题：{item['title']}')

        # 下一个列表
        i += 1    