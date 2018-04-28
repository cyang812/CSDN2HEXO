# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
import urllib.request
import urllib.parse
import json
import os
from csdn_sdk import *
from md_parse import *

article_list = list()
pic_list = list()
id_title = {}
download_err = {}
pic_cnts = 0

# 列表内容存为文件
def save_list_to_file(list_content, file_name):
    # 列表去重
    list_content = sorted(set(list_content), key = list_content.index)     
    print('list_content len = ', len(list_content))

    with open(file_name, 'w', encoding='utf-8') as file:
        for x in range(0,len(list_content)):
            file.write(str(list_content[x])+'\n') 

# json 内容存为文件
def save_json_to_file(json_dict, f_name):
    """
    把 json 存入文件，用缩进分隔
    :param json_dict:
    :return:
    """
    with open(f_name, 'w', encoding='utf-8') as file:
        # ensure_ascii 为 False
        file.write(json.dumps(json_dict, indent=4, ensure_ascii=False, separators=(',', ': ')))

# 保存 id 和 title 的对应关系
def IDandTitle(json_content, dict_content):
    size = len(json_content['list'])

    for x in range(0,size):
        id = json_content['list'][x]['id']
        title = json_content['list'][x]['title']
        dict_content[id] = title

    # debug
    # for x in range(0,size):
    #     id = json_content['list'][x]['id']
    #     print(dict_content.get(id, "none"))    

# 保存字典到文件
def save_dict_to_file(dict_content, file_name):
    # print(dict_content.keys())
    # print(str(dict_content))
    save_json_to_file(dict_content, file_name+'.json')

# 保存文章 ID 到列表
def update_article_idx(json_dict, art_list):
    num = len(json_dict['list'])
    # debug , last page article count
    if num!=15:
        print('[DEBUG] idx = ',num)

    for x in range(0, num):
        id = json_dict['list'][x]['id']
        art_list.append(id)

# 遍历文章 ID 和标题
def save_article_lists(dict_content):
    article_cnt = csdnOAuthV2.get_stats() # get blog count
    print('article_cnt = ',article_cnt)

    # 每一页 15 篇文章
    if article_cnt%15:
        loop_cnt = int(article_cnt/15) + 1
    else:
        loop_cnt = article_cnt/15    
    # print('loop_cnt = ', loop_cnt) #迭代次数

    for x in range(1,loop_cnt+1):
        if(x == loop_cnt+1):   # last pageE
            size = article_cnt%15
        else:
            size = 15    
        lists = csdnOAuthV2.get_article_list(page=x, size=size)
        # 从 json 中提取 ID 和 Title 信息
        IDandTitle(lists, dict_content)

    save_dict_to_file(dict_content, 'id_title')

# 去除字符串中的非法字符以保存为文件名
def get_file_name(str_content):
    intab = "\/:*?\"<>|"
    outtab = "  ： ？“《》 "     #用于替换特殊字符
    return str_content.translate(str.maketrans(intab,outtab))

# 保存文章的内容 markdown 格式
def save_article_content(idx, file_name):
    article = csdnOAuthV2.get_article(str(idx))
    with open(file_name+'.md', 'w', encoding='utf8') as f:
        try:
            f.write(article['markdowncontent'])
            isSuccess = True
        except Exception as e:
            print("article conntent err", idx, article)
            isSuccess = False

    return isSuccess            

# 下载文章中的图片
def save_article_pic(file_name):
    global pic_cnts
    pics = list()
    find_pics(file_name+'.md', pics)
    delete_watermark(pics)
    pic_cnts += len(pics)
    for pic in pics:
        download_pic(pic)

# 下载所有文章和图片，以标题为文件夹
def save_blog_to_file(dict_content):
    article_lists = dict_content.keys()
    # print(article_lists)

    root_path = os.getcwd()
    if not os.path.exists('blog'):
        os.mkdir('blog')
    os.chdir('blog')    
    print(os.getcwd())
    blog_path = os.getcwd()

    for article_list in article_lists:
        dir_name = get_file_name(dict_content.get(article_list))
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)           
        os.chdir(dir_name)    

        if save_article_content(article_list, dir_name):
            save_article_pic(dir_name)
        else:
            download_err[article_list] = dict_content.get(article_list)

        os.chdir(blog_path)

    # 将下载失败的文章标题写入文件
    os.chdir(root_path)
    save_dict_to_file(download_err, 'download_err')

# main
if __name__ == '__main__':
    '''
    获取 csdn 认证
    http://open.csdn.net/wiki/oauth2
    '''
    csdnOAuthV2 = CsdnOAuthV2()

    # 获取基本的博客信息
    csdnOAuthV2.get_info()

    # 保存所有文章 ID 和标题信息到 json 文件
    save_article_lists(id_title)

    # 下载所有博客
    save_blog_to_file(id_title)
    print('download pic cnt = ', pic_cnts)

