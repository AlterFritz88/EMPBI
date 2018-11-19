def get_etaps(file):
    etaps = []
    with open(file, 'r') as file:
        for line in file:
            if line[0] == 'E':
                for i in range(len(line)):
                    if (line[i] == ','):
                        etaps.append(int(line[1:i]))
                        break
    return etaps