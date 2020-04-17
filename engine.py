import pygame
import numpy as np

print("engine.py imported")


window_width = 600
window_height = 800
cell_size = int(window_width/3)


def new_move(terrain, player, mouse_x, mouse_y):
    global window_height, window_width, cell_size
    x_cell = mouse_x // cell_size
    y_cell = mouse_y // cell_size
    if(is_move_ok(terrain, x_cell, y_cell)):
        return([x_cell, y_cell])
    else:
        return([-1, -1])


def is_move_ok(terrain, x_cell, y_cell):
    if(x_cell < 0 or x_cell > 2 or y_cell < 0 or y_cell > 2):
        return 0
    if(terrain[x_cell][y_cell] == 0):
        return 1
    else:
        return 0


def is_finished(terrain):
    if(abs(terrain[0][0]+terrain[0][1]+terrain[0][2]) == 3):
        return(terrain[0][0])
    if(abs(terrain[1][0]+terrain[1][1]+terrain[1][2]) == 3):
        return(terrain[1][0])
    if(abs(terrain[2][0]+terrain[2][1]+terrain[2][2]) == 3):
        return(terrain[2][0])

    if(abs(terrain[0][0]+terrain[1][0]+terrain[2][0]) == 3):
        return(terrain[0][0])
    if(abs(terrain[0][1]+terrain[1][1]+terrain[2][1]) == 3):
        return(terrain[0][1])
    if(abs(terrain[0][2]+terrain[1][2]+terrain[2][2]) == 3):
        return(terrain[0][2])

    if(abs(terrain[0][0]+terrain[1][1]+terrain[2][2]) == 3):
        return(terrain[0][0])
    if(abs(terrain[2][0]+terrain[1][1]+terrain[0][2]) == 3):
        return(terrain[1][1])

    sum_cells = 0
    for i in range(3):
        for j in range(3):
            sum_cells += abs(terrain[i][j])
    if(sum_cells == 9):
        return -2
    return(0)


def flat_terrain(terrain, coef):
    flat_terrain = []
    for i in range(3):
        for j in range(3):
            flat_terrain.append(coef*terrain[i][j])
    return np.array(flat_terrain)


def draw_terrain(screen, terrain):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen, WHITE, (i*cell_size +
                                             i*2, j*cell_size+j*2, cell_size-4, cell_size-4))
            if(terrain[i][j] == -1):
                pygame.draw.circle(
                    screen, RED, (int((i+0.5)*cell_size), int((j+0.5)*cell_size)), int(cell_size/2-30), 5)
            elif(terrain[i][j] == 1):
                pygame.draw.line(screen, BLUE, (i*cell_size +
                                                i*2+30, j*cell_size+j*2+30), ((i+1)*cell_size +
                                                                              i*2-30, (j+1)*cell_size+j*2-30), 10)
                pygame.draw.line(screen, BLUE, (i*cell_size +
                                                i*2+30, (j+1)*cell_size+j*2-30), ((i+1)*cell_size +
                                                                                  i*2-30, j*cell_size+j*2+30), 10)


def write_text(screen, text, y_pos):
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont("Times", 72)

    text = font.render(text, True, BLACK)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = window_width+y_pos
    screen.blit(text, text_rect)
