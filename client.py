import socket
import pickle
import pygame


def transpose_matrix(matrix):
    new_matrix = []
    for j in range(len(matrix[0])):
        temp = []
        for i in matrix:
            temp.append(i[j])
        new_matrix.append(temp)
    return new_matrix


def get_matrix_diagonals(matrix):
    diagonal_1 = [matrix[0][0], matrix[1][1], matrix[2][2]]
    diagonal_2 = [matrix[2][0], matrix[1][1], matrix[0][2]]
    return diagonal_1, diagonal_2


from menu import main

ClientSocket = socket.socket()
pygame.init()
host, port, name = main()
num_client = None
port = int(port)
pygame.quit()

try:
    ClientSocket.connect((host, port))
    print("Connected")
except socket.error as e:
    print('ERROR: ' + e)
    exit()

w, h = 600, 600
h1 = 800
cross = 'x'
null = 'o'
fps = 120
crossColor = (0, 255, 0)
nullColor = (255, 0, 0)

ClientSocket.send(name.encode("utf-8"))
dat = ClientSocket.recv(4096)

if dat.decode("utf-8") == "0":
    num_client = 0
elif dat.decode("utf-8") == "1":
    num_client = 1

data = ClientSocket.recv(4096)
data_arr = pickle.loads(data)
pygame.init()

running = True
pygame.mouse.set_visible(False)

sc = pygame.display.set_mode([w, h1])
clock = pygame.time.Clock() 

font = pygame.font.SysFont('Arial', 200, bold=True)
font_cursor = pygame.font.SysFont('Arial', 80, bold=True)
font_score = pygame.font.Font('fonts/font.ttf', 30)
render_font_button = pygame.font.Font('fonts/font.ttf', 35).render("RESTART", False, (0, 0, 0))

icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(icon)

cursor = pygame.image.load('img/cursor.png')
cursor = pygame.transform.scale(cursor, (40, 40))

pointer = pygame.image.load('img/pointer.png')
pointer = pygame.transform.scale(pointer, (40, 40))

button_x, button_y = 200, 670
button_w, button_h = 200, 80

score1, score2 = data_arr[0], data_arr[1]
name1, name2 = data_arr[2], data_arr[3]
map_ = data_arr[4]
isCross = data_arr[5]
firstHod = data_arr[6]
crossWin, nullWin, nobody = data_arr[7], data_arr[8], data_arr[9]
pygame.display.set_caption('TIC TAC TOE ONLINE')

