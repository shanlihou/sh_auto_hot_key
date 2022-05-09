import logging

def INFO(*args):
    _str = ','.join(str(i) for i in args)
    print(_str)
    logging.info(_str)


def ERROR(*args):
    _str = ','.join(str(i) for i in args)
    print(_str)
    logging.error(_str)