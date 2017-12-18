import pyfirmata
import time


try:
    board = pyfirmata.util.get_the_board(base_dir='/dev/serial/by-id/', identifier='usb-')
except:
    time.sleep(0.5)
    continue

iterator = pyfirmata.util.Iterator(board)
iterator.start()

def proximity():
    board.analog[0].enable_reporting()
    board.analog[1].enable_reporting()
    board.analog[2].enable_reporting()
    straight = board.analog[0].read()
    right = board.analog[1].read()
    left = board.analog[2].read()
    
    return straight, right, left