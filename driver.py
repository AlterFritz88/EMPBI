import serial
import time
from modi import recive_pp
#sudo chmod a+rw /dev/tty




def do_prog():
    def etap_processor(etalons, data, etap, step, mod=None):
        data_b = [bytes([int(x, 2)]) for x in data]
        etalon = len(etalons) * 2
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



    ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000, timeout=0.5)

    answer = []
    to_send, etalons, etaps = recive_pp()


    for etap in etaps:
        data_temp = to_send[etap]
        etalon = etalons[etap]

        for step in range(len(data_temp)):

            if type(data_temp[step][0]) == str:
                print(etap, step, data_temp[step])
                etalon_s_e = etalon[step]
                answer.append(etap_processor(etalon_s_e, data_temp[step],etap, step))
            else:
                for mod in range(len(data_temp[step])):
                    print(etap, step, mod, data_temp[step][mod])
                    etalon_s_e = etalon[step][mod]
                    answer.append(etap_processor(etalon_s_e, data_temp[step][mod], etap, step, mod))

    return answer, etalons