import serial
import time
from modi import recive_pp
#sudo chmod a+rw /dev/tty

def etap_processor(data, etap, step, mod=None):
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
    if mod == None:
        return (etap, step), answer_etap
    else:
        return (etap, step, mod), answer_etap

ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000)

answer = []
to_send, etalons, etaps = recive_pp()


for etap in etaps:
    data_temp = to_send[etap]

    for step in range(len(data_temp)):

        if type(data_temp[step][0]) == str:
            print(etap, step, data_temp[step])
            answer.append(etap_processor(data_temp[step],etap, step))
        else:
            for mod in range(len(data_temp[step])):
                print(etap, step, mod, data_temp[step][mod])
                answer.append(etap_processor(data_temp[step][mod], etap, step, mod))

print(answer)