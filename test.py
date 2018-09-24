from scipy.io import loadmat
import DataManupulation
mat = loadmat('Data/Subject_04847/data-starplus-04847-v7.mat')

mata = DataManupulation.getMata(mat)
print (mata)