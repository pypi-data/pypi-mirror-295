import time
from . import aes256
from . import ModelJsonData
from . import ConstantVar as const

def _get_timestamp_():
    return int(time.time() * 1000)

_JSON_LINE_FEED_ = "\r\n"

CMD_LOGIN01 = "CMD_LOGIN01"
CMD_DDATA01 = "CMD_DATA01"
CMD_HB = "CMD_HB01"
CMD_CONTROL01 = "CMD_CTRL01"

RESULT_CODE_SUCCESS = "AVA01"
RESULT_CODE_ERROR = "ERR01"

CONTROL_TYPE_CODE_JSON = "type_json"
CONTROL_TYPE_CODE_STRING = "type_string"

"""
@brief 서버 로그인
CODE : DEV-LOGIN-001
CMD : CMD_LOGIN01
"""
def dev_login_001(device_id, device_pw):
    data = ModelJsonData.Create()
    aes = aes256.AES256(const.nobunobu)
    data.addJsonObject("device_id", device_id)
    data.addJsonObject("device_pw", aes.encrypt(device_pw))
    data.addJsonObject("timestamp", _get_timestamp_())
    data.addJsonObject("cmd", CMD_LOGIN01)
    return str(data.getJson() + _JSON_LINE_FEED_), CMD_LOGIN01


"""
@brief 노드 데이터 요소
DEV-DATA-001의 data Array 항목에 들어갈 요소를 얻는다.
"""
def node_data(node_id, node_type, node_data):
    data = ModelJsonData.Create()
    data.addJsonObject("node_id", node_id)
    data.addJsonObject("node_type", node_type)
    data.addJsonObject("node_data", node_data)
    return data.getData()

"""
@brief 노드 데이터 등록
CODE : DEV-DATA-001
CMD : CMD_DDATA01
"""
def dev_data_001(token, nodes):
    data = ModelJsonData.Create()
    data.addJsonObject("token", token)
    data.addJsonObject("timestamp", _get_timestamp_())
    data.addJsonObject("cmd", CMD_DDATA01)
    data.addJsonObject("data", nodes)
    return str(data.getJson() + _JSON_LINE_FEED_), CMD_DDATA01


"""
@brief 서버 HB 응답
CODE : SV-HB-001
CMD : CMD_HB01
"""
def sv_hb_001(token, result):
    data = ModelJsonData.Create()
    data.addJsonObject("token", token)
    data.addJsonObject("timestamp", _get_timestamp_())
    data.addJsonObject("cmd", CMD_HB)
    data.addJsonObject("result", result)
    return str(data.getJson() + _JSON_LINE_FEED_), CMD_HB


"""
@brief 서버 Control 응답
CODE : SV-CTRL-001
CMD : CMD_CTRL01
"""
def sv_ctrl_001(token, result):
    data = ModelJsonData.Create()
    data.addJsonObject("token", token)
    data.addJsonObject("timestamp", _get_timestamp_())
    data.addJsonObject("cmd", CMD_CONTROL01)
    data.addJsonObject("result", result)
    return str(data.getJson() + _JSON_LINE_FEED_), CMD_CONTROL01
