# wechat-official-account-toolkit

本项目仅作个人学习使用

## Usage

1. 在网页微信公众平台下创建一个公众号。
2. 在内容与互动中点击 **草稿箱-新的创作-写新图文** 进入文章撰写界面。
3. 打开开发者工具，在顶部工具栏点击 **超链接-选择其他公众号**，输入公众号名称，**网络（Network）** 中找到 **appmsgpublish**
   开头的 js 响应，右键复制 URL，再单点此 json，在右侧 **Headers-Request Headers** 一栏复制其中的 **Cookie** 值
4. `pip install -r requirements.txt && python main.py`

### Extra Reference

上述步骤在以下图文中有对应体现，可供参考：  [python爬取微信公众号文章（包含文章内容和图片）_微信公众号爬虫能爬图片吗-CSDN博客](https://blog.csdn.net/weixin_41267342/article/details/96729138)