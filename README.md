# Xtools

### 前言
Xtools 是一款 Sublime Text 插件，同时是一款简单的资产处理工具，在渗透测试实战过程中，有很多重复的操作，所以思考着写一款小工具来减少重复的劳动。

日常渗透中使用过一款资产文本清洗工具,使用起来感觉不错，并且添加了一些额外功能和修改了暗黑主题，在此感谢 xinyu2428 师傅。
```
https://github.com/xinyu2428/HTML_TOOLS
```

在日常使用过程中，总感觉缺少了点什么。思考着继续补充 javascript 代码，发现无法和命令行进行交互，遂放弃。一番挣扎过后，发现很多时候都在使用 Subliem Text 编辑器，嗯，最后的思路就是集成在 Sublime Text 插件。这样一来，同时减少了很多的 ctl+c 和 ctl+v。  

<img width="1649" alt="1" src="https://github.com/chasingboy/Xtools/assets/39737245/e3f15d93-f6c7-4baf-9d44-ca01dfbab00d">
  
### 功能

1. IP、domain、url 处理
   * 提取 IPv4 (内网、外网)
   * IPv4 和 C 段互转
   * 提取 domain（根域名、所有域名）
   * 提取 url（有路径、无路径）
   * 提取 router（js、text）
   * 过滤 CDN 和 DNS 域名和IP（需补充）
2. 简单文本处理
   * 删除特殊字符、空格、`[*]`、`(*)` （* 表示括号内的所有内容）
   * 按行提取指定内容
   * 按行删除指定内容
   * 替换指定字典的 key 和 value
3. 简单编码和解码
   * base64 编码和解码
   * md5 加密
4. 调用系统命令执行
   * curl 下载文件
   * sqlmap
   * ......（自行配置）
  
### 使用截图
1. 在文本中提取 IP。

<img width="1736" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/b53054e3-2192-4292-98cb-08068bbbe219"><br/>
    
2. 按行进行 base64 编码。

<img width="1736" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/ac3ffa1f-ff2a-45c8-b018-72dc37891108"><br/>

3. 按字典进行 key 和 value 替换。

<img width="1721" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/c2c0d300-26c7-4b49-aa5f-0c06f63d8b38"><br/>

4. 打开终端调用 sqlmap。

<img width="1736" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/933036ac-52be-4fac-b315-73bc59e6cafd"><br/>

5. curl 批量下载文件，会在桌面自动创建 work 文件夹，并保存下载结果。

<img width="1731" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/071abf87-839d-49f3-bca6-ac9719327e8e"><br/>

6. 在处理需要输入时，选择 Input Text 即可打开输入框。

<img width="1698" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/96b80ebb-c73d-4666-b527-fb998d4d2f1b"><br/>

### 配置命令行
选择 Setting Config 即可打开配置文件，并在注释的范围内添加需要的系统命令。统一格式为 `"args": {"cmd":"sqlmap -r target.txt"}`， 比如 slqmap，httpx，nuclei。

```
/* 通过 <args->cmd> 设置命令, 设置目标为 target.txt, 运行时自动替换为临时文件
                       eg: httpx -l target.txt
                       */
                    {
                        "caption": "httpx",
                        "command": "run_cmd",
                        "args": {"cmd":"httpx -sc -title -l target.txt"}
                    },
                    {
                        "caption": "nuclei",
                        "command": "run_cmd",
                        "args": {"cmd":"nuclei -l target.txt"}
                    },
                    {
                        "caption": "sqlmap",
                        "command": "run_cmd",
                        "args": {"cmd":"sqlmap -r target.txt"}
                    },

                    /* -- END -- */
```

~~⚠️注意：命令行功能目前只支持 macOS。~~

#### 新增支持 windows 命令行调用
```
/* 通过 <args->cmd> 设置命令, 设置目标为 target.txt, 运行时自动替换为临时文件
                       eg: httpx -l target.txt
                       */
                    {
                        "caption": "httpx",
                        "command": "run_cmd",
                        "args": {"cmd":"C:\\Users\\kali\\httpx\\httpx -sc -title -l target.txt"}
                    },
                    /* -- END -- */
```
比如配置 httpx 命令，或者把 httpx 命令添加到环境变量。

<img width="1846" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/ecc36edb-c1d0-40d2-907c-7fd90bce36ac">


### 安装
下载源码，github 下载后文件名 Xtools-main.zip，解压后需重命名为 Xtools，否则可能某些路径出错。

进入到 Sublime Text 插件目录：Preferences->Browse Packpages，把 Xtools 放在该目录下，同时解压 applescript 文件即可。

<img width="1730" alt="image" src="https://github.com/chasingboy/Xtools/assets/39737245/6d4a5c50-1079-4534-8acf-9aec8213dc23"><br/>

注意：python 调用 masOS 终端需要 applescript 模块，需在 Xtools 目录下解压 applescript.zip

#### 安装报错
最近有师傅反馈，window 11 安装时出现错误，功能无法正常使用。经过调试，发现是师傅的系统**用户名是中文**。如果系统的用户名是中文且安装不成功，可以尝试在 xtools.py 文件自定义系统用户名。
```
if platform == 'windows':
    HOME = os.environ['HOMEPATH']
else:
    HOME = os.environ['HOME']

'''
如果系统的用户名是中文且安装不成功，可以尝试在 xtools.py 文件自定义系统用户名，并删除 # 注释。
'''
# HOME = "/Users/" + u"<用户名>"  # osx
# HOME = "/home/" + u"<用户名>"  # linux
# HOME = "C:\Users\" + u"<用户名>"  # windows
workdir = os.path.join(HOME,'.xtools')
```

### 特别感谢
xinyu2428 师傅 https://github.com/xinyu2428/HTML_TOOLS

linkfinder https://github.com/GerbenJavado/LinkFinder

### 更新记录
[+] 2023-07-15 增加 Windows 命令行调用支持。

[+] 2023-07-18 增加一键排序去重、提取 javascript 文件路由。
