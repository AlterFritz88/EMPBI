from to_binary import hex2bin


uart_data = []
preper_data = []
with open('bin_pp', 'r') as file:
    for line in file:
        preper_data.append(line[:-1])
print(preper_data)


all_data = len(preper_data)
i = 0
while i < all_data:
    if preper_data[i][5:] == '11111111111':                                  # it means FG
        if preper_data[i][1:4] == '000' and preper_data[i][0] == '0':       # it means mode 000
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

        if preper_data[i][1:4] == '001' and preper_data[i][0] == '0':       # it means mode 001
            groups = int(preper_data[i + 1], 2) * 5
            print(groups)
            i += 2
            uart_data.append('10010100')  # byte to say
            uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
            uart_data.append('00000000')    # initial adr memory
            uart_data.append('00000001')
            for j in range(groups):
                uart_data.append(preper_data[i + j][0:8])
                uart_data.append(preper_data[i + j][8:])
            i += groups

        if preper_data[i][1:4] == '010' and preper_data[i][0] == '0':       # it means mode 010
            groups = int(preper_data[i + 1], 2) * 3
            print(groups)
            i += 2
            uart_data.append('10000001')    # start
            uart_data.append('10011000')    # read memory
            uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
            uart_data.append('00000000')  # initial adr memory
            uart_data.append('00000001')
            i += groups

        if preper_data[i][1:4] == '011' and preper_data[i][0] == '0':       # it means mode 011
            groups = int(preper_data[i + 1], 2) * 3
            print(groups)
            i += 2
            uart_data.append('10000001')    # start
            uart_data.append('10011000')    # read memory
            uart_data.append(hex2bin(str(hex(groups)), 16)[8:])
            uart_data.append(preper_data[i][0:8])  # initial adr memory
            uart_data.append(preper_data[i][8:])
    i += 1
    print('i', i)



print(uart_data)