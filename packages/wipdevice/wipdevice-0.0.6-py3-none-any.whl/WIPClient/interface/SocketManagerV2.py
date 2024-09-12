import socket
import threading
import time
import traceback
from collections import deque

class SocketServer:
    # ip : 서버의 IP (기본값 : 0.0.0.0, IP 상관 없이 접속 가능)
    # port : 서버의 Port
    # name : 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    # isAutoConnect : SocketClient 클래스를 만들고 바로 접속을 시도할 지 여부
    # live_receive : 클라이언트가 연결되면 쓰레드를 통해 주기적으로 데이터를 읽어들이고 callback을 호출하도록 할 지 여부
    # max_connect_count : 클라이언트를 최대 몇 개까지 연결할 수 있는 지 (None이면 무한)
    def __init__(self, ip="0.0.0.0", port=9010, name="", receiveBuffer=4096, isAutoConnect=False, live_receive=False, max_connect_count=None):
        self.ip = ip
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + "Server Manager"
        self.receiveBuffer = receiveBuffer

        self.isAutoConnect = isAutoConnect
        self.live_receive = live_receive
        self.max_connect_count = max_connect_count

        # 클라이언트 번호 (먼저 접속된 순서부터 0번이 된다.)
        self.client_id = 0

        # 클라이언트 목록 (key 값은 client_id가 된다.)
        self.clients = {}

        # 클라이언트가 연결되었을 때 실시간으로 데이터를 수신받기 위한 쓰레드로,
        # 접속될 수 있는 클라이언트가 여러 개일 수도 있기 때문에 dict 형식으로 처리한다.
        # (key 값을 client_id가 된다.)
        self.receivedDataThreads = {}

        print("[" + self.log_title + " Setting]")
        print("Server IP : " + self.ip)
        print("Server Port : " + str(port))
        print()

        # self.ser_socket_autoconnect_is_try : 서버 접속에 대해 중복 호출을 방지하는 용도
        # self.ser_socket_connect_status : 현재 서버에 연결되었는 지 여부
        self.ser_socket_autoconnect_is_try = False
        self.ser_socket_connect_status = False

        # 서버 개방 쓰레드
        self.socketConnectThread = threading.Thread(target=self._connectFromServer)
        self.socketConnectThread_Enable = False
        
        # 서버 소켓
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if(self.isAutoConnect):
            self.startAutoConnect()
        
        self.live_receive_run = {}
        self.receiveDataQueue = {}

    # 서버 열기
    def startAutoConnect(self):
        # 중복 접속 방지
        if(self.ser_socket_autoconnect_is_try):
            return

        self.ser_socket_autoconnect_is_try = True
        self.socketConnectThread_Enable = False

        # 기존의 연결 시도 작업이 종료될 때까지 대기
        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass
    
        self.socketConnectThread_Enable = True
        self.socketConnectThread = threading.Thread(target=self._connectFromServer)
        self.socketConnectThread.setDaemon(True)
        self.socketConnectThread.start()
    
    # 서버 종료
    def stopAutoConnect(self):
        self.ser_socket_autoconnect_is_try = False
        self.socketConnectThread_Enable = False

        # 기존의 연결 시도 작업이 종료될 때까지 대기
        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass
    
    # 클라이언트 연결 수락 쓰레드 호출 시 사용되는 함수 (필요 시 사용자 정의)
    def _connectFromServer(self):
        print("[" + self.log_title + "] Waiting for client connection from {0}:{1}...".format(self.ip, self.port))
        while(self.socketConnectThread_Enable):
            try:
                # 한 번 서버에 연결되면 연결이 끊어지기 전까지 더 이상 접속을 시도하지 않도록 함
                if(not self.ser_socket_connect_status):
                    self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.ser_socket.bind((self.ip, self.port))
                    self.ser_socket_connect_status = True
                
                if(self.max_connect_count is None or self.max_connect_count > len(self.clients)):
                    # 클라이언트 소켓 연결 대기 (listen은 연결 요청 큐의 수)
                    # 연결이 대기되는 동안 계속 blocking되니 참고
                    self.ser_socket.listen(1)

                    # 클라이언트 연결 성공 시 client 소켓과 연결 정보를 받는다.
                    client_socket, client_address = self.ser_socket.accept()

                    # client_id를 키값으로 하여 리스트에 추가
                    self.clients[self.client_id] = client_socket
                    self.live_receive_run[self.client_id] = False
                    self.receivedDataThreads[self.client_id] = None
                    self.receiveDataQueue[self.client_id] = deque(maxlen=None)

                    # live_receive 옵션이 켜져있으면 쓰레드를 하나 만들어서 데이터를 자동으로 수신하도록 한다.
                    if(self.live_receive):
                        self.live_receive_run[self.client_id] = True
                        receiveDataThread = threading.Thread(target=self._receiveThread, args=(self.client_id,))
                        receiveDataThread.setDaemon(True)
                        receiveDataThread.start()
                        self.receivedDataThreads[self.client_id] = receiveDataThread
                    
                    self.client_id += 1

                    print("[{0}] The client is connected. ({1})".format(self.log_title, client_address))
                else:
                    pass

            except socket.error as e:
                print(e)
                continue
            finally:
                time.sleep(0.1)
    
    # 모든 클라이언트 소켓에 데이터 송신 (사용자 정의)
    def sendData(self, message, client_id=None):
        if(client_id is None):
            for socket_client in list(self.clients.values()):
                try:
                    socket_client.send(message.encode('utf-8'))
                except ConnectionResetError:
                    pass
                # client socket close는 receiveData 함수를 사용하는 쓰레드에서 관리하므로 여기서는 pass를 준다.
                except socket.error:
                    pass
        else:
            try:
                if(self.checkClientID(client_id)):
                    self.clients[client_id].send(message.encode('utf-8'))
            except ConnectionResetError:
                pass
            # client socket close는 receiveData 함수를 사용하는 쓰레드에서 관리하므로 여기서는 pass를 준다.
            except socket.error:
                pass

    # 클라이언트로부터 데이터를 자동으로 수신받는 쓰레드 호출 시 사용되는 함수 (사용자 정의)
    def _receiveThread(self, client_id):
        while(self.live_receive_run[client_id]):
            try:
                data = self.clients[client_id].recv(self.receiveBuffer)
                if data is not None:
                    if not (len(data) == 0):
                        self.receiveDataQueue[client_id].append(data.decode())
                    else:
                        print("[" + self.log_title + "] Disconnect from", str(self.getServerIP()))
                        self.close_client(client_id)
                        del self.clients[client_id]
                        break

            except ConnectionResetError:
                self.close_client(client_id)
                break # server에서는 client 소켓이 닫혀있으면 recv 할 때 데이터가 0이 들어오는 게 아닌, 무조건 예외가 발생하게 됨
            except socket.error as e:
                self.close_client(client_id)
                break
            finally:
                time.sleep(0.01)
        
        self.live_receive_run[client_id] = False

    # 클라이언트 소켓으로부터 데이터 수신 (사용자 정의)
    def receiveData(self, client_id):
        try:
            if(self.live_receive):
                if(self.live_receive_run[client_id] and self.receivedDataThreads[client_id].is_alive()):
                    data = self.receiveDataQueue[client_id].popleft() if self.receiveDataQueue[client_id] else None
                else:
                    print("{0} client socket has been terminated. A value of None is returned.".format(client_socket.getpeername()[0]))
                    data = None
            else:
                data = self.clients[client_id].recv(self.receiveBuffer)
                if data is not None and len(data) == 0:
                    print("disconnect..from " + str(self.clients[client_id].getpeername()[0]))
                    self.close_client(client_id)
                    del self.clients[client_id]
            
            return data

        except ConnectionResetError:
            self.close_client(client_id)
            return None
        except socket.error:
            self.close_client(client_id)
            return None
        except Exception as e:
            return None

    # 클라이언트 연결 대기 상태 확인
    def checkListening(self):
        return self.ser_socket_connect_status
    
    # 서버의 IP 가져오기
    def getServerIP(self):
        return self.ip
    
    # 서버의 Port 가져오기
    def getServerPort(self):
        return self.port
    
    # 서버 Port 변경 (단, 현재 소켓 서버 연결 혹은 시도 중인 경우 이를 차단합니다.)
    def setServerPort(self, port):
        self.port = port
        self.close()

    # 연결된 클라이언트 ID 목록 가져오기
    def getClientIDs(self):
        return list(self.clients.keys())

    # 연결된 클라이언트 수 가져오기
    def getClientCount(self):
        return len(self.clients)

    # 연결된 클라이언트 중에 해당 ID를 가지는 클라이언트가 있는 지 여부
    def checkClientID(self, client_id):
        return client_id in self.clients.keys()
    
    # 클라이언트 닫기
    def close_client(self, client_id):
        self.live_receive_run[client_id] = False
        if(self.checkClientID(client_id)):
            self.clients[client_id].close()
            del self.clients[client_id]
    
    # 서버 닫기
    def close(self):
        if(self.ser_socket_connect_status):
            for client_id in list(self.clients.keys()):
                self.close_client(client_id)
            self.clients.clear()
            self.ser_socket.close()
            self.ser_socket_connect_status = False
            print("[" + self.log_title + "] The server has been shut down.")
            self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 자원 할당 해제
    def dispose(self):
        # 자동 연결 해제
        self.ser_socket_autoconnect_is_try = False
        self.socketConnectThread_Enable = False
        self.close() # server socket의 listen 함수에서 계속 대기하고 있기 때문에 먼저 끊어주어야 한다.

        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass

        # # 실시간 데이터 수신 해제
        # for client_id in self.clients.keys():
        #     while(self.live_receive_run[client_id] or self.self.receivedDataThreads[client_id].is_alive()):
        #         time.sleep(1)


