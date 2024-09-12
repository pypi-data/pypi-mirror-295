import datetime
import logging
import logging.handlers
import logging.config

logging.basicConfig(level=logging.DEBUG,
                    filename='/var/log/wow_app/root.log',
                    filemode='w',
                    format='%(asctime)s [%(levelname)s]%(message)s')
gLog = logging.getLogger('app')

def currentNow():
    return datetime.datetime.now()

def currentTime():
    date = datetime.datetime.now()
    return "{0}년 {1}월 {2}일 {3:02}:{4:02}:{5:02}".format(date.year, date.month, date.day, date.hour, date.minute, date.second)
