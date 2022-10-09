import time
import threading

a=0
b=0

def func1():
    while True:
        a=a+1
        time.sleep(0.001)
        a=a+1
        time.sleep(0.001)
        if a>=400:
            print("1ラップA")
            a=0


def func2():
    while True:
        b=b+1
        time.sleep(0.001)
        b=b+1
        time.sleep(0.001)
        if b>=400:
            print("1ラップB")
            b=0

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    thread_2.start()
