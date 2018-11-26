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
    temp = {}

    with open(filename, 'r') as file:
        for line in file:
            line = line.replace(' ', '')
            line = line.replace('\t', '')
            if line[:2] == '0,':
                temp[count_et].append('0000000000000000')
                continue
            for i in range(len(line)):
                if line[0] == '/':
                    break
                elif (line[i] == ',') and (line[0] == 'x'):
                    temp[count_et].append(hex2bin(line[1:i], 16))
                    break
                elif (line[i] == ',') and (line[0] == '0'):
                    temp[count_et].append(hex2bin(line[1:i], 8))
                    break
                elif (line[i] == ':') and (line[0] == 'E'):
                    count_et = int(line[1:-2])
                    temp[count_et] = []
                    break

                elif line[i] == ',' and (not line[0] == 'x') and (not line[0] == '0') and (not line[0] == 'E'):
                    temp[count_et].append(hex2bin(line[0:i], 10))
                    break
    return temp


