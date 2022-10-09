import time
import threading



def func1():
    a=0
    while True:
        a=a+1
        time.sleep(1)


def func2():
    while True:
        if a%10==0:
            print("1ラップB")
            a=0

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)

    thread_1.start()
    thread_2.start()
