from .WIPClient import WIPClient as WIPClient_edu
from .WIPClient_advance import WIPClient as WIPClient_advanced
from .WIPClientAbstractModel import WIPClientAbstractModel

class WIPDevice(WIPClientAbstractModel):
	"""
	@brief 생성자
	@param ip Server IP
	@param port Server Port
	@param device_id Device ID
	@param device_pw Device PW
	@param isAutoConnect 자동 접속 관련 boolean. True일 경우 연결이 끊길 시 자동으로 접속한다.
	@param live_receive 자동으로 수신관련 처리를 수행할지 여부
	@param live_send 데이터를 자동으로 전송할지 여부
	@param live_send_interval live_send가 True일 경우 전송할 주기
	"""
	def __init__(self, ip="127.0.0.1", port=10008, use_advanced_protocol=True, device_id="device1", device_pw="00000000", isAutoConnect=True, live_receive=True, live_send=False, live_send_interval=1):
		self.mWIPClient = None

		if use_advanced_protocol:
			self.mWIPClient = WIPClient_advanced(ip, port, device_id, device_pw, isAutoConnect, live_receive, live_send, live_send_interval)
		else:
			print("WIP Device init on education mode")
			self.mWIPClient = WIPClient_edu(ip, port, device_id, device_pw, isAutoConnect, live_receive, live_send, live_send_interval)

		"""
	@brief 노드 데이터를 전송하는 메소드 live_send가 True일 경우 데이터만 등록된다.
	@param values [[]] 2중 list로 되어있다. 예시) [["Node1Name", "Node1Type","Node1Value"],["Node2Name", "Node2Type","Node2Value"]]
	"""
	def sendData(self, values):
		self.mWIPClient.sendData(values)

	"""
	@brief 노드 데이터를 즉시 전송하는 메소드 live_send가 True일 경우에도 즉시 전송
	@param values [[]] 2중 list로 되어있다. 예시) [["Node1Name", "Node1Type","Node1Value"],["Node2Name", "Node2Type","Node2Value"]]
	"""
	def sendDataDirect(self, values):
		self.mWIPClient.sendDataDirect(values)

	"""
	@brief 수신받은 데이터를 받는 메소드
	live_receive가 True일 경우 백그라운드에서 수신한 노드 데이터를 리턴한다.
	advanced protocol에서 live_receive가 False일 경우 None 리턴
	@return bool or None
	"""
	def receiveData(self):
		return self.mWIPClient.receiveData()

	"""
	@brief 인증이 완료되었는지 확인하는 메소드
	@return bool
	"""
	def checkCertified(self):
		return self.mWIPClient.checkCertified()

	"""
	live_receive가 True일 경우 Queue에 받은 데이터가 존재하는지 확인
	@return bool
	"""
	def isExistReceiveData(self):
		return self.mWIPClient.isExistReceiveData()

	"""
	서버 접속이 완료될 때 까지 대기한다.
	"""
	def waitForConnect(self):
		self.mWIPClient.waitForConnect()
