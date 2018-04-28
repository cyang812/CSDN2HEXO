# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
import urllib.request
import urllib.parse
import json

# base on https://github.com/DouMiaoO-Oo/CSDN-SDK

ACCESS_KEY = ""  # client_id
SECRET_KEY = ""  # client_secret
USER_NAME = ""
PASSWORD = ""

class CsdnOAuthV2:
    """
    csdn 客户端版本的类，用来进行一些需要的操作
    """
    def __init__(self):
        self.access_token = self.get_csdn_access_token()

    @staticmethod
    def get_csdn_access_token():
        """
        利用客户端的方式登录，解析 response 中的json格式数据
        :return: 解析好的 json，保存为 dict
        """
        url = 'http://api.csdn.net/oauth2/access_token?client_id=%s' \
              '&client_secret=%s' \
              '&grant_type=password' \
              '&username=%s' \
              '&password=%s'

        print(url % (ACCESS_KEY, SECRET_KEY, USER_NAME, PASSWORD))
        response = urllib.request.urlopen(url % (ACCESS_KEY, SECRET_KEY, USER_NAME, PASSWORD))
        res = response.read().decode()
        response.close()
        print(res)
        return json.loads(res, encoding="utf-8")['access_token']

    def get_article_list(self, status="enabled", page=1, size=15):
        """
        api doc: http://open.csdn.net/wiki/api/blog/getarticlelist
        :param status: enabled|draft
        :param page:
        :param size:
        :return:
        """
        query_para = urllib.parse.urlencode({'access_token': self.access_token, 'status': status,
                                             'page': page, 'size':size})
        url = 'http://api.csdn.net/blog/getarticlelist?'+query_para
        response = urllib.request.urlopen(url)
        res = response.read().decode()
        response.close()
        return json.loads(res, encoding="utf-8")

    def get_info(self):
        query_para = urllib.parse.urlencode({'access_token': self.access_token})
        url = 'http://api.csdn.net/blog/getinfo?' + query_para
        print(url)
        response = urllib.request.urlopen(url)
        res = response.read().decode()  # decode from bytes to utf-8
        print(res)
        return json.loads(res, encoding='utf8')  

    def get_stats(self):
        query_para = urllib.parse.urlencode({'access_token': self.access_token})
        url = 'http://api.csdn.net/blog/getstats?' + query_para
        print('url = ', url)
        response = urllib.request.urlopen(url)
        res = response.read().decode()  # decode from bytes to utf-8
        print('res = ', res)
        cnt = json.loads(res, encoding='utf8')['original_count']
        cnt += json.loads(res, encoding='utf8')['repost_count'] 
        cnt += json.loads(res, encoding='utf8')['translated_count'] 
        return cnt                

    def get_article(self, article_id):
        """
        api doc: http://open.csdn.net/wiki/api/blog/getarticle
        :param article_id: article id
        :return: title
        """
        query_para = urllib.parse.urlencode({'access_token': self.access_token, 'id': article_id})
        url = 'http://api.csdn.net/blog/getarticle?' + query_para
        print(url)
        response = urllib.request.urlopen(url)
        res = response.read().decode()  # decode from bytes to utf-8
        return json.loads(res, encoding='utf8')

    def save_article(self, title, content, type="original", **kw):
        """
        这一页的 csdn api 有错误，应该是repost 而不是 report
        api doc: http://open.csdn.net/wiki/api/blog/savearticle
        这里应该用 post 方法吧，毕竟要传输那么多博客内容
        :param title:
        :param type: original|repost|translated
        :param content:
        :param kw:
                   id, modify article need to specify id.
                   description
                   categories
                   tags
                   ip
        :return:
        """
        req = urllib.request.Request('')  # http post method
        para_dict = {'access_token': self.access_token}

        if type not in ('original', 'report', 'translated'):
            print("type 参数只有三个合法值 original | repost | translated")
            # 这里应该抛出一个异常比较好
            return None
        if kw.__contains__('id'):
            para_dict[id] = kw['id']
        if kw.__contains__('description'):
            para_dict[id] = kw['id']

# module test
if __name__ == '__main__':
    '''
    获取 csdn 认证
    http://open.csdn.net/wiki/oauth2
    '''
    csdnOAuthV2 = CsdnOAuthV2()

    # 获取基本的博客信息
    csdnOAuthV2.get_info()            