# -*- coding: utf-8 -*-
# vim: set ts=4 sw=4 tw=90:
""" module implements check args for diferent plots """
import argparse


# str to define help msg
h_logger_level = "Set the logging level"


def check_argsmaps(args):
    """get arguments for 2d plots"""
    parser = argparse.ArgumentParser(prog="maps")
    parser.add_argument("-f", required=True, help="file to read")
    parser.add_argument(
        "--grid",
        type=str,
        default="",
        help="grid file (canevas.grd in the case of cmxz)",
    )
    parser.add_argument(
        "--type",
        type=str,
        default="nc",
        choices=["cmx", "cmz", "cpmx", "nc", "olacdf4"],
        help="supported files",
    )
    parser.add_argument("-v", "--var", type=str, default="None", help="variable to plot")
    parser.add_argument("--olagrp", type=str, default="None", help="group in ola file")
    parser.add_argument(
        "--setid", nargs="*", type=str, default=None, help="List of setid"
    )
    parser.add_argument('--time', nargs=2, type=float, default=None, help='time_min time_max')
    parser.add_argument("--nl", type=int, default=0, help="z level in variable")
    parser.add_argument("--nt", type=int, default=0, help="time index in variable")
    parser.add_argument("--title", nargs="*", default=[""], help="Title figure")
    parser.add_argument(
        "--vminmax", nargs=2, type=float, default=None, help="min/max for plotting"
    )
    parser.add_argument(
        "--oper",
        default="None",
        choices=["None", "sqrt", "sq", "abs"],
        help="Operations : sqrt,sq,abs",
    )
    parser.add_argument(
        "--tplot", default="pcolor", choices=["pcolor", "scatter"], type=str
    )
    parser.add_argument(
        "--msize", default=0.05, help="Size of marker for scatter plots"
    )
    parser.add_argument(
        "--nreduce", default=1, help="Number of points to decimate (optimization)"
    )
    parser.add_argument(
        "--cmap", type=str, default="MPL_YlGnBu", help="Colormap one per var if wanted"
    )
    parser.add_argument(
        "--extent",
        nargs=4,
        type=float,
        default=[-180, 180, -80, 80],
        help="min/max for plotting",
    )
    parser.add_argument("--clon", type=float, default=0, help="central lon for proj")
    parser.add_argument(
        "--nbc", type=int, default=21, help="Colorbar number of intervals"
    )
    parser.add_argument("--proj", type=str, default="PlateCarree", help="Projection")
    parser.add_argument(
        "--DFigOUT",
        type=str,
        default="./",
        help="If present figures will be saved in DFigout directory",
    )
    parser.add_argument(
        "--FigOUTName", type=str, default="test_map2d", help="Name of the output file"
    )
    parser.add_argument(
        "--FigShow",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Use this to not view the fig in the screen",
    )

    return vars(parser.parse_args(args))
