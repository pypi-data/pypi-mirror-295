
import time
import threading
start = time.time()

def find_square():
    for i in range(6):
        time.sleep(.3)
        print('Hello world')

def another_method():
    for i in range(6):
        time.sleep(.3)
        print('Bye world')
    
t1 = threading.Thread(target=find_square,args=())
t2 = threading.Thread(target=another_method,args=())

t1.start()
t2.start()

t1.join()
t2.join()

end = time.time()
print('It takes --> ',end-start)