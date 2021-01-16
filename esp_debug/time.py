import time

__tick_strart = None

def localtime(secs=None):
    x = time.localtime(secs)
    return (
        x.tm_year,
        x.tm_mon,
        x.tm_mday,
        x.tm_hour,
        x.tm_min,
        x.tm_sec,
        x.tm_wday,
        x.tm_yday
    )


def mktime(t=None):
    if t is Mone:
        return int(time.mktime(time.gmtime()))
    t = (
        t[0], # year
        t[1], # month
        t[2], # mday
        t[3], # hour
        t[4], # minute
        t[5], # second
        0, 0, 0
    )
    return time.mktime(t)


def sleep(seconds):
    time.sleep(seconds)


def ticks_ms():
    global __tick_strart
    if __tick_strart:
        x = int(time.time()*1000 - __tick_strart)
    else:
        x = 0
    __tick_strart = time.time()*1000
    return x