# Exercise 5
from pathlib import Path
import numpy as np
import pandas as pd
import xarray as xr
import urllib.request
# import functions from utils here

data_dir = Path("data")
solution_dir = Path("solution")

# 1. Go to http://surfobs.climate.copernicus.eu/dataaccess/access_eobs.php#datafiles and 
#    download the 0.25 deg. file for daily mean temperature. Save the file into the data directory
#    but don't commit it to github. [2P]
urllib.request.urlretrieve("https://www.ecad.eu/download/ensembles/data/Grid_0.25deg_reg_ensemble/tg_ens_mean_0.25deg_reg_v19.0e.nc", data_dir/"tg_ens_mean_0.25deg_reg_v19.0e.nc")

# 2. Read the file using xarray. Get to know your data. What's in the file?
data = xr.open_dataset(data_dir/"tg_ens_mean_0.25deg_reg_v19.0e.nc")
#    Calculate monthly means for the reference periode 1981-2010 for Europe (Extent: Lon_min:-13, Lon_max: 25, Lat_min: 30, Lat_max: 72). [2P]
data_crop = data.sel(latitude=slice(30,72),longitude=slice(-13,25),time=slice("1981-01-01","2010-12-31"))
means = data_crop.groupby("time.month").mean("time")

# 3. Calculate monthly anomalies for 2018 for the reference period and extent in #2.
#    Make a quick plot of the anomalies for the region. [2P]
data_18 = data.sel(latitude=slice(30,72),longitude=slice(-13,25),time=slice("2018-01-01","2018-12-31")).groupby("time.month").mean("time")
anom_18 = data_18 - means
anom_18["tg"].plot(x="longitude", col="month")

# 4. Calculate the mean anomaly for the year 2018 for Europe and compare it to the anomaly of the element which contains
#    Marburg. Is the anomaly of Marburg lower or higher than the one for Europe? [2P] 
mean_anom_18 = anom_18.mean()["tg"]
mean_anom_18_marb = anom_18.sel(latitude = 50.81, longitude = 8.77, method = "nearest").mean()

if mean_anom_18_marb["tg"] > mean_anom_18:
    print("The mean anomaly for Marburg is higher than for Europe")
else:
    print("The mean anomaly of Europe is higher than for Marburg")

# 5. Write the monthly anomalies from task 3 to a netcdf file with name "europe_anom_2018.nc" to the solution directory.
#    Write the monthly anomalies for Marburg to a csv file with name "marburg_anom_2018.csv" to the solution directory. [2P]
anom_18.to_netcdf(solution_dir/"europe_anom_2018.nc")
anom_18.sel(latitude= 50.80, longitude=8.77, method="nearest").to_dataframe()["tg"].to_csv(solution_dir/"marburg_anom_2018.csv", header=True)
