import time
import threading

def A():
  while True:
    input_data = input()
    print("入力データ　＝　", int(input_data))

def B():
  while True:
    while input_data == "w":
      print("前")
    while input_data == "A":
      print("左")
    while input_data == "S":
      print("後")
    while input_data == "D":
      print("右")
 
try:
    if __name__ == "__main__":
        thread_1 = threading.Thread(target=A)
        thread_2 = threading.Thread(target=B)

        thread_1.start()
        thread_2.start()

except KeyboardInterrupt:       #Ctrl+Cキーが押された
        GPIO.cleanup()              #GPIOをクリーンアップ
        sys.exit()                  #プログラム終了
