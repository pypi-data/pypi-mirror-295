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

    params = _format_list_params(params)

    # Load data
    if params["type"] == "nc":
        ds = load_netcdf(params["f"])
    elif params["type"] == "olacdf4":
        params.update({"tplot" :"scatter"})
        ds = load_ola(params["f"], 
                olagrp=params["olagrp"],
                setid=params["setid"],
                time=params["time"])
    else:
        params.update({"tplot" :"scatter"})
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
            {params["var"]: (("z", "pt"), obj.GetVar(params["var"]))},
            coords={"longitude": (("pt"), obj.ptlon), "latitude": (("pt"), obj.ptlat)},
        )

    map2d = Map2d()
    map2d.set_param(params)
    fig, _ = map2d.plot(ds, params["var"])

    if not params["FigShow"]:
        output = os.path.join(params["DFigOUT"], params["FigOUTName"] + ".png")
        fig.savefig(output, bbox_inches="tight")
        plt.close(fig)
    else:
        plt.show()


def _format_list_params(params):
    """ format param values as list"""

    param_list_str = ["setid", "title"]
    param_list_float = ["time", "vminmax", "extent"]
    for k, v in params.items():
        if k in param_list_str:
            if isinstance(v, str):
                params[k] = v.split(' ')
        if k in param_list_float:
            if isinstance(v, str):
                params[k] = [float(val) for val in v.split(' ')]
    return params


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

