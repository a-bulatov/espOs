from .system import System
import threading, time

class Pin():
    IN, OUT, OPEN_DRAIN = range(3)
    PULL_UP = 1
    IRQ_RISING = 1
    IRQ_FALLING = 2

    def __init__(self, id, mode=- 1, pull=- 1, *, value=None, drive=None, alt=None):
        self.__sys = System()
        self.__pin = System.PINS[id]

    def value(self, x=None):
        if x is None:
            pass
        elif x:
            self.__pin['value'] = 1
        else:
            self.__pin['value'] = 0
        return self.__pin['value']

    def __call__(self, *args, **kwargs):
        if len(args)>0:
            return self.value(args[0])
        elif 'x' in kwargs:
            return self.value(kwargs['x'])
        else:
            return self.value()

    def mode(self, mode=None):
        if mode is None:
            pass
        else:
            self.__pin['mode'] = mode
        return self.__pin['mode']

    def pull(self, pull=None):
        pass

    def drive(self,drive=None):
        pass

    def irq(self,handler=None, trigger=IRQ_FALLING | IRQ_RISING, *, priority=1, wake=None, hard=False):
        pass

    def on(self):
        self.__pin['value'] = 1

    def off(self):
        self.__pin['value'] = 0


class Timer():
    ONE_SHOT, PERIODIC = range(2)

    def __init__(self, id):
        self.__id = id
        self.timer = None
        self.mode = None
        self.callback = None
        self.period = None
        self.tick = None

    def init(self, *, mode=PERIODIC, period=- 1, callback=None):
        self.mode = mode
        self.callback = callback
        self.period = period
        self.tick = time.time()*1000
        if self.timer is None:
            self.timer = threading.Thread(target=self.process)
            self.timer.start()

    def process(self):
        while True:
            if self.tick and (time.time()*1000 - self.tick)>=self.period:
                try:
                    if self.mode == Timer.ONE_SHOT:
                        self.tick = None
                    else:
                        self.tick = time.time() * 1000
                    if self.callback:
                        self.callback()
                except Exception as e:
                    s = '\n\n' + e.__class__.__name__ + '\n'
                    s += '\n'.join(str(x) for x in e.args)
                    with open('error.txt', 'a') as f:
                        f.write(s)
