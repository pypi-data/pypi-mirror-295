from abc import ABC, ABCMeta, abstractmethod

class WIPClientAbstractModel(metaclass=ABCMeta):
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
	# @abstractmethod 
	# def __init__(self, ip="127.0.0.1", port=10008, device_id="device1", device_pw="00000000", isAutoConnect=True, live_receive=True, live_send=False, live_send_interval=1):
	# 	print("AbstractModel Initialize")

	"""
	@brief 노드 데이터를 전송하는 메소드
	"""
	@abstractmethod 
	def sendData(self, values):
		print("AbstractModel sendData")

	"""
	@vbrief 
	"""
	@abstractmethod
	def sendDataDirect(self, values):
		print("AbstractModel sendDataDirect")

	"""
	@brief 수신받은 데이터를 받는 메소드
	live_receive가 True일 경우 백그라운드에서 수신한 노드 데이터를 리턴한다.
	advanced protocol에서 live_receive가 False일 경우 None 리턴
	"""
	@abstractmethod
	def receiveData(self):
		print("AbstractModel receiveData")

	"""
	@brief 인증이 완료되었는지 확인하는 메소드
	"""
	@abstractmethod
	def checkCertified(self):
		print("AbstractModel checkCertified")

	"""
	live_receive가 True일 경우 Queue에 받은 데이터가 존재하는지 확인
	"""
	@abstractmethod
	def isExistReceiveData(self):
		print("AbstractModel isExistReceiveData")

	"""
	서버 접속이 완료될 때 까지 대기한다.
	"""
	@abstractmethod
	def waitForConnect(self):
		print("AbstractModel waitForConnect")
