#連続して値を超音波センサの状態を読み取る
while True:
    try:
        print(1+1)
    except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
    
