import threading
import time

def foo():
    for i in range(5):
        print(i*10)
        time.sleep(.5)
        
th = threading.Thread(target=foo)
th.start()

for i in range(10):
    print(i)
    time.sleep(.2)
    
th.join()
print("hi")