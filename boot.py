try:
    import gc, esp_debug, webrepl
    import uos
except:
    from esp_debug import webrepl, machine, time, uos

try:
    webrepl.start()
    esp_debug.osdebug(None)
    uos.dupterm(None, 1)
except:
    pass
gc.collect()

#import main
#main.__init()
