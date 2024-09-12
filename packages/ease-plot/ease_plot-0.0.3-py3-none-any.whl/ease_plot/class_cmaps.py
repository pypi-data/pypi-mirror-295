#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import os, sys

import matplotlib as mpl
import matplotlib.cm as cm_mat
import matplotlib.pyplot as plt
import numpy as np


# # Author: C.REGNIER
# # Feb 2019


class Cmaps(object):
    def __init__(self):
        """
        Add new color palettes in matplotlib registry
        """
        # # Load externals palettes
        list_pal = Statics().get_all_palettes()
        self.dict_cmaps = {}
        for pal in list_pal:
            self.register(pal)
        self._list = self.dict_cmaps.keys()
        self._order_list = sorted(self._list)

    def register(self, file):
        """
        Add new palette in matplotlib registry
        """
        list_clm = plt.colormaps()
        name_pal = os.path.basename(file).split(".")[0]
        if name_pal not in list_clm:
            my_cmap = self.compute_cmap(file, name_pal)
            my_cmap_r = self.reverse_colourmap(my_cmap)
            cm_mat.register_cmap(name=name_pal, cmap=my_cmap)
            cm_mat.register_cmap(name=name_pal + "_r", cmap=my_cmap_r)
            self.dict_cmaps[name_pal] = my_cmap
            self.dict_cmaps[name_pal + "_r"] = my_cmap_r
        else:
            my_cmap = self.compute_cmap(file, name_pal)
            my_cmap_r = self.reverse_colourmap(my_cmap)
            self.dict_cmaps[name_pal] = my_cmap
            self.dict_cmaps[name_pal + "_r"] = my_cmap_r

    def reverse_colourmap(self, cmap, name="my_cmap_r"):
        """
        In:
        cmap, name
        Out:
        my_cmap_r
        Explanation:
        t[0] goes from 0 to 1
        row i:   x  y0  y1 -> t[0] t[1] t[2]
                       /
                      /
        row i+1: x  y0  y1 -> t[n] t[1] t[2]
        so the inverse should do the same:
        row i+1: x  y1  y0 -> 1-t[0] t[2] t[1]
                       /
                      /
        row i:   x  y1  y0 -> 1-t[n] t[2] t[1]
        """
        reverse = []
        k = []
        for key in cmap._segmentdata:
            k.append(key)
            channel = cmap._segmentdata[key]
            data = []
            for t in channel:
                data.append((1 - t[0], t[2], t[1]))
            reverse.append(sorted(data))

        LinearL = dict(zip(k, reverse))
        my_cmap_r = mpl.colors.LinearSegmentedColormap(name, LinearL)
        return my_cmap_r

    def filter(self, frame):
        """
        Filter dictionnary
        """
        filtered_dict = {k: v for (k, v) in self.dict_cmaps.items() if frame in k}
        return filtered_dict.keys()

    def compute_cmap(self, file, colormap):
        """
        Read colormaps_<name>.pal file and compute cmap
        """
        LinL = np.loadtxt(file)
        if np.max(LinL[:, :]) > 1.1:
            LinL[:, :] = LinL[:, :] / 255
        b3 = LinL[:, 2]
        b2 = LinL[:, 2]
        b1 = np.linspace(0, 1, len(b2))
        g3 = LinL[:, 1]
        g2 = LinL[:, 1]
        g1 = np.linspace(0, 1, len(g2))
        r3 = LinL[:, 0]
        r2 = LinL[:, 0]
        r1 = np.linspace(0, 1, len(r2))
        # Creating list
        R = zip(r1, r2, r3)
        G = zip(g1, g2, g3)
        B = zip(b1, b2, b3)
        # Transposition list
        RGB = zip(R, G, B)
        rgb = zip(*RGB)
        # Dictionnary
        k = ["red", "green", "blue"]
        LinearL = dict(zip(k, rgb))
        return mpl.colors.LinearSegmentedColormap(colormap, LinearL)

    @property
    def list(self):
        """
        Print added colormaps
        """
        return self._list

    def get_mplcolors(self, name_pal):
        """
        Return mplcolor of a colormap
        """
        return self.dict_cmaps[name_pal]

    @list.setter
    def list(self, file):
        """
        Add new palette in the registry
        """
        self.register(file)
        self._list = self.dict_cmaps.keys()
        return self._list

    @property
    def order_list(self):
        """
        Print ordered colormaps
        """
        return self._order_list

    def select_list(self, frame):
        """
        Select added colormaps
        """
        filtered_dict = self.filter(frame)
        return filtered_dict

    def show(self):
        """
        Show registered palettes
        """
        a = np.outer(np.arange(0, 1, 0.001), np.ones(10))
        plt.figure(figsize=(20, 20))
        plt.subplots_adjust(top=0.95, bottom=0.05, left=0.01, right=0.99)
        ncmaps = len(self.dict_cmaps.keys())
        nrows = 8
        for i, k in enumerate(sorted(self.dict_cmaps.keys())):
            cmaps = self.dict_cmaps[k]
            plt.subplot(nrows, ncmaps // nrows + 1, i + 1)
            plt.axis("off")
            plt.imshow(a, aspect="auto", cmap=k, origin="lower")
            plt.title(k, rotation=90, fontsize=10)
            plt.title(k, fontsize=10)
        # plt.show()
        plt.savefig("colormaps.png", dpi=300)
        plt.close()


class Statics(object):

    """Class to access static resources"""

    def __init__(self):
        """
        Constructor to build the shape
        """
        self.dir = os.path.dirname(os.path.abspath(__file__))
        self.palettes_dir = os.path.join(self.dir, "../statics")

    def get_resource(self, resource_name):
        return os.path.join(self.dir, resource_name)

    def get_palette(self, palette_name):
        return os.path.join(self.palettes_dir, palette_name)

    def get_all_palettes(self):
        return glob(os.path.join(self.palettes_dir, "*.pal"))
