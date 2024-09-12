# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=90:


import re

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from cartopy import crs as ccrs
import cartopy.feature as cfeature


class Map2d:
    def __init__(self):
        """ """
        dict_param = {
            "nl": 0,
            "nt": 0,
            "title": "",
            "vminmax": None,
            "oper": "None",
            "tplot": "pcolor",
            "msize": 0.05,
            "nreduce": 1,
            "cmap": "MPL_YlGnBu",
            "extent": [-180, 180, -90, 90],
            "clon": 0,
            "nbc": 21,
            "proj": "PlateCarree",
            "figsize": "auto",
            "coeff_fontsize": 1,
            "xtick_interv": 45,
            "ytick_interv": 30,
            "land_color": "lightgrey",
            "coast_color": "black",
            "ndim": 0,
        }
        self.params = dict_param

    def set_param(self, d):
        """
        Update Map2d parameters using a dictionnary.
        """
        self.params.update(d)

    def _set_fig_size(self, extent):
        """
        Automatically set the size of the figure given extent parameter.
        """

        dlon = extent[1] - extent[0]
        dlat = extent[3] - extent[2]
        clat = extent[2] + dlat / 2
        ratio_width = dlon / dlat
        corr_lat = np.cos(np.deg2rad(clat))
        ratio_width /= corr_lat
        fs = (10, np.round(12 / ratio_width, 1))
        return fs, ratio_width

    def plot(self, ds, v):
        """
        Plot variable v of ds dataset using Mapd2d.params parameters.
        """

        from ease_plot.class_cmaps import Cmaps

        # cmaps
        cmaps = Cmaps()
        cmap = cmaps.dict_cmaps[self.params["cmap"]]

        projnam = self.params["proj"]
        figsize = self.params["figsize"]
        coeff_fontsize = self.params["coeff_fontsize"]
        clon = self.params["clon"]
        title = self.params["title"]
        nreduce = int(self.params["nreduce"])
        extent = self.params["extent"]
        tplot = self.params["tplot"]
        vminmax = self.params["vminmax"]
        nbc = self.params["nbc"]

        if figsize == "auto":
            if not re.search("Polar", projnam):
                figsize, ratio_width = self._set_fig_size(extent)
                offset_title = -0.025 * (len(title[0]) > 0)
                y_stat = -0.05 * ratio_width + offset_title
            else:
                figsize = (9, 9)
                y_stat = -0.05
        else:
            assert type(figsize) == tuple
            assert len(figsize) == 2
            y_stat = -0.07 * 12 / figsize[1]

        # adapt arguments
        proj0 = ccrs.PlateCarree()
        proj = eval("ccrs." + projnam + "(" + str(clon) + ")")
        title = " ".join(title)

        ds_plt = self.format(ds, v, self.params["oper"])
        # make stats
        minval, maxval, weighted_mean = self.make_stats(ds_plt, extent)
        if vminmax is None:
            vminmax = [minval, maxval]

        # Apply reduction for optimization
        if nreduce > 1:
            ds_plt = self.reduce(ds_plt, nreduce)

        fig, ax = plt.subplots(1, 1, figsize=figsize, subplot_kw={"projection": proj})

        # Cartopy features (land, coast)
        land = cfeature.NaturalEarthFeature(
            "physical",
            "land",
            "50m",
            edgecolor=None,
            facecolor=self.params["land_color"],
        )
        coast = cfeature.NaturalEarthFeature(
            category="physical", scale="50m", facecolor="none", name="coastline"
        )
        ax.add_feature(land)
        ax.add_feature(coast, edgecolor=self.params["coast_color"], linewidth=0.5)

        if tplot == "pcolor":
            im = ds_plt.data.plot.pcolormesh(
                ax=ax,
                vmin=vminmax[0],
                vmax=vminmax[1],
                levels=nbc,
                transform=proj0,
                x="longitude",
                y="latitude",
                add_colorbar=False,
                cmap=cmap,
            )
        elif tplot == "scatter":
            im = ax.scatter(
                ds_plt.longitude,
                ds_plt.latitude,
                s=ds_plt.msize,
                c=ds_plt.data,
                vmin=vminmax[0],
                vmax=vminmax[1],
                transform=proj0,
                cmap=cmap,
            )

        if not re.search("Polar", projnam):
            xticks = np.arange(-180, 180, self.params["xtick_interv"])
            xlabels = [str(l) + "E" if l < 0 else str(l) + "W" for l in xticks]
            ax.set_xticks(xticks, crs=proj0)
            ax.set_xticklabels(xlabels, color="gray")
            yticks = np.arange(-90, 90, self.params["ytick_interv"])
            ylabels = [str(l) + "S" if l < 0 else str(l) + "N" for l in yticks]
            ax.set_yticks(yticks, crs=proj0)
            ax.set_yticklabels(ylabels, color="gray")

            ax.grid(linewidth=0.5, color="gray", alpha=0.5, linestyle="--")
        else:
            gl = ax.gridlines(
                draw_labels=True,
                crs=proj0,
                linewidth=0.5,
                color="gray",
                alpha=0.5,
                linestyle="--",
                rotate_labels=False,
                xlocs=range(-180, 180, 60),
                ylocs=range(-90, 90, 10),
            )
            gl.xlabel_style = {"fontsize": 8 * coeff_fontsize}
            gl.ylabel_style = {"fontsize": 8 * coeff_fontsize}
            theta = np.linspace(0, 2 * np.pi, 100)
            center, radius = [0.5, 0.5], 0.5
            verts = np.vstack([np.sin(theta), np.cos(theta)]).T
            circle = mpath.Path(verts * radius + center)
            ax.set_boundary(circle, transform=ax.transAxes)

        ax.set_extent(extent, crs=proj0)
        axpos = ax.get_position(original=True)
        pos_x = axpos.x0 + axpos.width + 0.02
        pos_y = axpos.y0
        cax_width = 0.02
        cax_height = axpos.height
        pos_cax = fig.add_axes([pos_x, pos_y, cax_width, cax_height])

        cb = plt.colorbar(im, cax=pos_cax)
        ax.set_aspect("auto", adjustable=None)

        fontdict = {"weight": "bold", "size": 16 * coeff_fontsize}
        ax.set_title(title, fontdict=fontdict)

        # Display infos (kind in bold)
        kwargs_text = {"fontsize": 10 * coeff_fontsize, "transform": ax.transAxes}
        ax.text(
            0.1,
            y_stat,
            r"$\bf{Min}$: " + str(minval),
            **kwargs_text,
            horizontalalignment="left"
        )
        ax.text(
            0.5,
            y_stat,
            r"$\bf{Mean}$: " + str(weighted_mean),
            **kwargs_text,
            horizontalalignment="center"
        )
        ax.text(
            0.9,
            y_stat,
            r"$\bf{Max}$: " + str(maxval),
            **kwargs_text,
            horizontalalignment="right"
        )

        return fig, ax

    def sort_longitude(self, lon, lat, var):
        """
        Sort longitude in ascending order.
        """
        if (len(lon.shape) > 1) & (len(lat.shape) > 1):
            nparange = np.arange(lon.shape[0])[:, None]
            npargsort = np.argsort(lon)
            lon = lon[nparange, npargsort]
            lat = lat[nparange, npargsort]
            var = var[nparange, npargsort]
        else:
            nparange = np.arange(lon.shape[0])
            npargsort = np.argsort(lon)
            lon, lat = np.meshgrid(lon[npargsort], lat)
            var = var[:, npargsort]

        return lon, lat, var

    def format(self, ds, v, oper):
        """
        Format data in order to use xarray plotting functions.
        """
        from siphonf.loaders.rncdf import get_dim_name

        nl, nt = int(self.params["nl"]), int(self.params["nt"])
        tplot = self.params["tplot"]

        dims = get_dim_name(ds)
        dict_sel = {}
        if dims["z"]:
            dict_sel.update({dims["z"]: nl})
        if dims["t"]:
            dict_sel.update({dims["t"]: nt})

        ds = ds.isel(dict_sel)
        coordx = ds[dims["coordx"]].values
        coordy = ds[dims["coordy"]].values
        data = ds[v].values
        ndim = len(data.shape)
        assert ndim in [1, 2]

        msize = float(self.params["msize"]) * np.ones(data.shape)

        # Apply oper
        data = self.apply_oper(data, oper)

        # Sort longitude if needed
        if ndim == 2:
            coordx, coordy, data = self.sort_longitude(coordx, coordy, data)

            ds_plt = xr.Dataset(
                {"data": (("lat", "lon"), data)},
                coords={
                    "longitude": (("lat", "lon"), coordx),
                    "latitude": (("lat", "lon"), coordy),
                    "msize": (("lat", "lon"), msize),
                },
            )
        elif ndim == 1:
            assert tplot == "scatter"
            ds_plt = xr.Dataset(
                {"data": (("pt"), data)},
                coords={
                    "longitude": (("pt"), coordx),
                    "latitude": (("pt"), coordy),
                    "msize": (("pt"), msize),
                },
            )

        self.params["ndim"] = ndim

        return ds_plt

    def reduce(self, ds, nreduce):
        """
        Decimate data using nreduce parameter.
        """
        if self.params["ndim"] == 2:
            ds = ds.isel(lat=slice(None, None, nreduce), lon=slice(None, None, nreduce))
        elif self.params["ndim"] == 1:
            ds = ds.isel(pt=slice(None, None, nreduce))

        return ds

    def apply_oper(self, data, oper):
        """
        Apply an operation on data.
        """
        dic_oper = {
            "abs": lambda x: abs(x),
            "sq": lambda x: x**2,
            "sqrt": lambda x: x**0.5,
        }

        if oper != "None":
            if oper == "sqrt":
                data[data > 0] = dic_oper[oper](data[data > 0])
                data[data < 0] = -dic_oper[oper](-data[data < 0])
            else:
                data = dic_oper[oper](data)

        return data

    def make_stats(self, ds, extent):
        """
        Make statistics on a formatted dataset (see format function) over a domain defined
        with extent array [lon0, lon1, lat0, lat1].
        """
        # mask ds with extent
        msk = (
            (ds.longitude > extent[0])
            | (ds.longitude < extent[1])
            | (ds.latitude > extent[2])
            | (ds.latitude < extent[3])
        )
        ds = ds.where(msk)

        if self.params["ndim"] == 2:
            # Gridded data
            weights = np.cos(np.deg2rad(ds.latitude))
            weights.name = "weights"
            ds_weighted = ds.weighted(weights)
            mean = np.round(float(ds_weighted.mean(("lon", "lat")).data.values), 3)
        elif self.params["ndim"] == 1:
            # Vector data
            mean = np.round(float(np.nanmean(ds.data)), 3)

        minval, maxval = np.round(float(np.nanmin(ds.data)), 3), np.round(
            float(np.nanmax(ds.data)), 3
        )

        return minval, maxval, mean
