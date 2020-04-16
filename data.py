import numpy as np
X = np.array(([[0,  0,  0,  0,  0,  0, 0, 0, 0],
               [-1, 0, 0,  0, 0,  0, 0, 0, 0],
               [0, 0,  0, 0, 0, 0,  0,  0, 0],
               [1, 0, 0,  0, -1, 0, 0, 0, 0],
               [1, 1, 0, 0, -1, 0, -1, 0, 0]]), dtype=int)  # données d'entrer
# données de sortie /  1 = rouge /  0 = bleu
y = np.array(([[0.5,    0.5],
               [0.5,   0.5],
               [0.5, 0.5],
               [1, 0.],
               [0.5, 0.]]), dtype=float)
