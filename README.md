# AutoLogin_njtech

AutoLogin_njtech 是一款自动登录校园网的应用程序。该软件可以帮助您在启动计算机时自动登录校园网，实现无缝网络连接。主要功能包括记住密码、开机自启动和后台自动检测登录情况。AutoLogin_njtech 基于 Python 语言开发，采用了 PyQt5 框架，实现了自动发送登录请求的功能。软件具有开箱即用的特点，无需安装任何环境，打包成的 exe 文件小巧美观，可以最小化挂在后端，用户无需再次操作界面。

<p align="right"><i><font color=#0000FF> ——made by njtech Melody</font></i></p>

## 使用方法

请点击此处跳转下载。

在下载完成后，运行此软件，你应该会看到如下界面

![image-20230420165357490](.\software interface.png)

在界面中填写学号和密码，选择运营商，选择登录

### 常见情况

- 若未登录校园网，则会报错“尚未连接wifi”
- 若首次登录时学号和密码错误，则会报错“账号或密码错误”
- 若登录成功，则会显示“登录成功！每隔10秒判断一次登录状态”
  - 登录成功后，每10秒检测一次登录情况，若成功登录，则显示“已经登录......”
  - 登录成功后，即使改变学号密码，仍会显示"已经登录......"，这是南工登录页特有的机制(悲)



## 软件功能

- [x] 记住密码：仅成功登录一次后，软件将会记住密码，下次启动无需手动输入
- [x] 开机自启：点选后，软件将注册在开启自启目录中，下次开启电脑将会自动启动
- [x] 后台检测：每10秒访问一次登录页，查看是否登录。这意味着如果你将电脑设置“休眠”或“睡眠”后，下次启动将会自动登录。
- [x] 最小化：挂载在后台中，可以通过右下角图标栏打开，在平时几乎可以忽略该程序



## 技术栈

- 语言：Python
- 框架：PyQt5
- 实现原理：自动发送登录请求



## 联系作者

如果您有任何问题，欢迎通过 `issue` 或 `pulls` 联系我或反馈bug



