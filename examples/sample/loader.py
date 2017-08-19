import numpy as np

def load(name):
    return np.loadtxt(name+"/model_B.tsv.gz")
