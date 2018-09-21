from scipy.io import loadmat
import DataManupulation
mat = loadmat('Data/data-starplus-05710-v7.mat')

mata = DataManupulation.getMata(mat)
print (mata)