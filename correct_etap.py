def correct_etap(preper_data, data):
    data_to_be_chanched = data[int(preper_data[1], 2)]
    print('chanche me', data_to_be_chanched)
    data_to_be_chanched[0] = '0000000001111110'
    for i in range(len(preper_data)):
        if i == 0:
            continue
        data_to_be_chanched[i] = preper_data[i]
    print('changed', data_to_be_chanched)
    return data_to_be_chanched