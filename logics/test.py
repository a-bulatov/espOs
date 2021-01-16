def index(*args, **kwargs):
    return 'Hello world!'

def setup(system):
    print('Setup')
    system.set_http_handler('/', index)

def loop(system):
    print('Loop')