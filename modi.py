from to_binary import hex2bin
from collections import deque
from to_binary import to_binary_pp
from lib_parse import get_etaps
from correct_etap import correct_etap
from pusk_modificated import modificated, non_modificated


def recive_pp():
    etalons_dick = {}

    data = to_binary_pp('prog_prov.txt')
    etaps = get_etaps('library.txt')

    #for key, value in data.items():
   #     print(key)
     #   for kusok in value:
    #        print(kusok)



    uart_data_etaps = {}

    for etap in etaps:
        preper_data = data[etap]
        if preper_data[0] == '0000000101111110':
            preper_data = correct_etap(preper_data, data)

        uart_data = []
        etalons = []
        all_data = len(preper_data)
        in_process = 0
        i = 0
        modification_point = None
        limited = False
        modifications = None
        limited_point = 0

        while i < all_data:

            if preper_data[i] == '0000000001111110' and  (i==0):
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
                preper_data = preper_data[i:]

            uart_data_t, etalons_t, i, limited, limited_point, modification_point = non_modificated(preper_data, 0, len(preper_data), limited)
            uart_data.append(uart_data_t)
            etalons.append(etalons_t)




            if (limited == 1):
                steps = int(preper_data[i][0:7], 2)
                modifications = int(preper_data[i][7:], 2)
                i += 2
                new_i = modification_point

                for step in range(steps):
                    if step > 0:
                        modifications = int(preper_data[i-1][7:], 2)
                        i += 1

                    uart_data_step = []
                    etalon_step = []

                    if preper_data[i - 1][8:] == '00000000':  # табличный закон
                        count_number_chanches = int(preper_data[i][0:4], 2)  # количество измененей
                        change_adreses = []
                        change_adreses.append(int(preper_data[i][10:], 2))
                        i += 1
                        for j in range(count_number_chanches - 1):
                            change_adreses.append(int(preper_data[i + j], 2))
                        i += count_number_chanches - 1


                        for mod in range(modifications):
                            for j in range(count_number_chanches):
                                preper_data[modification_point + change_adreses[j]] = preper_data[
                                    i + j]
                            i += count_number_chanches
                            uart_data_t, etal_t = modificated(preper_data, 0, limited_point)
                            uart_data_step.append(uart_data_t)
                            etalon_step.append(etal_t)



                    if preper_data[i-1][8:] == '00000001':  # закон сдвигов
                        slova = int(preper_data[i][0:4], 2)
                        upr_slovo = preper_data[i + slova]

                        if upr_slovo[13] == '0':
                            rotation = -int(upr_slovo[9:13], 2)
                        else:
                            rotation = int(upr_slovo[9:12], 2)

                        for mod in range(modifications):

                            if upr_slovo[6] == '0':  # циклический сдвиг
                                slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                                slovo_deq.rotate(rotation)
                                preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_deq)
                                i += 1
                                for slovo in range(slova):
                                    slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2) + slovo])
                                    slovo_deq.rotate(rotation)
                                    preper_data[modification_point + int(preper_data[i][4:], 2) + slovo] = ''.join(
                                        slovo_deq)
                                i -= 4

                            if upr_slovo[6] == '1':  # логический сдвиг вправо
                                if rotation > 0:
                                    slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                                    slovo_deq.rotate(rotation)
                                    slovo_lis = list(slovo_deq)
                                    slovo_lis[:rotation] = '0' * rotation
                                    preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_lis)
                                    i += 1
                                    for slovo in range(slova):
                                        slovo_deq = deque(
                                            preper_data[modification_point + int(preper_data[i][4:], 2) + slovo])
                                        slovo_deq.rotate(rotation)
                                        slovo_lis = list(slovo_deq)
                                        slovo_lis[:rotation] = '0' * rotation
                                        preper_data[modification_point + int(preper_data[i][4:], 2) + slovo] = ''.join(
                                            slovo_lis)
                                    i -= 4

                                else:
                                    if upr_slovo[6] == '1':  # логический сдвиг влево
                                        slovo_deq = deque(preper_data[modification_point + int(preper_data[i][4:], 2)])
                                        slovo_deq.rotate(rotation)
                                        slovo_lis = list(slovo_deq)

                                        slovo_lis[rotation:] = '0' * -rotation
                                        preper_data[modification_point + int(preper_data[i][4:], 2)] = ''.join(slovo_lis)
                                        i += 1
                                        for slovo in range(slova):
                                            slovo_deq = deque(
                                                preper_data[modification_point + int(preper_data[i][4:], 2) + slovo])
                                            slovo_deq.rotate(rotation)
                                            slovo_lis = list(slovo_deq)
                                            slovo_lis[rotation:] = '0' * -rotation
                                            preper_data[modification_point + int(preper_data[i][4:], 2) + slovo] = ''.join(
                                                slovo_lis)
                                        i -= 4

                            i += slova + 1


                            uart_data_t, etal_t = modificated(preper_data, 0, limited_point)
                            uart_data_step.append(uart_data_t)
                            etalon_step.append(etal_t)
                        i += 2

                    uart_data.append(uart_data_step)
                    etalons.append(etalon_step)
                    i += 1
            i = all_data + 1


            in_process = 0
            uart_data_etaps[etap] = uart_data
            etalons_dick[etap] = etalons

    return uart_data_etaps, etalons_dick, etaps
