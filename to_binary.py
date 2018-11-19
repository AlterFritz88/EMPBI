'''
преобразователь ПП в бинарный вид
прописать в правилах, что новая каждая команда на новой строчке и заканчивается запятой

'''


def hex2bin(str, form=16):
    """
    Переводчик hex, oct str в bin str
    """
    a = int(str, form)
    return format(a, '0>16b')

def to_binary_pp(filename):

    sample = ['0', 'x', 'E']
    temp = []

    with open('prog_prov.txt', 'r') as file:
        for line in file:
            line = line.replace(' ', '')
            if line[0] in sample:
                for i in range(len(line)):
                    if (line[i] == ',') and (line[0] == 'x'):
                        temp[count_et].append(line[1:i])
                        break
                    elif (line[i] == ',') and (line[0] == '0'):
                        temp[count_et].append(line[1:i])
                        break
                    elif (line[i] == ':') and (line[0] == 'E'):
                        temp.append([])
                        count_et = int(line[-3:2]) - 1
                        break



    temp_bin = []
    if len(max(temp[0])) == 4:
        for li in temp:
            temp_bin.append([hex2bin(x, 16) for x in li])

    else:
        for li in temp:
            temp_bin.append([hex2bin(x, 8) for x in li])


    '''
    with open('bin_pp', 'w') as wfile:
        for item in temp_bin:
            wfile.write(item + '\n')
    '''
    return temp_bin


