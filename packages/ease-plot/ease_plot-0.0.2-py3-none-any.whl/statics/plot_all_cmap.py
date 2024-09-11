import os, sys

sys.path.append("../../../../")
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

from tools import compute_cmap
import matplotlib.cm as cm_mat
from glob import glob
import numpy as np
from matplotlib import colors
import inspect

## C.REGNIER Feb 2019
## Code to plot cmaps inpired by cmaps module
## https://github.com/hhuangwx/cmaps

if __name__ == "__main__":

    list_pal = glob("/home/cregnier/SVN/mo/LIB/LIB_PYT/statics/palettes/*.pal")
    ## Register
    dict_cmaps = {}
    for pal in list_pal:
        print("Palette %s " % (pal))
        name_pal = os.path.basename(pal).split(".")[0]
        my_cmap = compute_cmap(pal, name_pal)
        cm_mat.register_cmap(name=name_pal, cmap=my_cmap)
        dict_cmaps[name_pal] = my_cmap
    ## Plot Cmap
    a = np.outer(np.arange(0, 1, 0.001), np.ones(10))
    plt.figure(figsize=(20, 20))
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.01, right=0.99)
    ncmaps = len(dict_cmaps.keys())
    nrows = 8
    for i, k in enumerate(dict_cmaps.keys()):
        cmaps = dict_cmaps[k]
        plt.subplot(nrows, ncmaps // nrows + 1, i + 1)
        plt.axis("off")
        # plt.imshow(a, aspect='auto', cmap=getattr(cmaps, k), origin='lower')
        plt.imshow(a, aspect="auto", cmap=k, origin="lower")
        plt.title(k, rotation=90, fontsize=10)
        plt.title(k, fontsize=10)
    plt.savefig("colormaps.png", dpi=300)
