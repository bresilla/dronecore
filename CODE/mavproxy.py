import os
os.system('sudo mavproxy.py --master=/dev/ttyS0 --baudrate=57600 --baudrate=57601 --baudrate=57602 --baudrate=57603 --baudrate=57604 --out=udp:10.42.0.1:14550')