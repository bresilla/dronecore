import pyfirmata

board = pyfirmata.util.get_the_board(base_dir='/dev/serial/by-id/', identifier='usb-')
iterator = pyfirmata.util.Iterator(board)
iterator.start()

def analog(PIN):
    board.analog[PIN].enable_reporting()
    analog = board.analog[PIN].read()
    return analog
