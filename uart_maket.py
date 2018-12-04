import pyb
ua = pyb.UART(6)
ua.init(1000000)
while 1:
    a = ua.read(1)
    print(a)
    if a == b'\x81':
        ua.write(b'\xff')       #stop word
        ua.write(b'\x11')
        ua.write(b'\x0f')
        ua.write(b'\xbf')
        ua.write(b'\x01')
        ua.write(b'\x02')
        ua.write(b'\x03')
        ua.write(b'\x04')
        ua.write(b'\x05')
        ua.write(b'\x06')
        ua.write(b'\x07')
        ua.write(b'\x08')
        ua.write(b'\x09')


