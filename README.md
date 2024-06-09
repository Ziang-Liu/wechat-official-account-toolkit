# Wechat-Offical-Account-fetcher  
  
本项目仅作个人学习使用  
  
## Usage  
  
1. 克隆本仓库至本地  
2. 在网页微信公众平台下创建一个公众号。  
3. 在内容与互动中点击 **草稿箱-新的创作-写新图文** 进入文章撰写界面。  
4. 打开开发者工具后，在顶部工具栏点击 **超链接-选择其他公众号-输入{公众号名称}**，在开发者工具 **网络** 中找到 **appmsgpublish** 开头的 json 文件 ，右键点击复制该文件的 url  
5. 安装 `requirements.txt` 中的库，运行`main.py` (`asyncio.run(get_official_account_publish())`取消掉注释)  
6. 根据控制台提示粘贴 url 和 **Headers-Request Headers** 中的 **Cookie** 值，输出的结果会保存在`workdir/results.csv`文件中  
  
### Extra Reference  
  
上述步骤在以下图文中有对应体现，可供参考：  [python爬取微信公众号文章（包含文章内容和图片）_微信公众号爬虫能爬图片吗-CSDN博客](https://blog.csdn.net/weixin_41267342/article/details/96729138)