from canmessage import canmessage

def CANtoGC(msg: canmessage) -> str:
    tid = msg.canid << 5

    gc = ':'
    gc += f'X{tid:04X}' if msg.ext else f'S{tid:04X}'
    gc += 'R' if msg.rtr else 'N'

    for i in range(msg.dlc):
        gc += f'{msg.data[i]:02X}'

    gc += ';'
    return gc

def GCtoCAN(gc: str) -> canmessage:
    # self.logger.log(f'** GCtoCAN {gc}')
    try:
        ext = True if (gc[1] == 'X') else False

        pos = gc.find('N')
        if pos == -1:
            rtr = True
            pos = gc.find('R')
        else:
            rtr = False

        canid = int(gc[2:pos], 16) >> 5

        data = gc[pos + 1:]
        datalen = int((len(gc) - pos) / 2)
        bytedata = [ int(data[i * 2: (i * 2) + 2], 16) for i in range(datalen)]

        msg = canmessage(canid=canid, ext=ext, rtr=rtr, data = bytedata)
        #print('convert ok')

    except:
        print('** GCtoCAN invalid string')
        msg = None

    return msg
