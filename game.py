import pygame
import numpy as np

import engine

window_width = 600
window_height = 800
cell_size = 200


def game():
    global window_width, window_height, cell_size, X, y

    pygame.init()

    screen = pygame.display.set_mode([window_width, window_height])
    pygame.display.set_caption("TicTacToe game")
    continu = True
    player = 1
    result = 0
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    timer = pygame.time.Clock()
    pich = 10

    terrain = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    wins = [0, 0, 0]

    while continu:
        if(player == -1 and (not result) and (not engine.is_draw(terrain))):
            print("Call IA")
            coordIA = engine.minimax(terrain, 0)
            print(coordIA)
            terrain[coordIA[0]][coordIA[1]] = player
            player *= (-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continu = False
            if event.type == pygame.KEYDOWN:
                if(result or engine.is_draw(terrain)):
                    result = 0
                    terrain = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            if event.type == pygame.MOUSEBUTTONUP:
                if(result == 0 and player == 1):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    coord = engine.new_move(
                        terrain, player, mouse_x, mouse_y)
                    if(coord[0] != -1 and coord[1] != -1):
                        terrain[coord[0]][coord[1]] = player
                        player *= (-1)

        engine.draw_terrain(screen, terrain)

        if(result == 0):
            result = engine.winner_or_not(terrain)
            wins[result+1] += 1

        if(result or engine.is_draw(terrain)):
            if(result):
                draw_string = "player "+str(result)+" wins"
            else:
                draw_string = "egalite"

        else:
            draw_string = "player "+str(player)

        score = str(wins[0])+"   |   "+str(wins[2])
        engine.write_text(screen, draw_string, 20)
        engine.write_text(screen, score, 100)
        pygame.display.update()
    pygame.quit()


game()
