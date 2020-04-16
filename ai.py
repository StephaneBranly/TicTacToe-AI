import numpy as np
print("ai.py imported")


# Notre classe de réseau neuronal


class Neural_Network(object):
    def __init__(self):

        # Nos paramètres
        self.inputSize = 9  # Nombre de neurones d'entrée
        self.outputSize = 2  # Nombre de neurones de sortie
        self.hiddenSize = 5  # Nombre de neurones cachés

    # Nos poids
        self.W1 = np.random.randn(self.inputSize, self.hiddenSize)
        self.W2 = np.random.randn(self.hiddenSize, self.outputSize)

    # Fonction de propagation avant
    def forward(self, X):

        # Multiplication matricielle entre les valeurs d'entrer et les poids W1
        self.z = np.dot(X, self.W1)
        # Application de la fonction d'activation (Sigmoid)
        self.z2 = self.sigmoid(self.z)
        # Multiplication matricielle entre les valeurs cachés et les poids W2
        self.z3 = np.dot(self.z2, self.W2)
        # Application de la fonction d'activation, et obtention de notre valeur de sortie final
        o = self.sigmoid(self.z3)
        return o

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
        self.z2_error = self.o_delta.dot(self.W2.T)
        # Application de la dérivée de la sigmoid à cette erreur
        self.z2_delta = self.z2_error*self.sigmoidPrime(self.z2)

        self.W1 += X.T.dot(self.z2_delta)  # On ajuste nos poids W1
        self.W2 += self.z2.T.dot(self.o_delta)  # On ajuste nos poids W2

    # Fonction d'entrainement
    def train(self, X, y):
        o = self.forward(X)
        self.backward(X, y, o)

    # Fonction de prédiction
    def predict(self, xPrediction):
        return [int(self.forward(xPrediction)[0]*3), int(self.forward(xPrediction)[1] * 3)]
