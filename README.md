# Wechat-Offical-Account-fetcher
本项目仅作个人学习使用

## Usage
1. 克隆本仓库至本地
2. 在网页微信公众平台下创建一个公众号。
3. 在内容与互动中点击 **草稿箱-新的创作-写新图文** 进入文章撰写界面。
4. 打开开发者工具后，在顶部工具栏点击 **超链接-选择其他公众号-输入{公众号名称}**，在开发者工具 **网络** 中找到 **appmsgpublish** 开头的 json 文件
5. 安装 `requirements.txt` 中的库，打开`gui.py`。
6. 分别复制 **Headers-Request Headers** 中的 **Cookie** 值和 **User-Agent** 值，以及 **Payload-Query String Parameters** 中的 **fakeid** 值和**token** 值，粘贴到步骤四打开的窗口，点击 **Start fetching pages** 开始获取列表。
### Extra Reference
上述步骤在以下图文中有对应体现，可供参考：
[python爬取微信公众号文章（包含文章内容和图片）_微信公众号爬虫能爬图片吗-CSDN博客](https://blog.csdn.net/weixin_41267342/article/details/96729138)

## 获取列表后的操作
> 你会发现项目文件夹的根目录下多出一个文件 `app_msg_list.csv` ，打开可以看到获取的文章名称和对应链接
- 使用`pic_downloader.py` 可以把每个文章中大于 90KB 的 `.jpg` ，`.png`，`.gif` 格式的文件根据文章标题下载到 **“~./download/{文章标题}”** 中。
- 使用`pic_search` 可以调用 **ascii2d API** 将下载下来的图片遍历进行以图搜图，主要针对蓝P和黑X上的插画和插图。