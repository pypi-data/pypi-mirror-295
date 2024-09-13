# -*- encoding：utf-8 -*-

# ailab.

# Created :2024-9-12  16:50
# Author：AI Lab 100 Morgan
# Copyright (C) 2020-2024  数智教育发展 (山东) 有限公司
# For license information, see LICENSE.txt
# ID: main.py

import itertools

case_list = ['用户名', '密码']
value_list = ['正确', '不正确', '特殊符号', '超过最大长度']


def gen_case(item=case_list, value=value_list):
    '''输出笛卡尔用例集合'''
    for i in itertools.product(item, value):
        print('输入'.join(i))

def test_print():
     print("欢迎搜索关注公众号: 「测试开发技术」!")

if __name__ == '__main__':
    test_print()
