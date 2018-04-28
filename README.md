# CSDN2HEXO

CSDN2HEXO 是一款基于[CSDN开放平台](http://open.csdn.net/) 的 csdn blog 内容下载器， 可以下载博客中的文章内容和图片，文章保存为 markdown 格式，图片可下载无水印图片，并根据文章标题生成文件夹存储相关数据。

## 用法
- 1、首先需要获得开发者认证，并创建应用，获取到 App_key 和 App_secret 以通过 OAuth2 认证，可[在此获取](http://open.csdn.net/apps/createapp)

- 2、将 App_key，App_secret，CSDN_username，CSDN_secret 填入 `csdn_sdk.py` 文件开头处

- 3、运行 `csdn-spider.py`

## 结果展示
- 1、文章列表 
	![文章列表](https://github.com/cyang812/CSDN2HEXO/raw/master/1.png)
- 2、文章内容 	
	![博客内容](https://github.com/cyang812/CSDN2HEXO/raw/master/2.png)


## 特性
- 1、下载 csdn 博客的部分文章时，可能会出现返回的 json 数据仅为 `{'status': True}`，此时文章内容无法获取。会将出错的文章id 和文章标题写到本地 `download_err.json` 文件。

- 2、如果是分析本地的 hexo 博客 markdown 文件，则运行 `md_parse.py`。可下载其中的无水印图片，并可替换图床，加入图片样式。


