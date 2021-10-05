import threading
from threading import Thread
import time

class test(Thread):
    compteur = 0
    def __init__(self):
        test.compteur += 1
        self.nameThrd = "Thread_" + str(test.compteur)
        self.compteur = test.compteur
        self.i = 0
        self.thread = Thread.__init__(self, name=self.nameThrd)

    def run(self):
        while (self.i < 10 * self.compteur) :
            self.i += 1
            time.sleep(.05)  # let quick sleep to avoid overload

    def somme(self, a):
        a += a
        return a


    def __str__(self):
        return "{0} : {1} + {2}".format(self.name, self.i, self.is_alive())

if __name__ == "__main__":
    thrd1 = test()
    thrd2 = test()

    thrd1.start()
    thrd2.start()

    print("ok")

