VERSION = "1.4.0"


DEVICE_LOCATION_TYPE_SEONGNAM	=	"SEONGNAM_00"
DEVICE_LOCATION_TYPE_DONGTAN	=	"DONGTAN_00"
DEVICE_LINE_NUMBER              =   1               # 진로 번호를 저장하는 변수이며, 1부터 시작한다.
"""
DEVICE_LOCATION_TYPE 별로 동작이 다를 수 있으므로, 
코드 수정할 때 설치한 검사소에 따라 다른 동작을 하고 있는지 확인하고 싶을 경우 
DEVICE_LOCATION_TYPE를 서칭해서 확인하면 된다.
"""
DEVICE_LOCATION_TYPE			=	""

ADMIN_PASSWD					=	"13207"
AADDMMIINN_PPAASSWWDD           =   "99390413"

temperature_offset = [0.0] * 3
humidity_offset = [0.0] * 3

nobunobu = "wowsystemnobu!)(%589631(W*W=W^2)"

LED_MAX_COUNT = 5
FAN_MAX_COUNT = 4

########################################################### IoT 태그명 정의 ###########################################################

#### IoT 원격 명령 수신 시 마이컴에 안보내고, 임베디드에서 처리할 escape node 별도 정의 ####
C_AlertSound = "C_AlertSound"
C_SystemPing = "C_SystemPing"
ESCAPE_NODE = [C_AlertSound, C_SystemPing]
#################################################################################

#####################################################################################################################################

lamp_on_stylesheet = "border-image: url(:/res/res/lamp_on.png);"
lamp_off_stylesheet = "border-image: url(:/res/res/lamp_off.png);"

led_r_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(231, 76, 60);font: Bold 24pt \"NanumGothicOTFExtraBold\";}\n" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(201, 46, 30);font: Bold 24pt \"NanumGothicOTFExtraBold\";}"
led_g_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(46, 204, 113);font: Bold 24pt \"NanumGothicOTFExtraBold\";}\n" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(16, 174, 83);font: Bold 24pt \"NanumGothicOTFExtraBold\";}"
led_b_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color:rgb(52, 152, 219);font: Bold 24pt \"NanumGothicOTFExtraBold\";}\n" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(22, 122, 189);font: Bold 24pt \"NanumGothicOTFExtraBold\";}"
led_f_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(52, 73, 94);font: Bold 24pt \"NanumGothicOTFExtraBold\";}\n" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(22, 43, 64);font: Bold 24pt \"NanumGothicOTFExtraBold\";}"
led_disable_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(149, 165, 166);font: Bold 24pt \"NanumGothicOTFExtraBold\";}\n" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(119, 135, 136);font: Bold 24pt \"NanumGothicOTFExtraBold\";}"

fan_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(189, 215, 238);font: Bold 18pt \"NanumGothicOTFExtraBold\";}" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(164, 187, 206);font: Bold 18pt \"NanumGothicOTFExtraBold\";}"

traffic_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(189, 215, 238);font: Bold 18pt \"NanumGothicOTFExtraBold\";}" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(164, 187, 206);font: Bold 18pt \"NanumGothicOTFExtraBold\";}"

shutter_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(189, 215, 238);font: Bold 18pt \"NanumGothicOTFExtraBold\";}" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(164, 187, 206);font: Bold 18pt \"NanumGothicOTFExtraBold\";}"

alert_button_stylesheet = "QPushButton{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(189, 215, 238);font: Bold 18pt \"NanumGothicOTFExtraBold\";}" \
"QPushButton:pressed{border-radius: 10px; color: rgb(255, 255, 255);background-color: rgb(164, 187, 206);font: Bold 18pt \"NanumGothicOTFExtraBold\";}"
# 경보 페이지에 표시할 버튼의 텍스트를 설정하며, 이 리스트의 길이에 따라 추가하는 버튼도 달라진다.
alert_button_texts = ["온도 경고", "습도 경고", "화재 경보", "사람 쓰러짐", "차량 충돌", "가스 경보", "경보 테스트", "경보 정지"]

SETUP_FILE_PATH = "/boot/setup.ini"

NO_ACTION_TIME_OUT = 10
CONTROL_PAGE_NO_ACTION_TIME_OUT	= 60 * 5 # 제어 페이지 관련 장시간 무반응 타임아웃

# 메인보드 리셋 핀. 검사소마다 다르다.
# 이 상수 값은 app.py __init__에서 DEVICE_LOCATION_TYPE에 따라 재설정된다.
MAINBOARD_RESET_PIN = 8

page_start = 0
page_login = 1
page_menu1 = 2
page_monitor = 3
page_led = 4
page_fan = 5
page_traffic = 6
page_shutter = 7
page_alert = 8
page_iot_setup = 9
page_popup_message = 10
page_protect_screen = 11
page_inet_setting = 12
page_test = 13

_COUNTDOWN_ROLLBACK_PAGE = 5
_COUNTDOWN_TIMEOUT = 60
_COUNTDOWN_ENDPROCESS = 10
