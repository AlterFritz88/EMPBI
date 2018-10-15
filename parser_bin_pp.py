def fg_parse_mode_000():
    global i, preper_data, uart_data
    uart_data.append('10100100')    # byte to say
    uart_data.append('11111111')    # first byte of 1 reg
    uart_data.append('0' + preper_data[i+1][11] + preper_data[i+1][9:11] + preper_data[i+1][12] + preper_data[i+1][13] + preper_data[i+1][14:])
    uart_data.append(preper_data[i+2][0:8])
    uart_data.append(preper_data[i+2][8:])
    uart_data.append(preper_data[i+3][0:8])
    uart_data.append(preper_data[i+3][8:])
    i = i + 3

def fg_parse_mode_001():
    global i, preper_data, uart_data
    groups = int(preper_data[i+1], 2) * 5
    print(groups)
    i += 2
    uart_data.append('10000100')
    for j in range(groups):
        uart_data.append(preper_data[i+j][0:8])
        uart_data.append(preper_data[i+j][8:])
    i += groups


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
            fg_parse_mode_000()

        if preper_data[i][1:4] == '001' and preper_data[i][0] == '0':       # it means mode 000
            fg_parse_mode_001()
    i += 1
    print('i', i)



print(uart_data)