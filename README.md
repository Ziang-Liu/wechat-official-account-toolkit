# wechat-official-account-toolkit

本项目仅作个人学习使用

### Step-by-Step Tutorial

1. **登录微信公众号平台**：
    - 访问微信公众号平台并使用您的账号登录。

2. **进入文章撰写界面**：
    - 导航至 **内容与互动**，选择 **草稿箱**，然后点击 **新的创作**，选择 **写新图文** 以进入文章撰写界面。

3. **获取开发者工具中的 Cookie 值**：
    - 打开浏览器的开发者工具。
    - 在顶部工具栏中点击 **超链接**，选择 **其他公众号**，并输入目标公众号的名称。
    - 在 **网络 (Network)** 面板中找到以 **appmsgpublish** 开头的 JavaScript 响应，右键点击并复制其 URL。
    - 单击该 JSON 响应，在 **Headers** 标签下的 **Request Headers** 部分复制 **Cookie** 值。

4. **安装依赖并运行脚本**：
    - 在终端中运行以下命令以安装所需依赖并执行脚本：
      ```sh
      pip install -r requirements.txt && python main.py
      ```
