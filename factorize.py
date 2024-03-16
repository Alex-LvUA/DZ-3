from time import time
import multiprocessing
from multiprocessing import Process, freeze_support
from threading import Thread
import concurrent.futures



#print(f'процесорів {multiprocessing.cpu_count()}')


def fact(num):
    m=1
    set1=list()
    set1.append(m)
    set2 = list()
    set2.append(num)
    while True:
        if set2[-1]-m<2:
            break
        else:
            m+=1
            if num%m==0:
                set1.append(m)
                set2.append(int(num/m))
    set=set1+sorted(set2)
    print(set)
    return(set)
def factorize(*number):

    timer = time()
    for n in number:
       fact(n)
    print(f'-Done by 1 process: {round(time() - timer, 4)}\n')

    processes = []
    lenn=len(number)
    for n in number:
        pr=Process(target=fact, args=(n,))
        processes.append(pr)

    timer2 = time()

    [process.start() for process in processes]
    [process.join() for process in processes]
    [process.close() for process in processes]
    print(f'Done by {lenn} processes: {round(time() - timer2, 4)}\n')


    threads = []
    timer3 = time()
    for n in number:
        th = Thread(target=fact, args=(n,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f'Time with using thread: {round(time() - timer3, 4)}\n')

    timer4 = time()
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
       executor.map(fact,number)
    print(f'Time with using concurrent.futures: {round(time() - timer4, 4)}\n')





if __name__ == '__main__':
    multiprocessing.freeze_support()
    factorize(128, 255, 99999, 10651060,9650123, 28932392323)