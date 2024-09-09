#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" 简易http服务端 """

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class RequestHandler(BaseHTTPRequestHandler):

    def _set_init(self):
        # 请求信息
        self.req_type = self.command
        self.req_url = urlparse(self.path)
        self.req_path = self.req_url.path
        self.req_params = parse_qs(self.req_url.query)
        self.req_data = {}

        if self.req_type in ['POST']:
            self.req_data = json.loads(self.rfile.read(int(self.headers['content-length'])))

        # 响应信息
        self.rsp_code: int = 200
        self.rsp_data: dict = {}

    def _set_rsp(self):
        self.send_response(self.rsp_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.rsp_data, ensure_ascii=False).encode())

    def do_GET(self):
        self._set_init()
        self.handle_get()
        self._set_rsp()

    def do_POST(self):
        self._set_init()
        self.handle_post()
        self._set_rsp()

    def _set_rsp_demo(self):
        self.rsp_data = {
            "return_code": "200",
            "return_info": "处理成功",
            'req_type': self.req_type,
            'req_path': self.req_path,
            'req_params': self.req_params,
            'req_data': self.req_data,
        }

    def handle_get(self):
        """ 用于重写, 处理GET请求, 生成响应 """

        self._set_rsp_demo()

    def handle_post(self):
        """ 用于重写, 处理POST请求, 生成响应 """

        self._set_rsp_demo()


def run_server(addr: str = 'localhost', port: int = 8080, handler=RequestHandler):
    """ 启动简易http服务端 """

    my_server = HTTPServer((addr, port), handler)
    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        pass
    my_server.server_close()
