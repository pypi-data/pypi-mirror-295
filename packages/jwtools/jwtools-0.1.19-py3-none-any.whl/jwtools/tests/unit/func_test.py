import unittest
import inspect
from jwtools.func import *
from jwtools.tests.test_base import BasicsTestCase


class FuncTestCase(BasicsTestCase):
    def test_flatten_list(self):
        print_line('不使用 NumPy 平铺列表')

        # 示例列表
        my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]]]

        # 不使用 NumPy 平铺列表
        flattened_list = flatten_list(my_list)
        print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        assert_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertListEqual(flattened_list, assert_list)

        # 示例列表
        my_list = [[1, 2, 3], [4, [5, 6]], [7, 8, [9, 10]], [11, [12, [13, 14, [15, 16]]]]]
        flattened_list = flatten_list(my_list)
        print(flattened_list)  # 输出 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        assert_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
        self.assertListEqual(flattened_list, assert_list)

    def test_get_max_dimension(self):
        print_line('test_get_max_dimension')
        lst = [
            [1, 2, 3],
            [1, [2, 3]],
            [1, [2, [3, 4]]],
            [1, [2, [3, 4, [5, 6]]]],
            [1, [2, [3, 4, [5, [6]]]]],
        ]
        result = [get_max_dimension(item) for item in lst]
        print_vf('input:', lst, 'output:', result)
        self.assertListEqual(result, [1, 2, 3, 4, 5])

    def test_dict_filter_sort(self):
        data = {
            'k1': {'weight': 0},
            'k2': {'weight': 3},
            'k3': {'weight': 1},
            'z1': {'weight': 2},
            'z2': {'weight': 2}
        }

        result = dict_filter_sort(
            data=data,
            filter_func=lambda x: x[0].startswith('k') and x[1].get('weight') >= 0,
            sort_func=lambda item: item[1].get('weight'),
            top=2
        )
        print([(k, v) for k, v in result.items()])

        self.assertTrue(True)

    def test_print_list(self):
        data = [
            {'key': 'k1', 'level': '1', 'weight': 0},
            {'key': 'k2', 'level': '2', 'weight': 3},
            {'key': 'k3', 'level': '3', 'weight': 1},
            {'key': 'z1', 'level': '1', 'weight': 2},
            {'key': 'z2', 'level': '2', 'weight': 2}
        ]

        # for item in data:
        #     print({k: v for k, v in item.items()})
        #     break

        print_list(data)
        print_list(data, ['key', 'level'])

        self.assertTrue(True)

    def test_print_json(self):
        data = '{"id":1,"message":"\u6211\u662fA1\u54c8\u54c8"}'
        print_json(data)

        data2 = {"id": 1, "message": "\u6211\u662fA1\u54c8\u54c8"}
        print_json(data2)

        self.assertTrue(True)

    def test_dict_value(self):
        # 示例数据
        data = {
            "p01": {
                "type": "proxy-pool",
                "region": "gn",
                "params": {
                    "username": "t10565224196293",
                    "password": "nxdhhkof",
                    "http": {
                        "host": "f753.kdltps.com",
                        "port": 15818
                    },
                    "socks": {
                        "host": "f753.kdltps.com",
                        "port": 20818
                    }
                }
            }
        }

        # 示例调用
        keys = ["p01", "params", "http", "host"]
        result = get_dict_value(data, keys, default_value="default_host")
        print(result)  # 输出: "f753.kdltps.com"

        # 当某个键不存在时
        keys = ["p01", "params", "http", "non_existent_key"]
        result = get_dict_value(data, keys, default_value="default_value")
        print(result)  # 输出: "default_value"

        # 当某个键不存在时
        keys = ["p01", "params", "http2", "non_existent_key"]
        result = get_dict_value(data, keys, default_value="default_value")
        print(result)  # 输出: "default_value"

        self.assertTrue(True)

    def test_url_path_join(self):
        base_url = 'tmp2/7fda40a173648558af3e3d693a71c1d9'
        file_path = '6260d6875c0e8938dfb08eb69bf6ee8f.png'

        result = url_path_join(base_url, file_path)
        print(result)

        self.assertTrue(True)

    def test_ensure_trailing_slash(self):
        # 示例
        path1 = "tmp2/7fda40a173648558af3e3d693a71c1d9"
        path2 = "tmp2/7fda40a173648558af3e3d693a71c1d9/"
        path3 = "example.com/api"

        print(ensure_trailing_char(path1))  # 输出: tmp2/7fda40a173648558af3e3d693a71c1d9/
        print(ensure_trailing_char(path2))  # 输出: tmp2/7fda40a173648558af3e3d693a71c1d9/
        print(ensure_trailing_char(path3, '?'))  # 输出: example.com/api?

        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
