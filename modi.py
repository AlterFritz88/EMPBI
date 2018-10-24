
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
    if (preper_data[i][6:] == '1111111111') and (preper_data[i][0] == '1'):
        if preper_data[i][0] == '1':
            modification_point = i
            print(modification_point)

    if (preper_data[i][4] == '1') and (preper_data[i][6:] == '1111111111'):
        limited = True


    if (limited == 1) and (preper_data[i+1] == '0000001000000000'):
        steps = int(preper_data[i][0:7], 2)
        i += 2
        count_number_chanches = int(preper_data[i][0:4], 2)             # количество измененей
        print(count_number_chanches)

        preper_data[modification_point + int(preper_data[i][10:], 2)] = preper_data[i+count_number_chanches]
        i += 1

        for j in range(count_number_chanches - 1):
            print(preper_data[i + j], i + j, i + count_number_chanches + j, preper_data[i + count_number_chanches + j])
            preper_data[modification_point + int(preper_data[i+j],2)] = preper_data[i+count_number_chanches+j]

        i += (count_number_chanches * 2) - 1


    i += 1
print(preper_data)

#print(preper_data[int(preper_data[i][10:], 2)])