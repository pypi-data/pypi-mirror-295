import socket
import threading
import time

class SocketServer:
    # port : 서버의 Port
    # name : 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    def __init__(self, port=9010, name="", receiveBuffer=4096):
        self.ip = "0.0.0.0"
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + "Server Manager"
        self.receiveBuffer = receiveBuffer

        self.clients = []

        print("[" + self.log_title + " Setting]")
        print("Server IP : " + self.ip)
        print("Server Port : " + str(port))
        print()

        self.ser_socket_connect_status = False
        self.ser_socket_is_try_connect = False
        self.open()

        socketConnectThread = threading.Thread(target=self._connectFromServer)
        socketConnectThread.setDaemon(True)
        socketConnectThread.start()

    # 서버 연결 시도
    def _connectFromServer(self):
        # 중복 접속 방지
        if(self.ser_socket_is_try_connect):
            return

        self.ser_socket_is_try_connect = True

        print("[" + self.log_title + "] Waiting for client connection from {0}:{1}...".format(self.ip, self.port))
        while(self.ser_socket_is_try_connect):
            try:
                # 클라이언트 소켓 연결 대기 (listen은 연결 요청 큐의 수)
                self.ser_socket.listen(1)

                # 클라이언트 연결 성공 시 client 소켓과 연결 정보를 받는다.
                client_socket, client_address = self.ser_socket.accept()

                receiveDataThread = threading.Thread(target=self.receiveData, args=(client_socket, client_address))
                receiveDataThread.setDaemon(True)
                receiveDataThread.start()

                print("[{0}] The client is connected. ({1})".format(self.log_title, client_address))

                self.clients.append(client_socket)
            except socket.error as e:
                print(e)
                continue
            finally:
                time.sleep(0.1)
        
    # 모든 클라이언트 소켓에 데이터 송신 (사용자 정의)
    def sendData(self, message, client_socket=None):
        if(client_socket is None):
            for csocket in self.clients:
                try:
                    csocket.send(message.encode('utf-8'))
                except ConnectionResetError:
                    pass
                # client socket close는 receiveData 함수를 사용하는 쓰레드에서 관리하므로 여기서는 pass를 준다.
                except socket.error:
                    pass
        else:
            try:
                client_socket.send(message.encode('utf-8'))
            except ConnectionResetError:
                pass
            # client socket close는 receiveData 함수를 사용하는 쓰레드에서 관리하므로 여기서는 pass를 준다.
            except socket.error:
                pass

    # 클라이언트 소켓으로부터 데이터 수신 (사용자 정의)
    def receiveData(self, client_socket, client_address):
        while(True):
            try:
                data = client_socket.recv(self.receiveBuffer)
                if data is not None:
                    if not (len(data) == 0):
                        data_str = data.decode('utf-8').strip()
                        # print(data_str)
                    else:
                        print("disconnect..from " + str(client_address))
                        break

            except ConnectionResetError:
                client_socket.close()
                self.clients.remove(client_socket)
                break
            except socket.error:
                client_socket.close()
                self.clients.remove(client_socket)
                break
            finally:
                time.sleep(0.01)

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
        self.close()
        self.port = port
        self.open()
    
    # 서버 열기
    def open(self):
        if(not self.ser_socket_is_try_connect):
            self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ser_socket.bind((self.ip, self.port))

    # 서버 닫기
    def close(self):
        self.ser_socket_connect_status = False
        self.ser_socket.close()

        print("[" + self.log_title + "] The server has been shut down.")


class SocketClient:
    # ip : 연결할 서버의 IP
    # port : 연결할 서버의 Port
    # name : 연결할 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    def __init__(self, ip="127.0.0.1", port=10004, name="", receiveBuffer=4096):
        self.ip = ip
        self.port = port
        self.name = name if name == "" else name + " "
        self.log_title = self.name + "Client Manager"
        self.receiveBuffer = receiveBuffer

        print("[" + self.log_title + " Setting]")
        print("Server IP : " + ip)
        print("Server Port : " + str(port))
        print()

        self.ser_socket_connect_status = False
        self.ser_socket_is_try_connect = False
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socketConnectThread = threading.Thread(target=self._connectToServer)
        socketConnectThread.setDaemon(True)
        socketConnectThread.start()

        receiveDataThread = threading.Thread(target=self.receiveData)
        receiveDataThread.setDaemon(True)
        receiveDataThread.start()

    # 서버 연결 시도
    def _connectToServer(self):
        # 중복 접속 방지
        if(self.ser_socket_is_try_connect):
            return

        self.ser_socket_is_try_connect = True

        print("[" + self.log_title + "] Connecting to {0}:{1}...".format(self.ip, self.port))
        while(self.ser_socket_is_try_connect):
            try:
                if(not self.ser_socket_connect_status):
                    self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.ser_socket.connect((self.ip, self.port))
                    self.ser_socket_connect_status = True
                    print("[" + self.log_title + "] Server connection was successful.")
            except socket.error as e:
                continue
            finally:
                time.sleep(0.1)

    # 소켓 서버에 데이터 송신 (사용자 정의)
    def sendData(self):
        pass

    # 소켓 서버로부터 데이터 수신 (사용자 정의)
    def receiveData(self):
        pass

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
        self.close()
        self.ip = ip
    
    # 서버 Port 변경 (단, 현재 소켓 서버 연결 혹은 시도 중인 경우 이를 차단합니다.)
    def setServerPort(self, port):
        self.close()
        self.port = port
    
    # 서버 연결 종료
    def close(self):
        if(self.ser_socket_connect_status):
            self.ser_socket.close()
            self.ser_socket_connect_status = False
            print("[" + self.log_title + "] The connection to the server has been terminated.")
        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def disconnect(self):
        self.ser_socket_is_try_connect = False
