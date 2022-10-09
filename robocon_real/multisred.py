import time
import threading

a=0

def func1(b):
    global a
    a = a + b
    print(a)
    time.sleep(1)


def func2():
    global a
    if a%5==0:
        print("1ラップB")
        time.sleep(1)

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1,b=1)
    thread_2 = threading.Thread(target=func2)
    while True:
        thread_1.start()
        thread_2.start()
