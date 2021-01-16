try:
    import webrepl, uos, machine, time, network
except:
    from esp_debug import webrepl, machine, time, uos, network
import json


def write_error(e:Exception, ext=None):
    s = e.__class__.__name__ + '\n'
    s += '\n'.join(str(x) for x in e.args)
    with open('error.txt', 'a') as f:
        f.write(s)
        if ext:
            f.write('\n'+ext+'\n')


def init_network(*, STA = None, AP = None):
    if STA is None and AP is None: return
    sta_if = network.WLAN(network.STA_IF)
    ap_if  = network.WLAN(network.AP_IF)
    try:
        if STA or STA == {}:
            if 'SSID' in STA and 'Password' in STA:
                ap_if.active(False)
                sta_if.active(True)
                sta_if.connect(STA['SSID'], STA['Password'])
            n = 6
            while not sta_if.isconnected() and n > 0:
                n -= 1
                time.sleep(0.5)
            if sta_if.isconnected():
                return
    except Exception as e:
        write_error(e, 'Try to start Assess Point')

    if AP:
        sta_if.active(False)
        ap_if.active(True)
        mode = AP.get("Mode", "OPEN").strip().upper()
        if mode.startswith("AUTH_"): mode = mode[5:]
        lst = {
            "OPEN": network.AUTH_OPEN,
            "WEP": network.AUTH_WEP,
            "WPA_PSK": network.AUTH_WPA_PSK,
            "WPA2_PSK": network.AUTH_WPA2_PSK,
            "WPA_WPA2_PSK": network.AUTH_WPA_WPA2_PSK
        }
        mode = lst.get(mode, network.AUTH_OPEN)
        ap_if.config(essid=AP['SSID'], authmode=mode, password=AP['Password'])


class _System:

    def __init__(self):
        try:
            uos.remove('error.txt')
        except:
            pass
        try:
            self.__config = None
            self.__config = self.config
            self.__http = {}
            init_network(STA=self.__config.get('STA'), AP=self.__config.get('AP'))
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
                # проверяем что наинициализировали
                if self.__http != {}:
                    lst = self.__http
                    s = self.__config.get('HTTP', {})
                    import lib.HTTP as HTTP
                    self.__http = HTTP.Http(
                        port=s.get("Port", 80),
                        address=s.get("Bind", "0.0.0.0"),
                        system=self
                    )
                    for x in lst:
                        self.__http.set_handler(x, lst[x])
                # запуск таймера
                self.__timer = machine.Timer(0)
                self.__prev_ms = time.ticks_ms()
                self.__timer.init(period=10, mode=machine.Timer.PERIODIC, callback=self.handler)
        except Exception as e:
            write_error(e)

    def handler(self):
        if self.__http:
            try:
                self.__http()
            except Exception as e:
                write_error(e)
        x = time.ticks_ms()-self.__prev_ms
        if x < 0 or x >= self.__config['LoopInterval']:
            self.__prev_ms = time.ticks_ms()
            try:
                self.__logic.loop(self)
            except Exception as e:
                write_error(e)

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

    def set_http_handler(self, request_mask, callback):
        if isinstance(self.__http, dict):
            self.__http[request_mask] = callback
        else:
            self.__http.set_handler(request_mask, callback)


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