class SocketClient:
    # ip : 연결할 서버의 IP
    # port : 연결할 서버의 Port
    # name : 연결할 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    # isAutoConnect : SocketClient 클래스를 만들고 바로 접속을 시도할 지 여부
    # live_receive : 서버 연결 후 쓰레드를 통해 주기적으로 데이터를 읽어들이고 callback을 호출하도록 할 지 여부
    def __init__(self, ip="127.0.0.1", port=10004, name="", receiveBuffer=4096, isAutoConnect=False, live_receive=False):
        self.ip = ip
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + "Client Manager"
        self.receiveBuffer = receiveBuffer

        self.isAutoConnect = isAutoConnect
        self.live_receive = live_receive

        # 서버로 연결되었을 때 클라이언트에서 실시간으로 데이터를 수신받기 위한 쓰레드
        self.socketReceiveThread = None

        print("[" + self.log_title + " Setting]")
        print("Server IP : " + ip)
        print("Server Port : " + str(port))
        print()

        # self.ser_socket_autoconnect_status : 자동 접속 쓰레드를 계속 사용할 지 여부
        # self.ser_socket_autoconnect_is_try : 서버 접속에 대해 중복 호출을 방지하는 용도
        # self.ser_socket_connect_status : 현재 서버에 연결되었는 지 여부
        self.ser_socket_autoconnect_status = False
        self.ser_socket_autoconnect_is_try = False
        self.ser_socket_connect_status = False

        # 서버 접속 쓰레드
        self.socketConnectThread = threading.Thread(target=self._connectToServer)
        self.socketConnectThread_Enable = False

        # 서버 소켓
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        if(self.isAutoConnect):
            self.startAutoConnect()

        self.live_receive_run = False
        self.receiveDataQueue = deque(maxlen=None)


        # # live_receive 옵션이 활성화된 경우 데이터 수신을 쓰레드로 받음
        # self.live_receive_run = live_receive
        # self.receiveDataQueue = deque(maxlen=None)
        # if(self.live_receive):
        #     self.socketReceiveThread = threading.Thread(target=self._receiveThread)
        #     self.socketReceiveThread.daemon = True
        #     self.socketReceiveThread.start()


    # 서버에 자동 접속 시작
    def startAutoConnect(self):
        # 중복 접속 방지
        if(self.ser_socket_autoconnect_is_try):
            return

        self.ser_socket_autoconnect_is_try = True
        self.socketConnectThread_Enable = False

        # 기존의 연결 시도 작업이 종료될 때까지 대기
        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass
    
        self.socketConnectThread_Enable = True
        self.socketConnectThread = threading.Thread(target=self._connectToServer)
        self.socketConnectThread.setDaemon(True)
        self.socketConnectThread.start()

    # 서버에 자동 접속 중지
    def stopAutoConnect(self):
        self.ser_socket_autoconnect_is_try = False
        self.socketConnectThread_Enable = False

        # 기존의 연결 시도 작업이 종료될 때까지 대기
        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass

    # 서버 자동 접속 쓰레드 호출 시 사용되는 함수 (필요 시 사용자 정의)
    def _connectToServer(self):
        print("[" + self.log_title + "] Connecting to {0}:{1}...".format(self.ip, self.port))
        while(self.socketConnectThread_Enable):
            try:
                # 한 번 서버에 연결되면 연결이 끊어지기 전까지 더 이상 접속을 시도하지 않도록 함
                if(not self.ser_socket_connect_status):
                    self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.ser_socket.connect((self.ip, self.port))
                    self.ser_socket_connect_status = True

                    # URL로부터 이미지를 읽어들일 경우 (영상 지연 문제로 쓰레드를 별도로 만들어 아래와 같이 비동기로 읽어들임)
                    if(self.live_receive):
                        self.live_receive_run = True
                        self.receiveDataQueue.clear()
                        self.socketReceiveThread = threading.Thread(target=self._receiveThread)
                        self.socketReceiveThread.daemon = True
                        self.socketReceiveThread.start()

                    print("[" + self.log_title + "] Server connection was successful.")
            except socket.error as e:
                print(e)
                continue
            finally:
                time.sleep(0.1)
    
    # 소켓 서버에 데이터 송신 (사용자 정의)
    def sendData(self, value):
        try:
            if(type(value) not in [str, bytes, int]):
                print("[" + self.log_title + "] Invalid data type. ({0})".format(type(value)))
                return
            
            if(type(value) in [str, int]):
                value = str(value).encode('utf-8')

            self.ser_socket.send(value)

        except ConnectionResetError:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip, self.port))
            pass
        except socket.error as e:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip, self.port))
            pass
        finally:
            pass

    # 데이터 자동 수신 쓰레드 호출 시 사용되는 함수 (사용자 정의)
    def _receiveThread(self):
        while(self.live_receive_run):
            try:
                data = self.ser_socket.recv(self.receiveBuffer)
                if data is not None:
                    if not (len(data) == 0):
                        self.receiveDataQueue.append(data.decode())
                    else:
                        print("disconnect..from " + str(self.getServerIP()))
                        self.close()
                        break

            except ConnectionResetError:
                self.close()
            except socket.error as e:
                self.close()
            finally:
                time.sleep(0.01)
        
        self.live_receive_run = False

    # 소켓 서버로부터 데이터 수신 (사용자 정의)
    def receiveData(self):
        try:
            if(self.live_receive):
                if(self.live_receive_run and self.socketReceiveThread.is_alive()):
                    data = self.receiveDataQueue.popleft() if self.receiveDataQueue else None
                else:
                    print("The connection with the socket has been terminated. A value of None is returned.")
                    data = None
            else:
                data = self.ser_socket.recv(self.receiveBuffer)
                if data is not None and len(data) == 0:
                    print("[" + self.log_title + "] Disconnect from", str(self.getServerIP()))
                    self.close()

            return data
        
        except ConnectionResetError:
            self.close()
            return None
        except socket.error as e:
            self.close()
            return None
        except Exception as e:
            return None

    # 서버 연결 상태 확인
    def checkConnected(self):
        return self.ser_socket_connect_status
    
    # 서버의 IP 가져오기
    def getServerIP(self):
        return self.ip
    
    # 서버의 Port 가져오기
    def getServerPort(self):
        return self.port
    
    # 서버 IP 변경 (단, 현재 소켓 서버 연결 혹은 시도 중인 경우 이를 차단합니다.)
    def setServerIP(self, ip):
        self.ip = ip
        self.close()
    
    # 서버 Port 변경 (단, 현재 소켓 서버 연결 혹은 시도 중인 경우 이를 차단합니다.)
    def setServerPort(self, port):
        self.port = port
        self.close()
    
    # 서버 연결 종료 (자동 연결이 활성화되어있으면 곧바로 재접속을 시도함)
    def close(self):
        if(self.ser_socket_connect_status):
            self.ser_socket.close()
            print("[" + self.log_title + "] The connection to the server has been terminated.")
            self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ser_socket_connect_status = False

    # 자원 할당 해제
    def dispose(self):
        # 자동 연결 해제
        self.ser_socket_autoconnect_is_try = False
        self.socketConnectThread_Enable = False
        while(self.socketConnectThread.is_alive()):
            time.sleep(1)
            pass

        # 실시간 데이터 수신 해제
        self.live_receive_run = False
        while(self.live_receive_run or self.socketReceiveThread.is_alive()):
            time.sleep(1)

        self.close()
