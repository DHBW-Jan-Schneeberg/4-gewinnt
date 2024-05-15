import numpy as np

field = np.array([[0, 0, 0], [0, 1, 0]])

a = field[0, :].nonzero()

print(a)

