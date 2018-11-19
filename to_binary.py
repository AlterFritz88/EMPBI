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
    temp = {}

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
                        count_et = int(line[-3:2])
                        temp[count_et] = []
                        break

    temp_bin = {}
    if len(max(temp[count_et])) == 4:
        for key, value in temp.items():
            temp_bin[key] = [hex2bin(x, 16) for x in value]

    else:
        for key, value in temp.items():
            temp_bin[key] = [hex2bin(x, 8) for x in value]

    return temp_bin


