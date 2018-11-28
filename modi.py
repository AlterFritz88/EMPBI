from to_binary import hex2bin
from collections import deque
from to_binary import to_binary_pp
from lib_parse import get_etaps
from correct_etap import correct_etap

etalons = []

data = to_binary_pp('prog_prov.txt')
etaps = get_etaps('library.txt')

for key, value in data.items():
    print(key)
    for kusok in value:
        print(kusok)
print(etaps)


uart_data_etaps = {}

for etap in etaps:
    preper_data = data[etap]
    if preper_data[0] == '0000000101111110':
        preper_data = correct_etap(preper_data, data)

    uart_data = []
    all_data = len(preper_data)
    in_process = 0
    i = 0
    modification_point = None
    limited = False
    modifications = None
    limited_point = 0


    while i < all_data:

        if preper_data[i] == '0000000001111110':
            'этап модификации этапа'
            temp_data = preper_data
            count_words = int(preper_data[i+2][0:7], 2)
            shift = int(preper_data[i+2][7:], 2)
            value = preper_data[i+3]
            preper_data[shift] = value
            i += 4

            for j in range(count_words - 1):
                shift = int(preper_data[i], 2)
                preper_data[shift] = preper_data[i+1]
                i += 2

        if preper_data[i][6:] == '1111111111':
            if preper_data[i][0] == '1':
                modification_point = i

            if preper_data[i][4] == '1':
                limited = True
                limited_point = i

            if (preper_data[i][1:4] == '000') and in_process == 0:  # it means mode 000
                in_process = 1
                uart_data.append('10000010')  # reset
                uart_data.append('10100100')  # byte to say
                uart_data.append('11111111')  # first byte of 1 reg
                uart_data.append(
                    '0' + preper_data[i + 1][11] + preper_data[i + 1][9:11] + preper_data[i + 1][12] + preper_data[i + 1][
                        13] + preper_data[i + 1][14:])
                uart_data.append(preper_data[i + 2][0:8])
                uart_data.append(preper_data[i + 2][8:])
                uart_data.append(preper_data[i + 3][0:8])
                uart_data.append(preper_data[i + 3][8:])
                i = i + 3


            if (preper_data[i][1:4] == '001') and  in_process == 0:  # it means mode 001
                in_process = 1
                groups = int(preper_data[i + 1], 2) * 5
                i += 2
                uart_data.append('10010100')  # byte to say
                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                uart_data.append('00000000')  # initial adr memory
                uart_data.append('00000001')
                for j in range(groups):
                    uart_data.append(preper_data[i + j][0:8])
                    uart_data.append(preper_data[i + j][8:])
                i += groups - 1
            if etap == 100:
                print(etap, preper_data[i], i)
            if (preper_data[i][1:4] == '010') and in_process == 0:  # it means mode 010
                in_process = 1
                groups = int(preper_data[i + 1], 2) * 3
                i += 2
                uart_data.append('10000001')  # start
                uart_data.append('10011000')  # read memory
                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                uart_data.append('00000000')  # initial adr memory
                uart_data.append('00000001')
                for j in range(groups):
                    etalons.append(preper_data[i + j])
                i += groups

            if (preper_data[i][1:4] == '011') and in_process == 0:  # it means mode 011
                in_process = 1
                groups = int(preper_data[i + 1], 2) * 3
                i += 2
                uart_data.append('10000001')  # start
                uart_data.append('10011000')  # read memory
                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                uart_data.append(preper_data[i][0:8])  # initial adr memory
                uart_data.append(preper_data[i][8:])
                for j in range(groups):
                    etalons.append(preper_data[i + j])
                i += groups + 1

        if (limited == 1):
            steps = int(preper_data[i][0:7], 2)
            modifications = int(preper_data[i][7:], 2)
            i += 2

            for step in range(steps):
                for mod in range(modifications):

                    if preper_data[i-1][8:] == '00000000':                       #табличный закон
                        count_number_chanches = int(preper_data[i][0:4], 2)      # количество измененей

                        preper_data[modification_point + int(preper_data[i][10:], 2)] = preper_data[i+count_number_chanches]
                        i += 1

                        for j in range(count_number_chanches - 1):
                            preper_data[modification_point + int(preper_data[i+j],2)] = preper_data[i+count_number_chanches+j]
                        i += (count_number_chanches * 2) - 1

                    if preper_data[i-1][8:] == '00000001':                      # закон сдвигов
                        slova = int(preper_data[i][0:4], 2)
                        upr_slovo = preper_data[i+slova]
                        if upr_slovo[13] == '0':
                            rotation = -int(upr_slovo[9:13], 2)
                        else:
                            rotation = int(upr_slovo[9:12], 2)

                        if upr_slovo[6] == '0':                                   # циклический сдвиг
                            slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                            slovo_deq.rotate(rotation)
                            preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_deq)
                            i += 1
                            for slovo in range(slova):
                                slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)+slovo])
                                slovo_deq.rotate(rotation)
                                preper_data[modification_point + int(preper_data[i][4:], 2)+slovo] = ''.join(slovo_deq)
                            i += slova + 1

                        if upr_slovo[6] == '1':                                 #логический сдвиг вправо
                            if rotation > 0:
                                slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                                slovo_deq.rotate(rotation)
                                slovo_lis = list(slovo_deq)
                                slovo_lis[:rotation] = '0' * rotation
                                preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_lis)
                                i += 1
                                for slovo in range(slova):
                                    slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2) + slovo])
                                    slovo_deq.rotate(rotation)
                                    slovo_lis = list(slovo_deq)
                                    slovo_lis[:rotation] = '0' * rotation
                                    preper_data[modification_point + int(preper_data[i][4:], 2) + slovo] = ''.join(slovo_lis)
                                i += slova + 1

                            else:
                                if upr_slovo[6] == '1':                                 #логический сдвиг влево
                                    slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                                    slovo_deq.rotate(rotation)
                                    slovo_lis = list(slovo_deq)

                                    slovo_lis[rotation:] = '0' * -rotation
                                    preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_lis)
                                    i += 1
                                    for slovo in range(slova):
                                        slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2) + slovo])
                                        slovo_deq.rotate(rotation)
                                        slovo_lis = list(slovo_deq)
                                        slovo_lis[rotation:] = '0' * -rotation
                                        preper_data[modification_point + int(preper_data[i][4:], 2) + slovo] = ''.join(slovo_lis)
                                    i += slova + 1
                    new_i = modification_point
                    in_process = 0

                    while new_i <= limited_point:
                        if preper_data[new_i][5:] == '11111111111':  # it means FG
                            if (preper_data[new_i][1:4] == '000') and in_process == 0:  # it means mode 000
                                in_process = 1
                                uart_data.append('10000010')  # reset
                                uart_data.append('10100100')  # byte to say
                                uart_data.append('11111111')  # first byte of 1 reg
                                uart_data.append(
                                    '0' + preper_data[new_i+1][11] + preper_data[new_i+1][9:11] + preper_data[new_i+1][12] +
                                    preper_data[new_i + 1][
                                        13] + preper_data[new_i + 1][14:])
                                uart_data.append(preper_data[new_i + 2][0:8])
                                uart_data.append(preper_data[new_i + 2][8:])
                                uart_data.append(preper_data[new_i + 3][0:8])
                                uart_data.append(preper_data[new_i + 3][8:])
                                new_i = new_i + 3

                            if (preper_data[new_i][1:4] == '001') and in_process == 0:  # it means mode 001
                                in_process = 1
                                groups = int(preper_data[new_i + 1], 2) * 5
                                new_i += 2
                                uart_data.append('10010100')  # byte to say
                                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                                uart_data.append('00000000')  # initial adr memory
                                uart_data.append('00000001')
                                for j in range(groups):
                                    uart_data.append(preper_data[new_i + j][0:8])
                                    uart_data.append(preper_data[new_i + j][8:])
                                new_i += groups - 1

                            if (preper_data[new_i][1:4] == '010') and in_process == 0:  # it means mode 010
                                in_process = 1
                                groups = int(preper_data[new_i + 1], 2) * 3
                                new_i += 2
                                uart_data.append('10000001')  # start
                                uart_data.append('10011000')  # read memory
                                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                                uart_data.append('00000000')  # initial adr memory
                                uart_data.append('00000001')
                                for j in range(groups):
                                    etalons.append(preper_data[new_i + j])
                                new_i += groups

                            if (preper_data[new_i][1:4] == '011') and in_process == 0:  # it means mode 011
                                in_process = 1
                                groups = int(preper_data[new_i + 1], 2) * 3
                                new_i += 2
                                uart_data.append('10000001')  # start
                                uart_data.append('10011000')  # read memory
                                uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
                                uart_data.append(preper_data[new_i][0:8])  # initial adr memory
                                uart_data.append(preper_data[new_i][8:])
                                for j in range(groups):
                                    etalons.append(preper_data[new_i + j])
                                new_i += groups + 1
                        new_i += 1
                        in_process = 0
            limited = False
        i += 1
        in_process = 0
        uart_data_etaps[etap] = uart_data
print(preper_data)
print(uart_data_etaps)
print(etalons)
