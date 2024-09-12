# ease_plot

ease_plot is a very simple and lightweight library to make 2D map plots (scatter/contour).

## Getting started

In a python >= 3.10.4 environment just do:

```
pip install ease_plot
```

# Command line with map2d

map2d is an entrypoint to the map2d function that loads and plot different type of files (gridded netcdf, OLA, cmx, cpmx and cmz).
For help, please type:

```
map2d --help

usage: maps [-h] -f F [--grid GRID] [--type {cmx,cmz,cpmx,nc,ola}] [-v V] [--setid [SETID ...]] [--nl NL] [--nt NT] [--title [TITLE ...]] [--vminmax VMINMAX VMINMAX] [--oper {None,sqrt,sq,abs}] [--tplot {pcolor,scatter}] [--msize MSIZE] [--nreduce NREDUCE] [--cmap CMAP]
            [--extent EXTENT EXTENT EXTENT EXTENT] [--clon CLON] [--nbc NBC] [--proj PROJ] [--DFigOUT DFIGOUT] [--FigOUTName FIGOUTNAME] [--FigShow | --no-FigShow]

options:
  -h, --help            show this help message and exit
  -f F                  file to read
  --grid GRID           grid file (canevas.grd in the case of cmxz)
  --type {cmx,cmz,cpmx,nc,ola}
                        supported files
  -v V                  variable to plot
  --setid [SETID ...]   List of setid
  --nl NL               z level in variable
  --nt NT               time index in variable
  --title [TITLE ...]   Title figure
  --vminmax VMINMAX VMINMAX
                        min/max for plotting
  --oper {None,sqrt,sq,abs}
                        Operations : sqrt,sq,abs
  --tplot {pcolor,scatter}
  --msize MSIZE         Size of marker for scatter plots
  --nreduce NREDUCE     Number of points to decimate (optimization)
  --cmap CMAP           Colormap one per var if wanted
  --extent EXTENT EXTENT EXTENT EXTENT
                        min/max for plotting
  --clon CLON           central lon for proj
  --nbc NBC             Colorbar number of intervals
  --proj PROJ           Projection
  --DFigOUT DFIGOUT     If present figures will be saved in DFigout directory
  --FigOUTName FIGOUTNAME
                        Name of the output file
  --FigShow, --no-FigShow
                        Use this to not view the fig in the screen (default: False)

```

# Use in a python script

```
import xarray as xr
from ease_plot.class_plot_map import Map2d

ds = xr.open_dataset(filename)

map2d = Map2d()

params = {'nl': 0,
   'nt': 0,
   'title': [''],
   'vminmax': [-1.0, 1.0],
   'oper': 'None',
   'tplot': 'pcolor',
   'msize': 0.05,
   'nreduce': 1,
   'cmap': 'MO_greyed70_middle_rev',
   'extent': [-180.0, 180.0, -80.0, 80.0],
   'clon': 0,
   'nbc': 21,
   'proj': 'PlateCarree',
   'figsize': "auto",
   'coeff_fontsize': 1,
   'xtick_interv': 45,
   'ytick_interv': 30,
   'land_color': "lightgrey",
   'coast_color': "black"}

fig, _ = map2d.plot(ds, variable)
fig.savefig("test.png", bbox_inches="tight")

```

# Gallery
## Colormaps
Available colormaps in ease_plot:

![colormaps](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/colormaps.png?ref_type=heads)

## Examples

### NetCDF gridded files:

```
map2d -f /ec/res4/hpcperm/ars4/cnes_obs-sl_glo_phy-mdt_my_0.125deg_P20Y_1703146258243.nc --proj PlateCarree -v mdt --vminmax -1 1 --cmap MO_greyed70_middle_rev --title MDT CNES --DFigOUT ./ --FigOUTName example_nc1 --nbc 21 --extent -180 180 -80 80
```

![example_nc1](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_nc1.png?ref_type=heads)


```
map2d -f /ec/res4/hpcperm/ars4/cnes_obs-sl_glo_phy-mdt_my_0.125deg_P20Y_1703146258243.nc --proj PlateCarree -v mdt --vminmax -1 1 --cmap MO_greyed70_middle_rev --title MDT CNES --DFigOUT ./ --FigOUTName example_nc2 --nbc 21 --extent -50 30 -10 60
```
![example_nc2](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_nc2.png?ref_type=heads)

```
map2d -f /ec/res4/hpcperm/ars4/iORCA025/R20201224/000GLO4_1d_20201224_20201230_gridT_20201224-20201224.nc -v thetao --nl 7 --vminmax 22 30 --cmap cmocean_thermal --title Temperature at level 7 --DFigOUT ./ --FigOUTName example_nc3 --nbc 21 --extent 90 180 0 50
```

![example_nc3](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_nc3.png?ref_type=heads)

```
map2d -f /ec/res4/hpcperm/ars4/NOOBS_TEST/OLA/000iORCA025_QCOLA_IS_BEST_R20170503.nc --type ola --proj PlateCarree --tplot scatter --msize 0.05 -v obs --setid SLA/s3a SLA/j3 --vminmax -0.5 0.5 --cmap MO_sla --title SLA obs from s3a/j3 --DFigOUT ./ --FigOUTName example_qcola --nbc 21 --extent -180 180 -80 80
```

### OLA NetCDF

![example_qcola](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_qcola.png?ref_type=heads)

```
map2d -f /ec/res4/scratch/toji/TEST_DEPLOY_ens_a7500c83d1/GLO4/TEST_DEPLOY_ens/R20240530M000_050/REA/BEST/CDF/M000/000GLO4_1d-m_2DT-siconc_20240527-20240527.nc --proj SouthPolarStereo -v siconc --vminmax 0.5 1 --cmap ODV_GEBCO3_r --title Sea ice Concentration --DFigOUT ./ --FigOUTName example_SPS --nbc 21 --extent -180 180 -90 -50
```

### Polar projection

![example_SPS](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_SPS.png)

```
map2d -f /ec/res4/scratch/toji/TEST_DEPLOY_ens_a7500c83d1/GLO4/TEST_DEPLOY_ens/R20240530M000_050/REA/CMXZ/M001/BEST/001delta_C27171.0_27178.0_D27175.0_TEMSAL_OCE_M000_050.cmx --type cmx --grid /ec/res4/scratch/toji/TEST_DEPLOY_ens_a7500c83d1/GLO4/staticinput/assim/canevas_iORCA025_meshmask_v3.1_fullgrid.grd --nl 5 --tplot scatter -v TEM --vminmax -1 1 --cmap MO_greyed70_middle_rev --title TEM delta --DFigOUT ./ --FigOUTName example_cmx --nbc 21 --extent -180 180 -80 80
```

### CMX files

![example_cmx](https://gitlab.mercator-ocean.fr/internal/ease_plot/-/raw/main/gallery/example_cmx.png?ref_type=heads)