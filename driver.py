import serial
import time
from modi import recive_pp
#sudo chmod a+rw /dev/tty

ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000)

answer = {}
to_send, etalons, etaps = recive_pp()

for etap in etaps:
    data = to_send[etap]
    data_b = [bytes([int(x, 2)]) for x in data]
    etalon = len(etalons[etap]) * 2
    answer_etap = []
    for inf in data_b:
        if inf == b'\x81':
            ser.write(inf)
            response = b'\x00'
            while response != b'\xff':
                print('wait answer from block')
                response = ser.read(1)
                print(response)
        ser.write(inf)
    for i in range(etalon):
        answer_etap.append(ser.read(1))  # len(etalons[etap])
    answer[etap] = answer_etap


send = bytes([(int('10000001', 2))])
print(send)
print(answer)