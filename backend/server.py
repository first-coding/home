import socket
import threading
import json
import os
from threading import Lock
from concurrent.futures import ThreadPoolExecutor
import logging

logging.basicConfig(filename='./server.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MiniFlask:
    def __init__(self):
        self.routes = {}
        self.static_dir = 'static'
        self.routes_lock = Lock()  # 添加锁以确保路由字典的线程安全性
        self.thread_pool = ThreadPoolExecutor(max_workers=4)  # 创建线程池

    def route(self, path, methods=['GET']):
        def decorator(func):
            with self.routes_lock:  # 在修改路由字典时获取锁
                self.routes[path] = {'func': func, 'methods': methods}
            return func
        return decorator

    def handle_request(self, request,client_address):
        method, path, headers, body = self.parse_request(request)
        route = self.routes.get(path)
        # 记录请求信息
        request_info = f'Received {method} request for {path} from {client_address},Body: {body}'
        logging.info(request_info)
        try:
            if route:
                if method in route['methods']:
                    try:
                        if len(route['methods'])==1:
                            response_body = route['func'](request)
                            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}'
                        else:
                            response_body = route['func'](request,method)
                            response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}'
                    except Exception as e:
                        # 记录异常信息
                        error_message = f'Internal Server Error: {str(e)}'
                        response = f'HTTP/1.1 500 Internal Server Error\r\nContent-Length: {len(error_message)}\r\n\r\n{error_message}'
                        error_info = f'Error for {client_address}, Path: {path}, Error: {error_message}'
                        logging.error(error_info)
                else:
                    response_body = 'Method Not Allowed'
                    response = f'HTTP/1.1 405 Method Not Allowed\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}'
                    # 记录响应信息
                    response_info = f'Sent response for {path} to {client_address}, Status: 405 Method Not Allowed'
                    logging.info(response_info)
            else:
                # Check if it's a static file request
                static_file_path = os.path.join(self.static_dir, path[1:])
                if os.path.isfile(static_file_path):
                    with open(static_file_path, 'rb') as file:
                        response_body = file.read()
                        response = f'HTTP/1.1 200 OK\r\nContent-Length: {len(response_body)}\r\n\r\n'
                        # 记录响应信息
                        response_info = f'Sent response for {path} to {client_address}, Status: 200 OK'
                        logging.info(response_info)
                else:
                    response_body = 'Not Found'
                    response = f'HTTP/1.1 404 Not Found\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}'
                    # 记录响应信息
                    response_info = f'Sent response for {path} to {client_address}, Status: 404 Not Found'
                    logging.info(response_info)
        except Exception as e:
            # 记录异常信息
            error_message = f'Internal Server Error: {str(e)}'
            response = f'HTTP/1.1 500 Internal Server Error\r\nContent-Length: {len(error_message)}\r\n\r\n{error_message}'
            error_info = f'Error for {client_address}: {error_message}'
            logging.error(error_info)
        return response
    
    def parse_request(self, request):
        # 解析HTTP请求，分离请求行、请求头和请求体
        request_lines = request.split('\r\n')
        request_line = request_lines[0]
        headers = request_lines[1:-2]
        body = request_lines[-1]

        # 解析请求行
        method, path, _ = request_line.split(' ', 2)

        # 解析请求头，将其存储为字典
        headers_dict = {}
        for header in headers:
            key, value = header.split(': ', 1)
            headers_dict[key] = value

        return method, path, headers_dict, body

    def handle_client(self, client_socket, client_address):
        try:
            request = client_socket.recv(1024).decode('utf-8')
            while request:  # 循环接收直到客户端关闭连接
                try:
                    response = self.handle_request(request, client_address)
                    client_socket.send(response.encode('utf-8'))
                    request = client_socket.recv(1024).decode('utf-8')
                except Exception as e:
                    error_message = f'Internal Server Error: {str(e)}'
                    response = f'HTTP/1.1 500 Internal Server Error\r\nContent-Length: {len(error_message)}\r\n\r\n{error_message}'
                    client_socket.send(response.encode('utf-8'))
        except OSError as e:
            if e.errno != 10038:  # 忽略已关闭套接字的错误
                raise
        finally:
            client_socket.close()

        
    def run(self, host, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)

        print(f'Server is listening on {host}:{port}')

        while True:
            client_socket, client_addr = server_socket.accept()
            self.thread_pool.submit(self.handle_client, client_socket, client_addr)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_addr))
            client_thread.start()


app = MiniFlask()

# 示例路由定义
@app.route('/')
def index(request):
     data = {'message': 'Hello, World!'}
     return json.dumps(data)

@app.route('/about')
def about(request):
    return 'About Page'

@app.route('/json_example', methods=['GET', 'POST'])
def json_example(request,methods):
    if methods == 'GET':
        data = {'message': 'Hello, JSON!'}
        return json.dumps(data)
    elif methods == 'POST':
        # 在这里处理POST请求的逻辑，使用请求体中的数据
        # 例如，可以解析JSON数据或处理表单数据
        return 'POST Request Received'

if __name__ == '__main__':
    host = '0.0.0.0'  # 服务器监听的主机
    port = 8001  # 服务器监听的端口
    
    app.run(host, port)

