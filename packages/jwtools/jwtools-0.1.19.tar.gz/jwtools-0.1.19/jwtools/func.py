import datetime
import hashlib
import json
import random
import time
import os
import sys
import traceback
from typing import Dict, Tuple, List, Callable


def get_text_md5(text) -> str:
    """
    计算字符串md5
    :param text:
    :return:
    """
    # print('md5处理：%s' % text)
    md5 = hashlib.md5(text.encode("utf-8")).hexdigest()
    return md5


def print_vf(*args):
    """
    print var or function
    :author wjh
    :date 2023-05-22
    :param args:
    :return:
    """
    for arg in args:
        if callable(arg):
            print(arg())
        else:
            print(arg)


def print_exit(*args, code=0):
    """
    print var or function
    :author wjh
    :date 2023-05-22
    :param args:
    :return:
    """

    exit()


def print_list(data: list, keys=[]):
    """
    print list
    :author wjh
    :date 2023-11-01
    :param data:
    :param keys: keys for to dict of list item
    :return:
    """
    for arg in data:
        if keys:
            if isinstance(arg, dict):
                pp = {k: v for k, v in arg.items() if k in keys}
                print(pp)
            else:
                print(arg)
        else:
            print(arg)


def get_max_dimension(lst):
    """
    获取列表的最大维度
    :author wjh
    :date 2023-05-23
    :param lst:
    :return:
    """
    if isinstance(lst, list):
        dimensions = [get_max_dimension(item) for item in lst]
        max_dim = max(dimensions) if dimensions else 0
        return max_dim + 1
    else:
        return 0


def flatten_list(lst) -> list:
    """
    平铺列表为一维列表
    递归函数，遍历列表的每个元素。如果元素是列表，则递归调用该函数继续平铺。如果元素是非列表元素，则直接添加到最终的一维列表中
    :author wjh
    :date 2023-05-23
    :param lst: 多维列表
    :return: 平铺后列表
    """
    flattened = []
    for item in lst:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened


def print_line(title='', fill_char='-', length=30, newline=True):
    """
    输出分隔线
    :author wjh
    :date 2023-05-23
    :param title: 标题
    :param fill_char: 填充字符
    :param length: 长度
    :param newline: 是否换行
    :return:
    """
    separator = fill_char * int(length / 2) + title + fill_char * int(length / 2)
    if newline:
        print(separator)
    else:
        print(separator, end='')


def dict_filter_sort(data: dict, filter_func: Callable[[], bool], sort_func: Callable[[], None], top=0,
                     reverse=True) -> dict:
    """
    对 dict 进行过滤并排序，最后返回 top 条记录
    :author wjh
    :date 2023-10-7
    :example  调用示例：
        result = dict_filter_sort(
            data=data,
            filter_func=lambda x: x[0].startswith('k') and x[1].get('weight') >= 0,
            sort_func=lambda item: item[1].get('weight'),
            top=2
        )
    :param data: 数据
    :param filter_func: 过滤函数
    :param sort_func: 排序函数
    :param top: top
    :param reverse: 是否倒序
    :return: 处理后数据
    """
    # 使用 filter 筛选
    filtered_data = filter(filter_func, data.items())
    # 使用 sorted 函数进行倒序排序
    sorted_filtered_data = sorted(filtered_data, key=sort_func, reverse=reverse)
    # 生成最终结果的字典
    result = dict(sorted_filtered_data[:top] if top > 0 else sorted_filtered_data)
    return result


def print_json(content):
    """
    对 json 或 json 字符串进行格式化输出
    :author wjh
    :date 2024-3-8
    :param content: 数据
    :return: None
    """
    if isinstance(content, str):
        content = json.loads(content)

    print(json.dumps(content, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=False))


def get_dict_value(data_dict, keys, default_value=None):
    """
    递归获取嵌套字典中的值，若键不存在则返回默认值
    :param data_dict: 输入的字典
    :param keys: 键列表，表示访问路径
    :param default_value: 键不存在时返回的默认值
    :return: 指定键的值，若不存在则返回 default_value
    """
    if not isinstance(data_dict, dict):
        return default_value

    # 如果 keys 是单个字符串，则将其转换为列表
    if isinstance(keys, str):
        keys = [keys]

    current_value = data_dict
    for key in keys:
        if isinstance(current_value, dict) and key in current_value:
            current_value = current_value[key]
        else:
            return default_value  # 如果某个键不存在，返回默认值
    return current_value



def url_path_join(*args):
    """
    类似于 os.path.join 的 URL 路径拼接函数。
    确保各个路径片段正确拼接，不覆盖前面的路径。
    """
    # 将所有片段去掉多余的斜杠
    stripped_args = [str(arg).strip('/') for arg in args]

    # 用 '/' 分隔符连接各个路径片段
    return '/'.join(stripped_args)


def ensure_trailing_char(path, char='/'):
    """
    确保字符串以指定的字符结尾，默认是 '/'。
    如果没有则添加。
    """
    if not path.endswith(char):
        return path + char
    return path