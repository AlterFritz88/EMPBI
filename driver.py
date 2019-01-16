import serial
import time
from modi import recive_pp
from to_binary import hex2bin
#sudo chmod a+rw /dev/tty

def etap_processor(etalons, data):
    ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000, timeout=0.5)
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
    answer_etap_res = []
    for i in range(len(answer_etap)):
        if i % 2 == 1:
            continue
        else:
            answer_etap_res.append(hex2bin(str(int.from_bytes(answer_etap[i], byteorder='big')), 10)[7:] + hex2bin(
                str(int.from_bytes(answer_etap[i + 1], byteorder='big')), 10)[7:])

    return answer_etap_res  # int.from_bytes(i, byteorder='big')



def do_prog(start_etap=0, end_etap=-1):
    def etap_processor(etalons, data, etap, step, mod=None):
        ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000, timeout=0.2)
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
        answer_etap_res = []
        for i in range(len(answer_etap)):
            if i % 2 == 1:
                continue
            else:
                answer_etap_res.append(hex2bin(str(int.from_bytes(answer_etap[i], byteorder='big')), 10)[7:] + hex2bin(str(int.from_bytes(answer_etap[i+1], byteorder='big')), 10)[7:])
        if mod == None:
            return (etap, step), answer_etap_res  #int.from_bytes(i, byteorder='big')
        else:
            return (etap, step, mod), answer_etap_res



    ser = serial.Serial('/dev/ttyUSB0', baudrate=1000000, timeout=0.5)
    answer = []
    to_send, etalons, etaps = recive_pp()
    etalon_bin = []
    etaps = etaps[start_etap:end_etap]

    for etap in etaps:
        data_temp = to_send[etap]
        etalon = etalons[etap]

        for step in range(len(data_temp)):

            if type(data_temp[step][0]) == str:
                print(etap, step, data_temp[step])
                etalon_s_e = etalon[step]
                answer.append(etap_processor(etalon_s_e, data_temp[step],etap, step))
                etalon_bin.append(((etap, step), etalon_s_e))
            else:
                for mod in range(len(data_temp[step])):
                    print(etap, step, mod, data_temp[step][mod])
                    etalon_s_e = etalon[step][mod]
                    answer.append(etap_processor(etalon_s_e, data_temp[step][mod], etap, step, mod))
                    etalon_bin.append(((etap, step, mod), etalon_s_e))

    return answer, etalon_bin


def get_info_for_send():
    to_send, etalons, etaps = recive_pp()
    data_for_return = []

    for etap in etaps:
        data_temp = to_send[etap]
        etalon = etalons[etap]

        for step in range(len(data_temp)):

            if type(data_temp[step][0]) == str:
                print(etap, step, data_temp[step])
                etalon_s_e = etalon[step]
                data_for_return.append([(etap, step), data_temp[step], etalon_s_e])



            else:
                for mod in range(len(data_temp[step])):
                    print(etap, step, mod, data_temp[step][mod])
                    etalon_s_e = etalon[step][mod]
                    data_for_return.append([(etap, step, mod), data_temp[step][mod], etalon_s_e])

    return data_for_return




if __name__ == '__main__':
    data = get_info_for_send()
    print('datat', data)
    for i in data:
        print('i', i)
        get_ans = etap_processor(i[-1], i[1])
        i.append(get_ans)
    print(data)