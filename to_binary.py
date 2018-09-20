'''
преобразователь ПП в бинарный вид
прописать в правилах, что новая каждая команда на новой строчке и заканчивается запятой

'''
sample = ['0', 'x']
temp = []
with open('octal_pp', 'r') as file:
    for line in file:
        line = line.replace(' ', '')
        if line[0] in sample:
            for i in range(len(line)):
                if (line[i] == ',') and (line[0] == 'x'):
                    temp.append(line[1:i])
                elif (line[i] == ',') and (line[0] == '0'):
                    temp.append(line[:i])


def hex2bin(str, form=16):
    """
    Переводчик hex, oct str в bin str
    """
    a = int(str, form)
    return format(a, '0>16b')

if len(max(temp)) == 4:
    temp_bin = [hex2bin(x, 16) for x in temp]
else:
    temp_bin = [hex2bin(x, 8) for x in temp]

with open('bin_pp', 'w') as wfile:
    for item in temp_bin:
        wfile.write(item + ',')

print(temp_bin)
rgfydrtyrf

