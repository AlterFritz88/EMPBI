from modi import recive_pp

to_send, etalons, etaps = recive_pp()



for k, v in to_send.items():
    print(k, to_send[k])
print(type(to_send[1]))
print(len(to_send[1]))

