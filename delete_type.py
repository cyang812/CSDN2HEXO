# !/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re

# 去除文件名的后缀
def get_lists_path(path):
	file_list = os.listdir(path) #列出文件夹下所有的目录与文件
	print(len(file_list))
	os.chdir(path)
	for i in range(0,len(file_list)):
		temp_str = file_list[i].split('.')[0]
		print(temp_str)
		os.rename(file_list[i], temp_str)

	return file_list

# module test
if __name__ == '__main__':
	pic_lists = get_lists_path('pic')