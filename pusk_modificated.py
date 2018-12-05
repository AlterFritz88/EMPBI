from to_binary import hex2bin


def modificated(preper_data, new_i, limited_point):
    uart_data = []
    etalons = []
    in_process = 0
    while new_i <= limited_point:
        if preper_data[new_i][5:] == '11111111111':  # it means FG
            if (preper_data[new_i][1:4] == '000') and in_process == 0:  # it means mode 000
                in_process = 1
                uart_data.append('10000010')  # reset
                uart_data.append('10100100')  # byte to say
                uart_data.append('11111111')  # first byte of 1 reg
                uart_data.append(
                    '0' + preper_data[new_i + 1][11] + preper_data[new_i + 1][9:11] + preper_data[new_i + 1][12] +
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
        return uart_data, etalons



def non_modificated(preper_data, i, all_data, limited):
    uart_data = []
    etalons = []
    in_process = 0
    modification_point = None
    limited_point = None

    while ((i <= all_data) and not limited):

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

            if (preper_data[i][1:4] == '001') and in_process == 0:  # it means mode 001
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
            in_process = 0
            i += 1
    i -= 1

    return uart_data, etalons, i, limited, limited_point, modification_point