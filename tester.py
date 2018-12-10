from modi import recive_pp

to_send, etalons, etaps = recive_pp()



for k, v in etalons.items():
    print(k, etalons[k])


#print(len(to_send[1][1]), len(to_send[70]))

for etap in etaps:
    data_temp = to_send[etap]

    for step in range(len(data_temp)):

        if type(data_temp[step][0]) == str:
            print(etap, step, data_temp[step])
        else:
            for mod in range(len(data_temp[step])):
                print(etap, step, mod, data_temp[step][mod])

'''
for i in range(len(to_send[1][1][0])):
    print(to_send[70][1][0][i], to_send[70][1][1][i],to_send[70][1][2][i])
'''

