from threading import Thread
import socket, select, time

class System(Thread):
    INST = None
    PINS = {
    0: {
        'N': 18,
        'func': ['SPICS2'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    1: {
        'N': 22,
        'func': ['U0_TXD', 'SPICS1'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    2: {
        'N': 17,
        'func': ['U1_TXD', 'I2C_SDA', 'I2S0_WS'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    3: {
        'N': 21,
        'func': ['U0_RXD', 'I2S0_DATA'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    4: {
        'N': 19,
        'func': ['PWM'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    5: {
        'N': 20,
        'func': [],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    6: {
        'N': 14,
        'func': ['SPICLK', 'SDIO_CLK'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    7: {
        'N': 10,
        'func': ['SPIMISO', 'SDIO_DATA0'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    8: {
        'N': 13,
        'func': ['SPIMOSI', 'SDIO_DATA1'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    9: {
        'N': 11,
        'func': ['SDIO_DATA2', 'HSPIHD', 'SPIHD'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    10: {
        'N': 12,
        'func': ['SPIWP', 'HSPIWP', 'SDIO_DATA3'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    11: {
        'N': 9,
        'func': ['SDIO_CMD', 'SPICS0'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    12: {
        'N': 6,
        'func': ['PWM', 'MTDI', 'I2S1_DATA', 'HSPIMISO'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    13: {
        'N': 7,
        'func': ['MTCK', 'I2S1_BCK', 'U0_CTS', 'HSPIMOSI'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    14: {
        'N': 5,
        'func': ['PWM', 'MTMS', 'I2S_WS', 'I2C_SCL', 'HSPICLK'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    15: {
        'N': 16,
        'func': ['PWM', 'HSPICS', 'U0_RTS', 'I2S0_MCK', 'MTDO'],
        'mode': -1,
        'pull': -1,
        'value': 0
    },
    16: {
        'N': 4,
        'func': ['WakeUp'],
        'mode': -1,
        'pull': -1,
        'value': 0
    }
}

    def __new__(cls, *args, **kwargs):
        if System.INST is None:
            return object.__new__(cls)
        else:
            return System.INST

    def __init__(self, port: int = 8888):
        if not(System.INST is None): return
        System.INST = self
        self.__port = port

        self.http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (socket.getaddrinfo("0.0.0.0", self.__port))[0][-1]
        self.http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.http.bind(addr)
        self.http.listen(4)
        Thread.__init__(self)

        self.start()
        pass

    def run(self) -> None:

        while True:
            r, w, err = select.select((self.http,), (), (), 1)
            if r:
                for readable in r:
                    try:
                        client, client_addr = self.http.accept()
                        client.settimeout(3.0)
                        request = client.recv(1024)
                        client.settimeout(None)
                        page = request.decode("utf-8").split('\r\n')
                        request = {}
                        for w in page:
                            w = w.strip()
                            if w == '': continue
                            w = w.split(' ',1)
                            if w[0].endswith(':'):
                                request[w[0][:-1]] = w[1]
                            else:
                                request['METHOD'] = w[0]
                                request['ADDRESS'] = w[1].rsplit(' ',1)[0]
                        page = "HTTP/1.0 200 OK\r\ncontent-type: %s; charset=UTF-8\r\n\r\n%s" % self.handle_http(request, client_addr)
                        client.send(bytes(page, "ascii"))
                        client.close()
                    except:
                        pass
            time.sleep(0.1)

    def handle_http(self, request: dict, client_addr: tuple) -> tuple:
        return 'text/plain', 'YES ZZZ!!'
