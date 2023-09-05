import unittest
import requests  # 用于发送HTTP请求

# 导入您的 MiniFlask 应用
from server import app

class MiniFlaskTestCase(unittest.TestCase):
    def setUp(self):
        # 在每个测试用例开始前，创建一个测试服务器的地址
        self.base_url = 'http://0.0.0.0:8001'

    def test_home_page(self):
        # 发送GET请求到首页
        response = requests.get(self.base_url + '/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'Hello, World!')

    def test_about_page(self):
        # 发送GET请求到/about页面
        response = requests.get(self.base_url + '/about')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'About Page')

    def test_json_example_get(self):
        # 发送GET请求到/json_example
        response = requests.get(self.base_url + '/json_example')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, JSON!'})

    def test_json_example_post(self):
        # 发送POST请求到/json_example
        response = requests.post(self.base_url + '/json_example')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, 'POST Request Received')

if __name__ == '__main__':
    unittest.main()
