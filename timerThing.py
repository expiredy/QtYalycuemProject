import datetime
from time import sleep
import threading

def plug():
    pass

def timer_run(time, condition=True, intermediate_func=plug(), args_for_intermediate_func=None, end_func=plug(),
              args_for_end_func=None, is_return=False):
    print(f"\nfrom timer: 'Timer is started, time if end - {datetime.datetime.now().time() + time}'\n")
    end_time = datatime.datetime.now() + time
    while datatime.datetime.now() < end_time - 1:
        sleep(1)
        if eval(condition):
            intermediate_func()


def timer_activate(time, func=None, args=None):
    timer = threading.Thread(target=timer_run, args=(time, func, args))
    timer.start()