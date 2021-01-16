import socket, select, time, json

class Http:
    def __init__(self, port=8080, address='0.0.0.0', listeners=4, **kwargs):
        self.__serve = False
        self.__handlers = {}
        self.__ext = kwargs
        self.set_handler('/favicon.ico', '<link rel="icon" href="data:;base64,iVBORw0KGgo=">')
        self.set_handler(404, "<h1>Error: 404<br>Page Not Found!</h1>")
        self.http = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = (socket.getaddrinfo(address, port))[0][-1]
        self.http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.http.bind(addr)
        self.http.listen(listeners)

    def __call__(self, *args, **kwargs):
        r, w, err = select.select((self.http,), (), (), 1)
        if r:
            for readable in r:
                client, client_addr = self.http.accept()
                self.handle_http(client, client_addr)

    def serve_forever(self, realy=True, sleep=0.1):
        if realy and self.__serve: return
        self.__serve = realy
        while self.__serve:
            try:
                self()
            except:
                pass
            if sleep>0: time.sleep(sleep)

    def set_handler(self, request_mask, callback):
        self.__handlers[request_mask] = callback

    def handle_http(self, client, client_addr):
        client.settimeout(3.0)
        request = client.recv(1024)
        while not b"\r\n" in request:
            tmp = client.recv(1024)
            if not tmp: break
            request += tmp
        client.settimeout(None)
        if not request: return
        tmp = request.decode("utf-8").replace('\r\n\r\n', '').split('\r\n')
        request, f = {}, None
        for x in tmp:
            if f is None:
                x = x.split(' ')
                request['METHOD'] = x[0]
                request['VERSION']= x[2]
                x = x[1].split('?', 1)
                if len(x) == 2:
                    lst = x[1].split('&')
                    pms = {}
                    for p in lst:
                        p.split('=', 1)
                        if len(p)==2:
                            pms[p[0]] = p[1]
                    request['PARAMS'] = pms
                x = x[0]
                request['ADDRESS'] = x
                f = self.__handlers.get(x, self.__handlers[404])
            else:
                x = x.split(':', 1)
                request[x[0]] = x[1].strip()

        if isinstance(f, str):
            data = f
        else:
            request["EXT"] = self.__ext
            data = f(request)

        if isinstance(data, tuple):
            mime, data = data
        elif isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
            mime = "application/json"
        else:
            mime = "text/html"

        data = data.encode("utf-8")
        client.send(b"HTTP/1.0 200 OK\r\nServer: esp8266\r\nConnection: close\r\n")
        client.send(b"Content-Type: %s; charset=UTF-8\r\n" % mime.encode("utf-8"))
        client.send(b"Content-Length: %s\r\n\r\n" % str(len(data)).encode("utf-8"))
        client.send(data)
