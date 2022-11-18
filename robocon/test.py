import time

a = 0

while True:
    try:
        print(a)
        a = a + 1
        time.sleep(1)
    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
    
