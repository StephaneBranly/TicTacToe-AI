import pygame
import ai
import numpy as np
import data

window_width = 600
window_height = 800
cell_size = int(window_width/3)

NN = ai.Neural_Network()

X  = data.X
y = data.y

def new_move(terrain, player, mouse_x, mouse_y):
    global window_height, window_width, cell_size
    x_cell = mouse_x // cell_size
    y_cell = mouse_y // cell_size
    if(is_move_ok(terrain,x_cell,y_cell)):
        return([x_cell, y_cell])
    else:
        return([-1, -1])

def is_move_ok(terrain,x_cell,y_cell):
    if(x_cell<0 or x_cell>2 or y_cell<0 or y_cell>2):
        return 0
    if(terrain[x_cell][y_cell] == 0):
        return 1
    else: return 0

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

    sum_cells=0
    for i in range(3):
        for j in range(3):
            sum_cells+=abs(terrain[i][j])
    if(sum_cells==9):
        return -2
    return(0)


def flat_terrain(terrain,coef):
    flat_terrain=[]
    for i in range(3):
        for j in range(3):
            flat_terrain.append(coef*terrain[i][j])
    return np.array(flat_terrain)


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
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    timer = pygame.time.Clock()
    pich = 10
    font = pygame.font.SysFont("Times", 72)

    terrain = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    wins=[0,0]

    while continu:
        if(player%2==1 and result==0):
            if(ia_tries<9):
                for i in range(100):
                    NN.train(X,y)
                coord = NN.predict(flat_terrain(terrain,1))    
            else:
                coord = [(ia_tries-9)//3,(ia_tries-9)%3]
            if(is_move_ok(terrain,coord[0],coord[1])):
                terrain[coord[0]][coord[1]] = -1
                player += 1
                ia_tries=0
            else:
                NN.train(X,y)
                ia_tries+=1


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if(result!=0):
                        result=0
                        terrain=[[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                        ia_tries=0
            if event.type == pygame.MOUSEBUTTONUP:
                if(result==0 and player%2==0):
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    coord = new_move(terrain, player % 2, mouse_x, mouse_y)
                    if(coord[0] != -1 and coord[1] != -1):
                        if(player % 2 == 0):
                            X=np.append(X,[flat_terrain(terrain,-1)],axis=0)
                            y=np.append(y,np.array([[coord[0]/2,coord[1]/2]]),axis=0)
                            terrain[coord[0]][coord[1]] = 1
                        player += 1
        
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, (0, 0, window_width, window_width))

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
                                                                                  i*2-30, (j+1)*cell_size+j*2-30), 5)
                    pygame.draw.line(screen, BLUE, (i*cell_size +
                                                    i*2+30, (j+1)*cell_size+j*2-30), ((i+1)*cell_size +
                                                                                      i*2-30, j*cell_size+j*2+30), 5)

        timer.tick(60)

        if(result==0):
            result = is_finished(terrain)
            if(result==-1):
                result=2
            if(result==1 or result==2):
                wins[result-1]+=1
        if(result):
            if(result==-2):
                draw_string = "egalite"
            else:
                draw_string = "player "+str(result)+" wins"
        else:
            draw_string = "player "+str(player % 2+1)

        score = str(wins[0])+"   |   "+str(wins[1])


        text = font.render(draw_string, True, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.y = window_width+20
        screen.blit(text, text_rect)

        text2 = font.render(score, True, BLACK)
        text2_rect = text2.get_rect()
        text2_rect.centerx = screen.get_rect().centerx
        text2_rect.y = window_width+120
        screen.blit(text2, text2_rect)

        pygame.display.update()
    pygame.quit()

game()