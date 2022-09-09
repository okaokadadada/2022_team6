from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート
GPIO.setwarnings(False)
AWO=2

GPIO.setmode(GPIO.BCM)
GPIO.setup(AWO,GPIO.OUT)

try:
  GPIO.output(AWO,GPIO.HIGH)

except KeyboadInterrupt:
  GPIO.cleanup()
  sys.exit()
