
preper_data = []
with open('bin_pp', 'r') as file:
    for line in file:
        preper_data.append(line[:-1])
#print(preper_data)

all_data = len(preper_data)
i = 0
modification_point = None
limited = False
while i < all_data:
    print(i)
    if preper_data[i][5:] == '11111111111':
        if preper_data[i][0] == '1':
            modification_point = i

        if preper_data[i][4] == 1:
            limited = True

    if limited and (preper_data[i+1] == '0000000010000000'):
        steps = int(preper_data[i][0:7], 2)
        i += 2
        count_number_chanches = int(preper_data[i][0:8], 2)
        preper_data[int(preper_data[i][10:], 2)] = preper_data[i+count_number_chanches]
    i += 1
print(modification_point)

#print(preper_data[int(preper_data[i][10:], 2)])