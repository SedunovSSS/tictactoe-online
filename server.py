import socket, pickle

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
HOST = s.getsockname()[0]
PORT = int(input("PORT: "))
print(f"Server running in {HOST}:{PORT}")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
name1 = conn.recv(4096)
print('Connected by', addr)
conn.send("0".encode("utf-8"))
conn1, addr1 = s.accept()
name2 = conn1.recv(4096)
print('Connected by', addr1)
conn1.send("1".encode("utf-8"))

score1, score2 = 0, 0
cross = 'x'
null = 'o'

map_ = [
    ['', '', ''],
    ['', '', ''],
    ['', '', ''],
]

crossWin, nullWin, nobody = False, False, False
isCross = True
ready1, ready2 = False, False
firstHod = True

while True:
    arr = ([score1, score2, name1, name2, map_, isCross, firstHod, crossWin, nullWin, nobody])
    data_string = pickle.dumps(arr)
    conn.send(data_string)
    conn1.send(data_string)
    data = conn.recv(2048*2048)
    data1 = conn1.recv(2048*2048)
    if data.decode('utf-8') == 'ready1':
        ready1 = True
    if data1.decode('utf-8') == 'ready2':
        ready2 = True
    if ready1 and ready2:
        map_ = [
            ['', '', ''],
            ['', '', ''],
            ['', '', ''],
        ]
        firstHod = False if (firstHod and nullWin) or (not firstHod and crossWin) else firstHod if nobody else True
        crossWin, nullWin, nobody = False, False, False
        isCross = True
        ready1, ready2 = False, False
    if data.decode('utf-8') == 'crossWin' and data1.decode('utf-8') == 'crossWin':
        if not crossWin:
            if not firstHod:
                score1 += 1
            else:
                score2 += 1
        crossWin = True
    elif data.decode('utf-8') == 'nullWin' and data1.decode('utf-8') == 'nullWin':
        if not nullWin:
            if not firstHod:
                score1 += 1
            else:
                score2 += 1
        nullWin = True
    elif data.decode('utf-8') == 'nobody' and data1.decode('utf-8') == 'nobody':
        nobody = True
    elif data.decode('utf-8').split()[0] == 'setcross':
        x_index, y_index = int(data.decode('utf-8').split()[1]), int(data.decode('utf-8').split()[2])
        map_[x_index][y_index] = cross
        isCross = not isCross
        firstHod = not firstHod
    elif data1.decode('utf-8').split()[0] == 'setcross':
        x_index, y_index = int(data1.decode('utf-8').split()[1]), int(data1.decode('utf-8').split()[2])
        map_[x_index][y_index] = cross
        isCross = not isCross
        firstHod = not firstHod
    elif data.decode('utf-8').split()[0] == 'setnull':
        x_index, y_index = int(data.decode('utf-8').split()[1]), int(data.decode('utf-8').split()[2])
        map_[x_index][y_index] = null
        isCross = not isCross
        firstHod = not firstHod
    elif data1.decode('utf-8').split()[0] == 'setnull':
        x_index, y_index = int(data1.decode('utf-8').split()[1]), int(data1.decode('utf-8').split()[2])
        map_[x_index][y_index] = null
        isCross = not isCross
        firstHod = not firstHod
    else:
        pass
