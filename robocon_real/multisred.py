import time
import threading

a=0

def func1():
    global a
    while True:
        a = a + 1
        print(a)
        time.sleep(1)


def func2():
    global a
    while True:
        if a%5==0:
            print("1ラップB")
            time.sleep(1)

if __name__ == "__main__":
    thread_1 = threading.Thread(target=func1)
    thread_2 = threading.Thread(target=func2)
    thread_1.start()
    thread_2.start()
