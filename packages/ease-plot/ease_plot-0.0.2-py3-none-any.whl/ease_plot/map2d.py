# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=90:


def map2d(params):
    """
    """

    import os
    import xarray as xr
    import matplotlib
    import matplotlib.pyplot as plt
    from ease_plot.class_plot_map import Map2d

    from siphonf.loaders.rncdf import load_netcdf, load_ola
    from siphonf.loaders.rcmxz import Cmxz
    from siphonf.loaders.rcpmx import Cpmx

    map2d = Map2d()
    map2d.set_param(params)

    # Load data
    if params["type"] == "nc":
        ds = load_netcdf(params["f"])
    elif params["type"] == "ola":
        assert params["tplot"] == "scatter"
        ds = load_ola(params["f"], setid=params["setid"])
    else:
        assert params["tplot"] == "scatter"
        if params["type"] == "cmx":
            obj = Cmxz(params["grid"])
            obj.OpenCMXZ(params["f"])
        elif params["type"] == "cmz":
            obj = Cmxz(params["grid"])
            obj.OpenCMZ(params["f"])
        elif params["type"] == "cpmx":
            obj = Cpmx(params["grid"])
            obj.OpenCPMX(params["f"])
        ds = xr.Dataset(
            {params["v"]: (("z", "pt"), obj.GetVar(params["v"]))},
            coords={"longitude": (("pt"), obj.ptlon), "latitude": (("pt"), obj.ptlat)},
        )

    fig, _ = map2d.plot(ds, params["v"])

    if not params["FigShow"]:
        output = os.path.join(params["DFigOUT"], params["FigOUTName"] + ".png")
        fig.savefig(output, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()


def main():
    """
    """

    import sys
    import time
    from ease_plot.getopts import check_argsmaps

    T0 = time.time()

    params = check_argsmaps(sys.argv[1:])
    print(params)

    map2d(params)

    T1 = time.time()
    print(f"Elapsed: {round(T1-T0, 3)} sec.")

