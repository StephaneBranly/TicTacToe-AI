import pygame
import ai
import numpy as np
import data
import engine

window_width = 1200
window_height = 800
cell_size = 200

NN = ai.Neural_Network()

X = np.load('data_x.npy')  # load
y = np.load('data_y.npy')  # load
print("data len="+str(len(X)))
print("start training")
for i in range(10000):
    NN.train(X, y)
print("finished")


def game():
    global window_width, window_height, cell_size, X, y

    pygame.init()

    print("Press Z/W to make a new game")

    screen = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("TicTacToe game")
    continu = True
    player = 0
    result = 0
    ia_tries = 0
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    pich = 10

    terrain = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    wins = [0, 0]
    current_x0_data = []
    current_x1_data = []
    current_y0_data = []
    current_y1_data = []

    while continu:
        if(player % 2 == 1 and result == 0):
            if(ia_tries < 9):
                for i in range(1000):
                    NN.train(X, y)
                coord = NN.predict(engine.flat_terrain(terrain, 1))
            else:
                coord = [(ia_tries-9)//3, (ia_tries-9) % 3]
            if(engine.is_move_ok(terrain, coord[0], coord[1])):
                current_x1_data.append(engine.flat_terrain(terrain, 1))
                tab = [0,  0,  0,  0,  0,  0, 0, 0, 0]
                tab[coord[0]*3+coord[1]] = 1
                current_y1_data.append(tab)
                terrain[coord[0]][coord[1]] = -1
                player += 1
                ia_tries = 0
            else:
                NN.train(X, y)
                ia_tries += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if(result != 0):
                        result = 0
                        terrain = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                        ia_tries = 0
                if event.key == pygame.K_y:
                    print("retrain")
                    for i in range(10000):
                        NN.train(X, y)
            if event.type == pygame.MOUSEBUTTONUP:
                if(result == 0 and player % 2 == 0):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    coord = engine.new_move(
                        terrain, player % 2, mouse_x, mouse_y)
                    if(coord[0] != -1 and coord[1] != -1):
                        current_x0_data.append(
                            engine.flat_terrain(terrain, -1))
                        tab = [0,  0,  0,  0,  0,  0, 0, 0, 0]
                        tab[coord[0]*3+coord[1]] = 1
                        current_y0_data.append(tab)
                        terrain[coord[0]][coord[1]] = 1
                        player += 1

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, 600, 600))

        engine.draw_terrain(screen, terrain)
        timer.tick(60)

        if(result == 0):
            result = engine.is_finished(terrain)
            if(result == -1):
                result = 2
            if(result == 1 or result == 2):
                wins[result-1] += 1
                if(result == 2):
                    y = np.append(y, current_y1_data, axis=0)
                    X = np.append(X, current_x1_data, axis=0)
                else:
                    y = np.append(y, current_y0_data, axis=0)
                    X = np.append(X, current_x0_data, axis=0)
                current_x0_data = []
                current_x1_data = []
                current_y0_data = []
                current_y1_data = []

        if(result):
            if(result == -2):
                draw_string = "egalite"
            else:
                draw_string = "player "+str(result)+" wins"

        else:
            draw_string = "player "+str(player % 2+1)

        score = str(wins[0])+"   |   "+str(wins[1])
        engine.write_text(screen, draw_string, 20)
        engine.write_text(screen, score, 100)
        NN.draw_network(screen, 600, 0, 600, 600,
                        engine.flat_terrain(terrain, 1))
        pygame.display.update()
    pygame.quit()


game()


np.save('data_x.npy', X)  # save
np.save('data_y.npy', y)  # save
