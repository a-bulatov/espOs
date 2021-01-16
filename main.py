try:
    import webrepl, uos, machine, time
except:
    from esp_debug import webrepl, machine, time, uos
import json


class _System:

    def __init__(self):
        try:
            uos.remove('error.txt')
        except:
            pass
        try:
            self.__config = None
            self.__config = self.config
            self.__config['LoopInterval'] = self.__config.get('LoopInterval', 100)
            logic = self.__config.get('Logic')
            if logic is None:
                lst = uos.listdir('logics')
                if len(lst)==1:
                    logic = lst[0]
                else:
                    raise Exception('Logic is not defined')
            if logic.endswith('.py'):
                logic = logic[:-3]
            self.__logic = __import__('logics.' + logic)
            self.__logic = getattr(self.__logic, logic)
            lst = dir(self.__logic)
            if 'setup' in lst and 'loop' in lst:
                self.__logic.setup(self)
                self.__timer = machine.Timer(0)
                self.__prev_ms = time.ticks_ms()
                self.__timer.init(period=10, mode=machine.Timer.PERIODIC, callback=self.handler)
        except Exception as e:
            s = e.__class__.__name__ + '\n'
            s+= '\n'.join(str(x) for x in e.args)
            with open('error.txt', 'w') as f:
                f.write(s)


    def handler(self):
        x = time.ticks_ms()-self.__prev_ms
        if x < 0 or x >= self.__config['LoopInterval']:
            self.__prev_ms = time.ticks_ms()
            self.__logic.loop(self)

    @property
    def config(self):
        if self.__config:
            return self.__config
        try:
            src = ''
            f = open('config.json', 'r')
            f = f.readlines()
            for x in f:
                x = x.strip()
                if x == '' or x.startswith('--') or x.startswith('//'):
                    continue
                src += x
            return json.loads(src)
        except:
            return {}

SYSTEM = None

def init():
    global SYSTEM
    if SYSTEM is None:
        try:
            SYSTEM = _System()
        except:
            SYSTEM = None

init()
if __name__ == '__main__':
    while True:
        time.sleep(0.1)