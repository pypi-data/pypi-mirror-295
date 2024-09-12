import os
import sys
import json
import time
import threading
from socketserver import ThreadingMixIn
from urllib.parse import urlparse, parse_qs, unquote

# 파이썬 버전을 Tuple 형태로 가져옴
def getPythonVersion():
    return sys.version_info[:3]

if getPythonVersion()[0] == 3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
            
class HTTPWebServer:
    # ip : 서버의 IP (기본값 : 0.0.0.0, IP 상관 없이 접속 가능)
    # port : 서버의 Port
    # name : 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    # isAutoConnect : SocketClient 클래스를 만들고 바로 접속을 시도할 지 여부
    # live_receive : 클라이언트가 연결되면 쓰레드를 통해 주기적으로 데이터를 읽어들이고 callback을 호출하도록 할 지 여부
    # max_connect_count : 클라이언트를 최대 몇 개까지 연결할 수 있는 지 (None이면 무한)
    def __init__(self, ip="0.0.0.0", port=8080, name="HTTP"):
        self.ip = ip
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + "Server Manager"

        # HTTP 서버 실행 여부
        self.isRunning = False

        # HTTP Handler
        class HTTPWebServer_Handler(BaseHTTPRequestHandler):
            streamPath = "/"
            streamPathInfo = {}
            isRunning = True

            # # ex)
            # streamPathInfo = {
            #     ("/", "GET") : {
            #         "header": {
            #             "Content-type": "text/html; charset=utf-8",
            #         },
            #         "response_data": (200, "Hello World!"),
            #     }
            # }

            def log_message(self, format, *args):
                pass
            
            def do_GET(self):
                try:
                    # URL 경로 (뒤에 붙은 파라미터 값 제외)
                    url = urlparse(self.path).path
                    # 파라미터값
                    paramater_string = urlparse(self.path).query
                    paramater_json = parse_qs(paramater_string)

                    # 파라미터값이 여러 개 붙으면 제일 첫 번째 것을 가져오도록 함
                    paramater_json = {k: v[0] for k, v in paramater_json.items()}
                    # 경로 탐색
                    for ((path, protocol), content) in self.streamPathInfo.items():
                        if url == path and url != "/404" and protocol.upper() == "GET":
                            # 함수 형태인 경우, 파라미터 값을 인자로 주어 결과 및 응답 코드를 반환함
                            if(callable(content["response_data"])):
                                r = content["response_data"](paramater_json)
                                if(r is None): return
                                response_code = r[0]
                                response_text = r[1]
                            elif(type(content["response_data"]) in [list, tuple]):
                                response_code = content["response_data"][0]
                                response_text = content["response_data"][1]
                            else:
                                response_code = 200
                                response_text = content["response_data"]

                            # 응답 코드
                            self.send_response(response_code)

                            # 헤더 추가
                            for k, v in content["header"].items():
                                self.send_header(k, v)
                            self.end_headers()

                            # 본문 내용
                            if(type(response_text) is dict):
                                body_data = json.dumps(response_text).encode()
                            else:
                                body_data = str(response_text).encode()

                            self.wfile.write( body_data )
                            return

                    # 경로가 없는 경우
                    if(("/404", "GET") in self.streamPathInfo.keys()):
                        content = self.streamPathInfo[("/404", "GET")]
                        if(callable(content["response_data"])):
                            r = content["response_data"](paramater_json)
                            if(r is None): return
                            response_code = r[0]
                            response_text = r[1]
                        elif(type(content["response_data"]) in [list, tuple]):
                            response_code = content["response_data"][0]
                            response_text = content["response_data"][1]
                        else:
                            response_code = 200
                            response_text = content["response_data"]

                        self.send_response(response_code)
                        for k, v in content["header"].items():
                            self.send_header(k, v)
                        self.end_headers()
                        if(type(response_text) is dict):
                            body_data = json.dumps(response_text).encode()
                        else:
                            body_data = str(response_text).encode()
                        self.wfile.write( body_data )

                except (ConnectionResetError, ConnectionAbortedError) as e:
                    pass

            def do_POST(self):
                try:
                    # URL 경로 (뒤에 붙은 파라미터 값 제외)
                    url = urlparse(self.path).path
                    # 파라미터값
                    paramater_string = self.rfile.read(int(self.headers['Content-Length'])).decode()
                    paramater_json = parse_qs(paramater_string)

                    # 파라미터값이 여러 개 붙으면 제일 첫 번째 것을 가져오도록 함
                    paramater_json = {k: v[0] for k, v in paramater_json.items()}
                    # 경로 탐색
                    for ((path, protocol), content) in self.streamPathInfo.items():
                        if url == path and url != "/404" and protocol.upper() == "POST":
                            # 함수 형태인 경우, 파라미터 값을 인자로 주어 결과 및 응답 코드를 반환함
                            if(callable(content["response_data"])):
                                r = content["response_data"](paramater_json)
                                if(r is None): return
                                response_code = r[0]
                                response_text = r[1]
                            elif(type(content["response_data"]) in [list, tuple]):
                                response_code = content["response_data"][0]
                                response_text = content["response_data"][1]
                            else:
                                response_code = 200
                                response_text = content["response_data"]

                            # 응답 코드
                            self.send_response(response_code)

                            # 헤더 추가
                            for k, v in content["header"].items():
                                self.send_header(k, v)
                            self.end_headers()

                            # 본문 내용 (함수 형태인 경우, 파라미터 값을 인자로 주어 결과를 반환함)
                            if(type(response_text) is dict):
                                body_data = json.dumps(response_text).encode()
                            else:
                                body_data = str(response_text).encode()

                            self.wfile.write( body_data )
                            return

                    # 경로가 없는 경우
                    if(("/404", "POST") in self.streamPathInfo.keys()):
                        content = self.streamPathInfo[("/404", "GET")]
                        if(callable(content["response_data"])):
                            r = content["response_data"](paramater_json)
                            if(r is None): return
                            response_code = r[0]
                            response_text = r[1]
                        elif(type(content["response_data"]) in [list, tuple]):
                            response_code = content["response_data"][0]
                            response_text = content["response_data"][1]
                        else:
                            response_code = 200
                            response_text = content["response_data"]

                        self.send_response(response_code)
                        for k, v in content["header"].items():
                            self.send_header(k, v)
                        self.end_headers()
                        if(type(response_text) is dict):
                            body_data = json.dumps(response_text).encode()
                        else:
                            body_data = str(response_text).encode()
                        self.wfile.write( body_data )
                
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    print(e)
                    pass

            def do_PUT(self):
                try:
                    # URL 경로 (뒤에 붙은 파라미터 값 제외)
                    url = urlparse(self.path).path
                    # 파라미터값
                    paramater_string = self.rfile.read(int(self.headers['Content-Length'])).decode()
                    paramater_json = parse_qs(paramater_string)

                    # 파라미터값이 여러 개 붙으면 제일 첫 번째 것을 가져오도록 함
                    paramater_json = {k: v[0] for k, v in paramater_json.items()}
                    # 경로 탐색
                    for ((path, protocol), content) in self.streamPathInfo.items():
                        if url == path and url != "/404" and protocol.upper() == "PUT":
                            # 함수 형태인 경우, 파라미터 값을 인자로 주어 결과 및 응답 코드를 반환함
                            if(callable(content["response_data"])):
                                r = content["response_data"](paramater_json)
                                if(r is None): return
                                response_code = r[0]
                                response_text = r[1]
                            elif(type(content["response_data"]) in [list, tuple]):
                                response_code = content["response_data"][0]
                                response_text = content["response_data"][1]
                            else:
                                response_code = 200
                                response_text = content["response_data"]

                            # 응답 코드
                            self.send_response(response_code)

                            # 헤더 추가
                            for k, v in content["header"].items():
                                self.send_header(k, v)
                            self.end_headers()

                            # 본문 내용 (함수 형태인 경우, 파라미터 값을 인자로 주어 결과를 반환함)
                            if(type(response_text) is dict):
                                body_data = json.dumps(response_text).encode()
                            else:
                                body_data = str(response_text).encode()

                            self.wfile.write( body_data )
                            return

                    # 경로가 없는 경우
                    if(("/404", "POST") in self.streamPathInfo.keys()):
                        content = self.streamPathInfo[("/404", "GET")]
                        if(callable(content["response_data"])):
                            r = content["response_data"](paramater_json)
                            if(r is None): return
                            response_code = r[0]
                            response_text = r[1]
                        elif(type(content["response_data"]) in [list, tuple]):
                            response_code = content["response_data"][0]
                            response_text = content["response_data"][1]
                        else:
                            response_code = 200
                            response_text = content["response_data"]

                        self.send_response(response_code)
                        for k, v in content["header"].items():
                            self.send_header(k, v)
                        self.end_headers()
                        if(type(response_text) is dict):
                            body_data = json.dumps(response_text).encode()
                        else:
                            body_data = str(response_text).encode()
                        self.wfile.write( body_data )
                
                except (ConnectionResetError, ConnectionAbortedError) as e:
                    print(e)
                    pass

        self.handler = HTTPWebServer_Handler
        self.appendPath("/", protocol="GET", response_data=lambda d: (404, "Hi-Bready Sample WebServer"))
        self.appendPath("/404", protocol="GET", response_data=(404, "Page Not Found"))
        self.appendPath("/404", protocol="POST", response_data=(404, "Page Not Found"))

        # 여러 개의 연결을 받을 수 있도록 하기 위해 해당 클래스로 감쌈
        class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
            daemon_threads = True

        # self.httpServer = ThreadingHTTPServer((self.ip, self.port), self.handler)
        self.httpServer = ThreadingHTTPServer((self.ip, self.port), self.handler)

    # HTTP 서버 포트 설정
    def setPort(self, port):
        self.port = port

    # HTTP Server 시작
    def start(self):
        if(not self.isRunning):
            self.httpServer_thread = threading.Thread(target=self.httpServer.serve_forever)
            self.httpServer_thread.daemon = True
            self.httpServer_thread.start()
            self.isRunning = True

            print("[" + self.log_title + " Setting]")
            print("Server IP : " + str(self.ip))
            print("Server Port : " + str(self.port))
            print()
        
    # HTTP Server 종료
    def stop(self):
        if(self.isRunning):
            # 파이썬 httpServer에서는 shutdown 함수 호출 시 바로 종료되지 않는다.
            # shutdown 요청 후 적어도 한 번 이상 접속 요청이 있어야 종료 작업에 들어간다.
            self.httpServer.shutdown()
            self.isRunning = False
            self.handler.isRunning = False
    
    # HTTP Server Path 정보 추가
    def appendPath(self, path, protocol="GET", header={"Content-type": "text/html; charset=utf-8"}, response_data=(lambda d: (200, "Hello World!"))):
        streamPath = str(path)
        if(streamPath == ""):
            return
        if(streamPath[0] != "/"):
            streamPath = "/" + streamPath
        
        self.handler.streamPathInfo[(streamPath, protocol)] = {
            "header": header,
            "response_data": response_data,
        }

    # HTTP 정보 출력
    def printInformation(self):
        for k, v in self.handler.streamPathInfo.items():
            print("{0}: {1}".format(k, v))

