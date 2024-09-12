import socket
import time
import threading
from .interface import SocketManagerV2
from .protocol.advanced import commonFunction as cf
from .protocol.advanced import JsonDataProtocol as api
import json
import logging

class WIPClient(SocketManagerV2.SocketClient):
    # ip : 연결할 서버의 IP
    # port : 연결할 서버의 Port
    # name : 연결할 서버를 구분하기 위한 용도 (ex: iotGateway, AutoVehicle, iotMakers .. 등등)
    def __init__(self, ip="127.0.0.1", port=10008, device_id="device1", device_pw="00000000"):
        super().__init__(ip, port, "WOW Iot Platform", isAutoConnect=True, live_receive=True)
        self.device_id = str(device_id)
        self.device_pw = str(device_pw)
        self.token = ""
        self.isCertified = False
        self.is_wait_response = False
        self.send_list_queue = {}
        self.send_lock = threading.Lock()

        self.sock_lock = threading.Lock()

    # 서버 자동 접속 쓰레드 호출 시 사용되는 함수 (필요 시 사용자 정의)
    def _connectToServer(self):
        connect_check_time = 0
        certify_check_time = time.time()
        print("[" + self.log_title + "] Connecting to {0}:{1}...".format(self.ip, self.port))
        while (self.socketConnectThread_Enable):
            try:
                # 한 번 서버에 연결되면 연결이 끊어지기 전까지 더 이상 접속을 시도하지 않도록 함
                if not self.ser_socket_connect_status:
                    if time.time() - connect_check_time >= 10:  # 10초 마다 서버 소켓 연결시도
                        cf.gLog.info("서버 연결이 끊겨 있음 확인. 소켓 연결 시도")
                        connect_check_time = time.time()
                        self.ser_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        self.ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        self.ser_socket.connect((self.ip, self.port))
                        self.ser_socket_connect_status = True

                        # URL로부터 이미지를 읽어들일 경우 (영상 지연 문제로 쓰레드를 별도로 만들어 아래와 같이 비동기로 읽어들임)
                        if (self.live_receive):
                            cf.gLog.info("수신 및 송신 쓰레드 시작")
                            self.live_receive_run = True
                            self.receiveDataQueue.clear()
                            self.socketReceiveThread = threading.Thread(target=self._receiveThread)
                            self.socketReceiveThread.daemon = True
                            self.socketReceiveThread.start()

                            self.send_thread = threading.Thread(target=self._sendThread)
                            self.send_thread.setDaemon(True)
                            self.send_thread.start()

                        login_json, cmd = api.dev_login_001(self.device_id, self.device_pw)
                        print("인증 요청 => {0}\n".format(login_json))
                        self.sock_lock.acquire()
                        self.ser_socket.send(login_json.encode("utf-8"))
                        self.is_wait_response = True
                        self.sock_lock.release()
                        certify_check_time = time.time()  # 인증 체크 시간 초기화
                        cf.gLog.info("%s", str("[" + self.log_title + "] Server connection was successful."))

                # 접속 후 5초 넘게 인증이 완료되지 않았을 경우
                elif (time.time() - certify_check_time >= 5) and not self.isCertified:
                    certify_check_time = time.time()
                    cf.gLog.info("%s", str("[" + self.log_title + "] Not certified long time. retry"))
                    self.sock_lock.acquire()
                    login_json, cmd = api.dev_login_001(self.device_id, self.device_pw)
                    print("인증 요청 => {0}\n".format(login_json))
                    self.ser_socket.send(login_json.encode("utf-8"))
                    self.is_wait_response = True
                    self.sock_lock.release()

            except socket.error as e:
                cf.gLog.error("%s", str("[" + self.log_title + "] Connect to server process error " + str(e)))
                if self.sock_lock.locked():
                    self.sock_lock.release()
                self.close()
                continue

            except Exception as _e:
                import traceback
                traceback.print_exc()
                print(111, self.device_id, self.device_pw)
                cf.gLog.error("_connectToServer 쓰레드에서 알 수 없는 에러 발생! => %s", _e)

            finally:
                time.sleep(1.5)

        cf.gLog.critical("비정상적인 원인으로 _connectToServer 쓰레드 종료됨!!")

    # 서버에 보낼 IoT데이터 저장.
    # 동일한 태그가 이미 저장되어 있을 시 데이터를 덮어 씌운다.
    # 저장된 데이터는 주기적으로 전송하며 클리어한다.
    # value는 리스트 형태로 와야 하며, [name, type, value] 가 입력되어야 한다.
    def appendSendData(self, value):
        if type(value) != list or len(value) != 3:
            print("[" + self.log_title + "] Invalid data format ({0})".format(value))
            return
        if value[1] not in ["CS", "CN", "SS", "SN"]:
            print("[" + self.log_title + "] Invalid data type. ({0})".format(value[1]))
            return

        self.send_lock.acquire()
        key = str(value[0])
        self.send_list_queue[key] = value
        self.send_lock.release()

    # 소켓 서버에 IoT 데이터 전송
    # 입력 형태는 [name, type, value] 가 입력되어야 한다.
    def sendData(self, value):
        try:
            if type(value) != list or len(value) != 3:
                print("[" + self.log_title + "] Invalid data format ({0})".format(value))
                return
            if value[1] not in ["CS", "CN", "SS", "SN"]:
                print("[" + self.log_title + "] Invalid data type. ({0})".format(value[1]))
                return

            data = [api.node_data(value[0], value[1], value[2])]
            data_json, cmd = api.dev_data_001(self.token, data)
            self.sock_lock.acquire()
            self.ser_socket.send(data_json.encode('utf-8'))
            self.is_wait_response = True
            # print(tagPacket)

        except ConnectionResetError:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        except socket.error as e:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        finally:
            if self.sock_lock.locked():
                self.sock_lock.release()

    # Array 형태의 데이터를 전송한다.
    def sendDataArray(self, values):
        try:
            if type(values) != list or (len(values) == 0):
                cf.gLog.warning("warning in sendDataArray, values is not list")
                return
            
            dataArray = []
            for value in values:
                if type(value) != list or len(value) != 3:
                    continue
                dataArray.append(api.node_data(value[0], value[1], value[2]))
            data_json, cmd = api.dev_data_001(self.token, dataArray)
            print("데이터 전송", data_json)
            self.sock_lock.acquire()
            self.ser_socket.send(data_json.encode('utf-8'))
            self.is_wait_response = True
            # print(tagPacket)

        except ConnectionResetError:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        except socket.error as e:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        finally:
            if self.sock_lock.locked():
                self.sock_lock.release()

    # 소켓으로 데이터 전송하는 메소드
    def sendSocketData(self, str):
        try:
            self.sock_lock.acquire()
            self.ser_socket.send(str.encode('utf-8'))
        except ConnectionResetError:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        except socket.error as e:
            self.close()
            print("[" + self.log_title + "] {0}:{1} The connection to the server has been lost.".format(self.ip,
                                                                                                        self.port))
        finally:
            if self.sock_lock.locked():
                self.sock_lock.release()

    def _sendThread(self):
        send_interval_time = 0
        self_break = False
        cf.gLog.info("_sendThread 쓰레드 시작됨")
        while self.live_receive_run and (not self_break):
            try:
                if time.time() - send_interval_time >= 5:
                    send_interval_time = time.time()
                    # 인증 된 상태인지 확인한다.
                    if self.checkCertified():
                        self.send_lock.acquire()
                        if len(self.send_list_queue) > 0:
                            cf.gLog.info("##### IoT 데이터 전송 시퀀스 수행 #####")
                            _values = []
                            for key, value in self.send_list_queue.items():
                                _values.append(value)

                            self.send_list_queue.clear()  # 전송이 전부 다 되었으면 큐를 클리어 한다.
                            if self.send_lock.locked():
                                self.send_lock.release()
                            
                            if len(_values) > 0:
                                self.sendDataArray(_values) # 실제 전송하는 부분
                                self.is_wait_response = True

            except Exception as e:
                self_break = True
                cf.gLog.error("_sendThread에서 데이터 처리 중 문제 발생 => %s", e)

            finally:
                if self.send_lock.locked():
                    self.send_lock.release()
                time.sleep(0.005)

        self.live_receive_run = False
        cf.gLog.info("_sendThread 종료")

    # 데이터 자동 수신 쓰레드 호출 시 사용되는 함수 (사용자 정의)
    def _receiveThread(self):
        data = ""
        cf.gLog.info("_receiveThread 쓰레드 시작됨")
        while self.live_receive_run:
            try:
                data += self.ser_socket.recv(self.receiveBuffer).decode('utf-8')
                if data is not None:
                    # 만약 data 변수 데이터 크기가 과도하게 클 경우 data 길이를 초기화한다.
                    if len(data) >= 0x7FFF:
                        data = ""
                    elif not (len(data) == 0):
                        # linefeed 기준으로 split
                        split_data = data.split('\n')
                        for jd in split_data:
                            print("receive", jd)
                            if jd == '':
                                continue
                            try:
                                self.json_data = json.loads(jd)
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
                                        self.sendSocketData(j)

                                    # Control
                                    elif cmd == api.CMD_CONTROL01:
                                        j, cmd = api.sv_ctrl_001(self.token, api.RESULT_CODE_SUCCESS)
                                        self.sendSocketData(j)
                                        if(self.token == self.json_data['token']):
                                            nodes = self.json_data['data']
                                            for node in nodes:
                                                self.receiveDataQueue.append([node['node_id'], node['node_type'], node['node_data']])

                            except Exception as e:
                                cf.gLog.info("json process error =? %s", e)
                            finally:
                                pass
                        # for문을 다 돌았으면, 마지막 하나는 '' 또는 '남은데이터' 이다.
                        # data를 packets의 마지막 데이터로 적용하고, 뒤에 데이터 수신 시 쌓을 수 있도록 한다.
                        data = split_data[len(split_data)-1]

                    else:
                        print("disconnect..from " + str(self.getServerIP()))
                        self.close()
                        break

            except ConnectionResetError:
                cf.gLog.error("ConnectionResetError occurred in _receiveData thread")
                self.live_receive_run = False
                self.close()
                break
            except socket.timeout as e:
                # cf.gLog.error("socket time out error occurred in _receiveData thread => %s", e)
                pass
            except socket.error as e:
                cf.gLog.error("socket error occurred in _receiveData thread => %s", e)
                self.live_receive_run = False
                self.close()
                break
            finally:
                time.sleep(0.01)

        cf.gLog.error("_receiveThread 쓰레드 종료됨")

    def checkCertified(self):
        return self.isCertified

    def isExistReceiveData(self):
        return len(self.receiveDataQueue) > 0

    def waitForConnect(self):
        while (self.socketConnectThread_Enable and not self.checkConnected()):
            time.sleep(0.5)


if __name__ == '__main__':
    logging_format = logging.Formatter('%(asctime)s [%(levelname)s]%(message)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging_format)

    cf.gLog.addHandler(stream_handler)

    cf.gLog.setLevel(level=logging.DEBUG)

    cf.gLog.info("START APP PROGRAM")
    
    ########################################################### IoT 처리 시퀀스 ###########################################################
    seq = 0
    seq_time = time.time()
    iot = WIPClient(ip="192.168.10.2", port=51004, device_id="TestDevice", device_pw="1234")
    while True:
        if seq == 0:
            cf.gLog.info("#### IoT Platform 접속 시작! ####")
            seq = 1
        elif seq == 1:
            if iot is not None:
                if not (iot.socketConnectThread_Enable and not iot.checkConnected()):
                    cf.gLog.info("#### IoT Platform 접속 성공! ####")
                    seq_time = time.time()
                    seq = 2

        elif seq == 2:
            if iot is not None:
                if iot.checkCertified():
                    cf.gLog.info("#### IoT Platform 인증 성공! ####")
                    seq = 3

        time.sleep(0.01)