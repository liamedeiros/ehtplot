import numpy as np

def load(name, component=None):
    if component is None:
        return np.loadtxt(name+"/model_B.tsv.gz")
    else:
        return np.loadtxt(name+"/model_B."+component+".tsv.gz")