while running:
    isHod = (firstHod and num_client == 0) or (not firstHod and num_client == 1)
    map_set, isCrossWin, isNullWin, isNobody, isReady = [False for _ in range(5)]
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            running = False

    sc.fill('white')
    mouse_x, mouse_y = pygame.mouse.get_pos()

    pygame.draw.line(sc, (0, 0, 0), (0, 200), (w, 200), 5)
    pygame.draw.line(sc, (0, 0, 0), (0, 400), (w, 400), 5)
    pygame.draw.line(sc, (0, 0, 0), (200, 0), (200, h), 5)
    pygame.draw.line(sc, (0, 0, 0), (400, 0), (400, h), 5)

    pygame.draw.rect(sc, (0, 255, 0), (0, 600, w, h1))

    render_score1 = font_score.render(f"{name1.decode('utf-8')}: {score1}", False, (0, 0, 0))
    render_score2 = font_score.render(f"{name2.decode('utf-8')}: {score2}", False, (0, 0, 0))

    sc.blit(render_score1, (0, 600))
    sc.blit(render_score2, (0, 630))

    if (crossWin or nullWin or nobody):
        pygame.draw.rect(sc, (255, 255, 255), (button_x, button_y, button_w, button_h), border_radius=30)
        sc.blit(render_font_button, (button_x, button_y+button_h//4))

    if (crossWin or nullWin or nobody) and ((button_x < mouse_x < button_x + button_w and button_y < mouse_y < button_y + button_h) and pygame.mouse.get_pressed()[0]):
        isReady = True

    if mouse_y < h:
        if isHod and not (crossWin or nullWin or nobody):
            if isCross:
                rendered_font_cursor = font_cursor.render(cross, False, (0, 0, 0))
                sc.blit(rendered_font_cursor, (mouse_x, mouse_y-30))
            else:
                rendered_font_cursor = font_cursor.render(null, False, (0, 0, 0))
                sc.blit(rendered_font_cursor, (mouse_x, mouse_y-30))
        else:
            sc.blit(cursor, (mouse_x, mouse_y-30))
    else:
        if (button_x < mouse_x < button_x + button_w and button_y < mouse_y < button_y + button_h) and (crossWin or nullWin or nobody):
            sc.blit(pointer, (mouse_x, mouse_y))
        else:
            sc.blit(cursor, (mouse_x, mouse_y))
    for i_index, i in enumerate(map_):
        for j_index, j in enumerate(i):
            rendered_font = font.render(j, False, (0, 0, 0))
            sc.blit(rendered_font, (i_index*200+50, j_index*200-40))
            if pygame.mouse.get_pressed()[0] and not crossWin and not nullWin and not nobody and mouse_x < w and mouse_y < h:
                map_index_i, map_index_j = min(mouse_x // 200, 2), min(mouse_y // 200, 2)
                if map_[map_index_i][map_index_j] == '' and isHod:
                    map_set = True
                    break
        else:
            continue
        break

    tr_map = transpose_matrix(map_)

    for i in range(3):
        setted_map = set(map_[i])
        if '' not in map_[i]:
            if len(setted_map) == 1:
                if cross in map_[i]:
                    if not (crossWin or nullWin or nobody):
                        isCrossWin = True
                    pygame.draw.line(sc, crossColor, (i*200+100, 0), (i*200+100, h), 15)
                if null in map_[i]:
                    if not (crossWin or nullWin or nobody):
                        isNullWin = True
                    pygame.draw.line(sc, nullColor, (i*200+100, 0), (i*200+100, h), 15)

        setted_tr_map = set(tr_map[i])
        if '' not in tr_map[i]:
            if len(setted_tr_map) == 1:
                if cross in tr_map[i]:
                    if not (crossWin or nullWin or nobody):
                        isCrossWin = True
                    pygame.draw.line(sc, crossColor, (0, i*200+100), (w, i*200+100), 15)
                if null in tr_map[i]:
                    if not (crossWin or nullWin or nobody):
                        isNullWin = True
                    pygame.draw.line(sc, nullColor, (0, i*200+100), (w, i*200+100), 15)


    diagonal_1, diagonal_2 = get_matrix_diagonals(map_)

    setted_d1 = set(diagonal_1)
    setted_d2 = set(diagonal_2)

    if len(setted_d1) == 1:
        if cross in diagonal_1:
            if not (crossWin or nullWin or nobody):
                isCrossWin = True
            pygame.draw.line(sc, crossColor, (0, 0), (w, h), 15)
        if null in diagonal_1:
            if not (crossWin or nullWin or nobody):
                isNullWin = True
            pygame.draw.line(sc, nullColor, (0, 0), (w, h), 15)

    if len(setted_d2) == 1:
        if cross in diagonal_2:
            if not (crossWin or nullWin or nobody):
                isCrossWin = True
            pygame.draw.line(sc, crossColor, (h, 0), (0, w), 15)
        if null in diagonal_2:
            if not (crossWin or nullWin or nobody):
                isNullWin = True
            pygame.draw.line(sc, nullColor, (h, 0), (0, w), 15)

    if not crossWin and not nullWin and not any('' in i for i in map_):
        if not (crossWin or nullWin or nobody):
            isNobody = True

    if map_set and isHod:
        if isCross:
            ClientSocket.send(f"setcross {map_index_i} {map_index_j}".encode("utf-8"))
        else:
            ClientSocket.send(f"setnull {map_index_i} {map_index_j}".encode("utf-8"))
    elif isReady:
        if num_client == 0:
            ClientSocket.send(f"ready1".encode("utf-8"))
        else:
            ClientSocket.send(f"ready2".encode("utf-8"))
    elif isCrossWin:
        ClientSocket.send("crossWin".encode("utf-8"))
        isCrossWin = False
    elif isNullWin:
        ClientSocket.send("nullWin".encode("utf-8"))
        isNullWin = False
    elif isNobody:
        ClientSocket.send("nobody".encode("utf-8"))
        isNobody = False
    else:
        ClientSocket.send("None".encode("utf-8"))

    data = ClientSocket.recv(2048*2048)
    data_arr = pickle.loads(data)
    score1, score2 = data_arr[0], data_arr[1]
    name1, name2 = data_arr[2], data_arr[3]
    map_ = data_arr[4]
    isCross = data_arr[5]
    firstHod = data_arr[6]
    crossWin, nullWin, nobody = data_arr[7], data_arr[8], data_arr[9]
    pygame.display.flip()
    clock.tick(fps)

