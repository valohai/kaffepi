from contextlib import contextmanager


@contextmanager
def lit(red=255, green=255, blue=255, brightness=0.3, enable=False):
    if not enable:
        yield
        return
    import blinkt
    print('Turning lights on...')
    try:
        blinkt.set_all(red, green, blue, brightness)
        blinkt.show()
    except:
        pass
    yield
    print('Turning lights off...')
    try:
        blinkt.clear()
        blinkt.show()
    except:
        pass
