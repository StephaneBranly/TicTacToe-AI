import numpy as np
import pygame

print("ai.py imported")


class Neural_Network(object):
    def __init__(self):

        # Nos paramètres
        self.inputSize = 9  # Nombre de neurones d'entrée
        self.outputSize = 9  # Nombre de neurones de sortie
        self.hidden1Size = 3  # Nombre de neurones cachés
        self.hidden2Size = 2  # Nombre de neurones cachés
        # self.hidden3Size = 5  # Nombre de neurones cachés

    # Nos poids
        self.W1 = np.random.randn(self.inputSize, self.hidden1Size)
        self.W2 = np.random.randn(self.hidden1Size, self.hidden2Size)
        self.W3 = np.random.randn(self.hidden2Size, self.outputSize)
        #self.W4 = np.random.randn(self.hidden3Size, self.outputSize)

    # Fonction de propagation avant
    def forward(self, X):

        # Multiplication matricielle entre les valeurs d'entrer et les poids W1
        self.z = np.dot(X, self.W1)
        self.z2 = self.sigmoid(self.z)
        self.z3 = np.dot(self.z2, self.W2)
        self.z4 = self.sigmoid(self.z3)
        self.z5 = np.dot(self.z4, self.W3)
        #self.z6 = self.sigmoid(self.z5)
        #self.z7 = np.dot(self.z6, self.W4)
        self.o = self.sigmoid(self.z5)
        return self.o

    # Fonction d'activation
    def sigmoid(self, s):
        return 1/(1+np.exp(-s))

    # Dérivée de la fonction d'activation
    def sigmoidPrime(self, s):
        return s * (1 - s)

    # Fonction de rétropropagation
    def backward(self, X, y, o):
        self.o_error = y - o  # Calcul de l'erreur
        # Application de la dérivée de la sigmoid à cette erreur
        self.o_delta = self.o_error*self.sigmoidPrime(o)

        # Calcul de l'erreur de nos neurones cachés
        #self.z4_error = self.o_delta.dot(self.W4.T)
        # Application de la dérivée de la sigmoid à cette erreur
        #self.z4_delta = self.z4_error*self.sigmoidPrime(self.z6)

        # Calcul de l'erreur de nos neurones cachés
        self.z3_error = self.o_delta.dot(self.W3.T)
        # Application de la dérivée de la sigmoid à cette erreur
        self.z3_delta = self.z3_error*self.sigmoidPrime(self.z4)

        # Calcul de l'erreur de nos neurones cachés
        self.z2_error = self.z3_error.dot(self.W2.T)
        # Application de la dérivée de la sigmoid à cette erreur
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2)

        self.W1 += X.T.dot(self.z2_delta)  # On ajuste nos poids W1
        self.W2 += self.z2.T.dot(self.z3_delta)  # On ajuste nos poids W2
        self.W3 += self.z4.T.dot(self.o_delta)  # On ajuste nos poids W3
        # self.W4 += self.z6.T.dot(self.o_delta)  # On ajuste nos poids W4

    # Fonction d'entrainement
    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    # Fonction de prédiction
    def predict(self, xPrediction):
        prediction = self.forward(xPrediction)
        index_max = np.argmax(prediction)
        return [int(index_max//3), int(index_max % 3)]

    def draw_network(self, screen, x, y, width, height, terrain):
        for j in range(self.inputSize):
            if(terrain[j] == -1):
                COLOR = (255, 0, 0)
            elif(terrain[j] == 1):
                COLOR = (0, 0, 255)
            else:
                COLOR = (120, 120, 120)
            pygame.draw.circle(
                screen, COLOR, (int(x+width/6),
                                int(y+(height/(self.inputSize+1))*(j+1))), 20)
            pygame.draw.circle(screen, (0, 0, 0), (int(x+width/6),
                                                   int(y+(height/(self.inputSize+1))*(j+1))), 20, 1)
        size_tab = [self.hidden1Size, self.hidden2Size, self.outputSize]
        result = self.predict(terrain)
        color_tab = [self.z2, self.z4, self.o]
        xdec = 2
        for i in size_tab:
            for j in range(i):

                COLOR = (int(color_tab[xdec-2][j]*255),
                         0, int(color_tab[xdec-2][j]*255))

                pygame.draw.circle(
                    screen, COLOR, (int(x+(width/6)*xdec),
                                    int(y+(height/(i+1))*(j+1))), 20)
                if(xdec == 4 and j == result[0]*3+result[1]):
                    pygame.draw.circle(
                        screen, (255, 0, 0), (int(x+(width/6)*xdec),
                                              int(y+(height/(i+1))*(j+1))), 20, 5)
                else:
                    pygame.draw.circle(
                        screen, (0, 0, 0), (int(x+(width/6)*xdec),
                                            int(y+(height/(i+1))*(j+1))), 20, 1)
            xdec += 1
