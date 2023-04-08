import filepickle
import numpy as np
word_matrix = filepickle.load('output/matrix.dump')

co_matrix = word_matrix > 0

m = np.matmul(co_matrix,co_matrix.T) # co incidence

