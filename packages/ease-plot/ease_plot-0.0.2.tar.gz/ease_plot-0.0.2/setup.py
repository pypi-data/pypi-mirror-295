from setuptools import setup

setup(
    install_requires=[
        "numpy",
        "matplotlib",
        "xarray>=2024.6.0",
        "netcdf4",
        "cartopy",
        "siphonf",
    ],
    python_requires=">=3.10.4",
)
