try:
    import machine, time, uos
    import ustruct as struct
except:
    from esp_debug import machine, time, uos
    import struct

class Pzem:
    CMD = {
        'Addr': b'\xB4\xC0\xA8\x01\x01\x00\x1E',
        'Voltage': b'\xB0\xC0\xA8\x01\x01\x00\x1A',
        'Current': b'\xB1\xC0\xA8\x01\x01\x00\x1B',
        'Power'  : b'\xB2\xC0\xA8\x01\x01\x00\x1C',
        'RegPower':b'\xB3\xC0\xA8\x01\x01\x00\x1D'
    }

    def __init__(self):
        uos.dupterm(None, 1)
        time.sleep(1)
        self.uart = machine.UART(0, 9600)
        time.sleep(0.1)
        self.uart.read()

    def command(self, cmd):
        self.uart.write(Pzem.CMD[cmd])
        time.sleep(0.2)
        x = self.uart.read()
        if len(x) == 7:
            x = list(struct.unpack("!7B", x))
            c = x.pop()
            s = sum(x)
            if c == s % 256:
                return x

    def __call__(self, *args, **kwargs):
        return bool(self.command('Addr'))

    def voltage(self):
        x = self.command('Voltage')
        if x:
            return x[2] + x[3] / 10.0

    def current(self):
        x = self.command('Current')
        if x:
            return x[2] + x[3] / 100.0

    def power(self):
        x = self.command('Power')
        if x:
            return x[1] * 256 + x[2]

    def reg_power(self):
        x = self.command('RegPower')
        if x:
            return x[1] * 256 * 256 + x[2] * 256 + x[3]
