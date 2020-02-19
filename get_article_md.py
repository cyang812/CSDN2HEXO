# -*- coding: utf-8 -*-
# @Author: cy101
# @Date:   2020-02-18 22:18:14
# @Last Modified by:   cyang
# @Last Modified time: 2020-02-19 21:00:02

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-29 21:17:36
# @Author  : Kaiyan Zhang (kaiyanzh@outlook.com)
# @Link    : https://github.com/iseesaw
# @Version : v1.0
"""
将csdn博客导出为markdown
方法：
1. 编辑博客，抓包
2. 获取博客markdown格式链接
https://mp.csdn.net/mdeditor/getArticle?id=100125817
3. 模拟请求
Request Headers
:authority: mp.csdn.net
:method: GET
:path: /mdeditor/getArticle?id=100125817
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8
cookie: uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FpostList%252Flist%22%2C%22tid%22%3A%22e0a1148715d862%22%2C%22q%22%3A0%2C%22a%22%3A42%7D; ViewMode=list; aliyun_webUmidToken=T9204DD7B1A1971E571EFE43913410386D4C2C9D905BA336A2BEDBC206D; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567074771,1567083797,1567083801,1567084099; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567084279; dc_tos=px01z9
referer: https://mp.csdn.net/mdeditor/100125817
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: 
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36

Query String Parameters
id=100125817
"""
import json
import uuid
import time
import requests
import datetime
from bs4 import BeautifulSoup

def request_blog_list(page=1):
    """获取博客列表
    主要包括博客的id以及发表时间等
    """
    url = f'https://blog.csdn.net/u011303443/article/list/{page}'
    reply = requests.get(url)
    parse = BeautifulSoup(reply.content, "lxml")
    spans = parse.find_all('div', attrs={'class':'article-item-box csdn-tracking-statistics'})
    blogs = []
    for span in spans[:40]:
        try:
            href = span.find('a', attrs={'target':'_blank'})['href']
            read_num = span.find('span', attrs={'class':'num'}).get_text()
            date = str.strip(span.find('span', attrs={'class':'date'}).get_text())  
            blog_id = href.split("/")[-1]
            # print(blog_id)
            # artile_info = str(blog_id + "--" + date + "--" + href)
            # blogs.append(article_info)
            blogs.append([blog_id, date, href])
        except:
            print('Wrong, ' + href)
    return blogs

def write_hexo_md(data, date, herf):
	"""将获取的json数据解析为hexo的markdown格式"""
	title = data["data"]["title"]
	title = title.replace("[", "【")
	title = title.replace("]", "】")
	title = title.replace(":", "：")
	tags = data["data"]["tags"]
	# 页面唯一标识符，用于统计系统和评论系统
	key = "key" + str(uuid.uuid4())
	now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	name = title
	tag = "tags:\n- " + "\n- ".join(tags.split(","))

	header = "---\n" + f"title: {title}\n" + f"date: {date}\n" +f"update: {now_time}\n" +f"comments: true\n" + tag + "\n" + f"categories:\n- " + f"\nthumbnail: \n" + "---\n\n"
	# f"key: {key}\n" +

	content = data["data"]["markdowncontent"].replace("@[toc]", "")
	tail = f"\n\n原文链接：[本人CSDN博客]({herf})"

	with open(f"./_posts/{name}.md", "w", encoding="utf-8") as f:
	    f.write(header + content + tail)

	print(f"写入 {name}")

def request_md(blog_id, date, herf):
    """获取博客包含markdown文本的json数据"""
    # url = f"https://mp.csdn.net/mdeditor/getArticle?id={blog_id}"
    # url = f"https://editor.csdn.net/md/?articleId={blog_id}"
    url = f"https://blog-console-api.csdn.net/v1/editor/getArticle?id={blog_id}"

    headers = {
        "cookie": "uuid_tt_dd=; dc_session_id=10_1561467833929.923263; UN=u011303443; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_19021907720-1561467833929-323401!5744*1*u011303443!1788*1*PC_VC; smidV2=20190720220913ca61bb166cfbfdd7d0d32cd11558413600cbd8e6cd99e2f80; UserName=u011303443; UserInfo=3a05b754f03342648c9a95b86db5b46f; UserToken=3a05b754f03342648c9a95b86db5b46f; UserNick=cyang812; AU=997; BT=1581342799648; p_uid=U000000; searchHistoryArray=%255B%2522csdn%2522%252C%2522hexo%2522%255D; hasSub=true; announcement=%257B%2522isLogin%2522%253Atrue%252C%2522announcementUrl%2522%253A%2522https%253A%252F%252Fblog.csdn.net%252Fblogdevteam%252Farticle%252Fdetails%252F103603408%2522%252C%2522announcementCount%2522%253A0%252C%2522announcementExpire%2522%253A3600000%257D; c_adb=1; utm_source=distribute.pc_relevant.none-task; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1582032249,1582032251,1582032251,1582032298; aliyun_webUmidToken=T9EC8B488EDE1E1BA24CC9B3C61EFF539561C75EA7F6E9992EF4EBFD85B; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1582032788; dc_tos=q5wgei",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36"
    }
    data = {"id": blog_id}
    print(url)
    # reply = requests.get(url, headers=headers, data=data)
    reply = requests.get(url, headers=headers)
    print(reply)
    # print(reply.json)

    try:
        write_hexo_md(reply.json(), date, herf)
    except Exception as e:
        print("***********************************")
        print(e)
        print(reply.json())

def main(total_pages): 
	"""
	获取博客列表，包括id，时间，链接
	获取博客markdown数据
	保存hexo格式markdown
	"""
	blogs = []
	for page in range(1, total_pages + 1):
		blogs.extend(request_blog_list(page))
	print(len(blogs))   

	for blog in blogs:
		print(blog[0], blog[1], blog[2])
		blog_id = blog[0]
		date = blog[1]
		herf = blog[2]
		request_md(blog_id, date, herf)
		time.sleep(1)

if __name__ == '__main__':
    main(total_pages=4) # change accordingly
