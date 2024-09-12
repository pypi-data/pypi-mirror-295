import time
import json
import socket
import logging
import threading
from .interface import SocketManagerV2
# from .protocol.advanced import commonFunction as cf
from .protocol.advanced import JsonDataProtocol as api
from .WIPClientAbstractModel import WIPClientAbstractModel

class WIPClient(WIPClientAbstractModel, SocketManagerV2.SocketClient):
    # ip : 연결할 서버의 IP
    # port : 연결할 서버의 Port
    # name : 연결할 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    def __init__(self, ip="127.0.0.1", port=10008, device_id="device1", device_pw="00000000", isAutoConnect=True, live_receive=True, live_send=False, live_send_interval=1):
        super().__init__(ip, port, "WOW Iot Platform", isAutoConnect=isAutoConnect, live_receive=live_receive)
        self.device_id = str(device_id)
        self.device_pw = str(device_pw)
        self.token = ""
        self.isCertified = False

        # 각 데이터가 노드 ID로 구분되기 때문에 WIP Client에서만 사용한다.
        self.live_send = live_send
        self.live_send_run = False
        self.live_send_interval = live_send_interval
        self.socketSendThread = None
        self.sendDataQueues = {}

        self.is_wait_response = False

    # 서버 자동 접속 쓰레드 호출 시 사용되는 함수 (필요 시 사용자 정의)
    def _connectToServer(self):
        certify_check_time = time.time()
        print("[" + self.log_title + "] Connecting to {0}:{1}...".format(self.ip, self.port))
        while(self.socketConnectThread_Enable):
            try:
                # 한 번 서버에 연결되면 연결이 끊어지기 전까지 더 이상 접속을 시도하지 않도록 함
                if(not self.ser_socket_connect_status):
                    self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    self.ser_socket.connect((self.ip, self.port))
                    self.ser_socket_connect_status = True

                    # 서버 로그인 진행
                    login_json, cmd = api.dev_login_001(self.device_id, self.device_pw)
                    # print("[" + self.log_title + "] Authentication Request => {0}\n".format(login_json))
                    self.ser_socket.send(login_json.encode("utf-8"))
                    self.is_wait_response = True

                    # self.ser_socket.send("{0},{1},{2}\n".format(self.device_id, self.device_pw, "S100").encode("utf-8"))

                    # URL로부터 이미지를 읽어들일 경우 (영상 지연 문제로 쓰레드를 별도로 만들어 아래와 같이 비동기로 읽어들임)
                    if(self.live_receive):
                        self.live_receive_run = True
                        self.receiveDataQueue.clear()
                        self.socketReceiveThread = threading.Thread(target=self._receiveThread)
                        self.socketReceiveThread.setDaemon(True)
                        self.socketReceiveThread.start()

                    if(self.live_send):
                        self.live_send_run = True
                        self.socketSendThread = threading.Thread(target=self._sendThread)
                        self.socketSendThread.setDaemon(True)
                        self.socketSendThread.start()

                    print("[" + self.log_title + "] Server connection was successful.")
                    certify_check_time = time.time() # 인증 체크 시간 초기화

                # 접속 후 5초 넘게 인증이 완료되지 않았을 경우 재요청
                elif (time.time() - certify_check_time >= 5) and not self.isCertified:
                    certify_check_time = time.time()
                    print("[" + self.log_title + "] Not certified long time. retry")
                    login_json, cmd = api.dev_login_001(self.device_id, self.device_pw)
                    print("[" + self.log_title + "] Authentication Request => {0}\n".format(login_json))
                    self.ser_socket.send(login_json.encode("utf-8"))
                    self.is_wait_response = True
                    # self.ser_socket.send("{0},{1},{2}\n".format(self.device_id, self.device_pw, "S100").encode("utf-8"))

            except socket.error as e:
                print("[" + self.log_title + "] Connect to server process error " + str(e))
                self.close()
                continue

            finally:
                time.sleep(1.5)

    # 소켓 서버에 IoT 데이터 전송
    def sendData(self, values):
        try:
            if(type(values) != list):
                print("[" + self.log_title + "] Invalid data format ({0})".format(value))
                return
            if(type(values[0]) != list):
                values = [values] # to 2d array
            
            dataList = []
            for value in values:
                if(type(value) != list or len(value) != 3):
                    print("[" + self.log_title + "] Invalid data format ({0})".format(value))
                    continue
                if(value[1] not in ["CS", "CN", "SS", "SN"]):
                    print("[" + self.log_title + "] Invalid data type. ({0})".format(value[1]))
                    continue
                value_final = api.node_data(value[0], value[1], value[2])
                dataList.append(value_final)

                if(self.live_send):
                    if(self.live_send_run and self.socketSendThread.is_alive()):
                        self.sendDataQueues[value[0]] = value_final
                    # else:
                    #     print("[" + self.log_title + "] {0}:{1} The connection with the socket has been terminated or closed. Data cannot be sent.".format(self.ip, self.port))
            if(not self.live_send):
                data_json, cmd = api.dev_data_001(self.token, dataList)
                self.ser_socket.send(data_json.encode('utf-8'))
                self.is_wait_response = True

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

    # 소켓 서버에 IoT 데이터 전송
    def sendDataDirect(self, values):
        try:
            if(type(values) != list):
                print("[" + self.log_title + "] Invalid data format ({0})".format(value))
                return
            if(type(values[0]) != list):
                values = [values] # to 2d array
            
            dataList = []
            for value in values:
                if(type(value) != list or len(value) != 3):
                    print("[" + self.log_title + "] Invalid data format ({0})".format(value))
                    continue
                if(value[1] not in ["CS", "CN", "SS", "SN"]):
                    print("[" + self.log_title + "] Invalid data type. ({0})".format(value[1]))
                    continue
                value_final = api.node_data(value[0], value[1], value[2])
                dataList.append(value_final)

            data_json, cmd = api.dev_data_001(self.token, dataList)
            self.ser_socket.send(data_json.encode('utf-8'))
            self.is_wait_response = True

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

    def _sendThread(self):
        send_interval_time = 0
        self_break = False

        while(self.live_send_run):
            try:
                if time.time() - send_interval_time >= self.live_send_interval:
                    send_interval_time = time.time()
                    # 인증 된 상태인지 확인한다.
                    if self.checkCertified() and len(self.sendDataQueues) > 0:
                        data_json, cmd = api.dev_data_001(self.token, list(self.sendDataQueues.values()))
                        self.ser_socket.send(data_json.encode('utf-8'))
                        self.is_wait_response = True
                        time.sleep(0.05)

            except Exception as e:
                self.live_send_run = False
                print("[" + self.log_title + "] Problem processing data in _sendThread. => ", e)
                break

            finally:
                time.sleep(0.01)

    # 데이터 자동 수신 쓰레드 호출 시 사용되는 함수 (사용자 정의)
    def _receiveThread(self):
        data = ""
        while(self.live_receive_run):
            try:
                data += self.ser_socket.recv(self.receiveBuffer).decode('utf-8')
                if data is not None:
                    if not (len(data) == 0):
                        packets = data.split('\n')
                        # 마지막 항목은 제외
                        for i in range(len(packets) - 1):
                            if len(packets[i]) > 5: # 못해도 5는 넘어야 정상적인 데이터 "A,B,C"
                                data_str = packets[i].strip()
                                try:
                                    self.json_data = json.loads(data_str)
                                except Exception as e: # JSON Load FAIL
                                    continue

                                try:
                                    # 받은 JSON 데이터의 cmd 항목 가져오기
                                    cmd = self.json_data["cmd"]

                                    if (
                                            self.is_wait_response and
                                            (
                                                    cmd == api.CMD_LOGIN01 or
                                                    cmd == api.CMD_DDATA01
                                            )
                                    ):
                                        self.is_wait_response = False
                                        # LOGIN
                                        if(cmd == api.CMD_LOGIN01):
                                            if(
                                                (self.json_data['result'] == api.RESULT_CODE_SUCCESS) and
                                                (self.json_data['device_id'] == self.device_id)
                                                ):
                                                self.token = self.json_data['token']
                                                self.isCertified = True
                                                
                                    elif (
                                            cmd == api.CMD_HB or
                                            cmd == api.CMD_CONTROL01
                                    ):
                                        # HB
                                        if cmd == api.CMD_HB:
                                            j, cmd = api.sv_hb_001(self.token, api.RESULT_CODE_SUCCESS)
                                            self.ser_socket.send(j.encode('utf-8'))

                                        # Control
                                        elif cmd == api.CMD_CONTROL01:
                                            j, cmd = api.sv_ctrl_001(self.token, api.RESULT_CODE_SUCCESS)
                                            self.ser_socket.send(j.encode('utf-8'))
                                            if(self.token == self.json_data['token']):
                                                nodes = self.json_data['data']
                                                for node in nodes:
                                                    self.receiveDataQueue.append([node['node_id'], node['node_type'], node['node_data']])

                                except Exception as e:
                                    # cf.gLog.info("json process error =? %s", e)
                                    pass
                                finally:
                                    pass

                        # for문을 다 돌았으면, 마지막 하나는 '' 또는 '남은데이터' 이다.
                        # data를 packets의 마지막 데이터로 적용하고, 뒤에 데이터 수신 시 쌓을 수 있도록 한다.
                        data = packets[-1]

                    else:
                        print("[" + self.log_title + "] Disconnect from", str(self.getServerIP()))
                        self.close()
                        break

            except ConnectionResetError:
                self.close()
                break
            except socket.timeout as e:
                pass
            except socket.error as e:
                self.close()
                break
            finally:
                time.sleep(0.01)

    # 소켓 서버로부터 데이터 수신 (사용자 정의)
    # 만약 live_receive가 true인 경우 백그라운드에서 실행된 수신 쓰레드에서 넣은 큐를 접근
    # 만약 live_receive가 false인 경우 None 리턴
    def receiveData(self):
        data = ""
        try:
            if(self.live_receive):
                if(self.live_receive_run and self.socketReceiveThread.is_alive()):
                    data = self.receiveDataQueue.popleft() if self.receiveDataQueue else None
                else:
                    print("The connection with the socket has been terminated. A value of None is returned.")
                    data = None
                return data
            else:
                return None
        except ConnectionResetError:
            self.close()
            return None
        except socket.error as e:
            self.close()
            return None
        except Exception as e:
            return None

    def checkCertified(self):
        return self.isCertified

    def isExistReceiveData(self):
        return len(self.receiveDataQueue) > 0

    def waitForConnect(self):
        while(self.socketConnectThread_Enable and not self.checkConnected()):
            time.sleep(0.5)
