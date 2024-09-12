import asyncio
import threading
import time

try:
    import websockets
except ModuleNotFoundError as e:
    print(e)
    print("websockets package not found. Therefore, the function cannot be used.")

class WebSocketServer:
    # port : 서버의 Port
    # name : 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    def __init__(self, port=9010, name=""):
        self.ip = "localhost"
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + " Web Socket Manager"

        self.clients = []

        print("[" + self.log_title + " Setting]")
        print("Server IP : " + self.ip)
        print("Server Port : " + str(port))
        print()
        
        self.ser_socket_is_try_connect = False

        self.socketConnectThread = threading.Thread(target=self._start_loop)

    def _start_loop(self):
        self._loop = asyncio.new_event_loop()
        self.server = websockets.serve(self.receiveData, self.ip, self.port, loop=self._loop)

        self._loop.run_until_complete(self.server)
        self._loop.run_forever()
    
    # 클라이언트 소켓으로부터 데이터 수신 (사용자 정의)
    async def receiveData(self, client_websocket, path):
        print("[" + self.log_title + "] Waiting for client connection from {0}:{1}...".format(self.ip, self.port))
        while(self.ser_socket_is_try_connect):
            try:
                data = await client_websocket.recv()
                await client_websocket.send("echo : " + data)

            except Exception as e:
                print(e)
                break
            finally:
                time.sleep(0.1)
    
    # 서버의 IP 가져오기
    def getServerIP(self):
        return self.ip
    
    # 서버의 Port 가져오기
    def getServerPort(self):
        return self.port

    # 서버 열기
    def open(self):
        if(not self.ser_socket_is_try_connect and "websockets" in globals()):
            self.ser_socket_is_try_connect = True

            # 쓰레드가 정상적으로 종료될 때까지 대기
            while(self.socketConnectThread.isAlive()):
                time.sleep(0.01)
                pass
            self.socketConnectThread = threading.Thread(target=self._start_loop)
            self.socketConnectThread.daemon = True
            self.socketConnectThread.start()

    # 서버 닫기
    def close(self):
        self.ser_socket_is_try_connect = False
        if(self._loop):
            self._loop.stop()
            self.server.ws_server.close()
            self.server.ws_server.wait_closed()

            try:
                # 강제 종료를 위해 한 번이라도 접속이 되어야 함
                async def _close_echo():
                    async with websockets.connect("ws://{0}:{1}".format(self.ip, self.port)) as websocket:
                        pass
                
                ws = asyncio.wait_for(_close_echo(), 1)
                asyncio.get_event_loop().run_until_complete(ws)
            except Exception as e:
                print(e)
                pass

            while(self._loop.is_running() or self._loop.is_closed()):
                print("[" + self.log_title + "] wait shut down...")
                time.sleep(1)

        print("[" + self.log_title + "] The server has been shut down.")
