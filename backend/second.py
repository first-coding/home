import re
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8000))
server_socket.listen()

def parse_request(data):
    lines = data.splitlines()
    request_line = lines[0]
    request_header = lines[1:]
    
    # 解析请求行
    match = re.match(rb'(\w+) (\S+) HTTP/(\d\.\d)', request_line)
    method = match.group(1)
    path = match.group(2)
    version = match.group(3)

    return {
        'method': method,
        'path': path,
        'version': version
    }

while True:
    client_socket, client_address = server_socket.accept()
    request_data = client_socket.recv(1024)
    
    # 解析请求
    request = parse_request(request_data)
    
    print(request)
    
    client_socket.close()

server_socket.close()