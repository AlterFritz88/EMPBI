from modi import recive_pp

to_send, etalons, etaps = recive_pp()



for k, v in to_send.items():
    print(k, to_send[k])




for i in range(len(to_send[1][1][0])):
    print(to_send[70][1][0][i], to_send[70][1][1][i],to_send[70][1][2][i])


