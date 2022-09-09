from signal import SIG_UNBLOCK
import RPi.GPIO as GPIO             #GPIO用のモジュールをインポート
import time                         #時間制御用のモジュールをインポート
import sys                          #sysモジュールをインポート

AWO=2

GPIO.setmode(GPIO.BCM)
GPIO.setup(AWO,OUT)

try:
  GPIO.output(AWO,GPIO.HIGH)

except KeyboadInterrupt:
  GPIO.cleanup()
  sys.exit()
