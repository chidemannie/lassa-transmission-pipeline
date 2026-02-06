import re
import sys
import xarray as xr
import geopandas as gpd
import rioxarray
import pandas as pd
import os
from pathlib import Path

# --- CLI input ---
ERA5_FILE = sys.argv[1]

m = re.search(r"era5_nigeria_(\d{4})_(\d{2})_daily\.nc$", ERA5_FILE)
if not m:
    raise ValueError(f"Cannot extract year/month from filename: {ERA5_FILE}")

year, month = m.group(1), m.group(2)

SHAPEFILE = "data/external/boundaries/gadm41_NGA_1.shp"
OUTDIR = "data/processed/era5/state_daily"
Path(OUTDIR).mkdir(parents=True, exist_ok=True)

OUTFILE = os.path.join(OUTDIR, f"era5_state_daily_{year}_{month}.csv")

# Load ERA5 daily grid
ds = xr.open_dataset(ERA5_FILE)

# Ensure CRS metadata exists for clipping
ds = ds.rio.set_spatial_dims(x_dim="longitude", y_dim="latitude")
ds = ds.rio.write_crs("EPSG:4326")

# Load state polygons
states = gpd.read_file(SHAPEFILE).to_crs("EPSG:4326")

records = []

for _, row in states.iterrows():
    state = row["NAME_1"]
    geom = row.geometry

    clipped = ds.rio.clip([geom], states.crs, drop=True)

    # mean across grid cells within the polygon for each day
    df = (
        clipped[["rain_mm", "temp_c"]]
        .mean(dim=["latitude", "longitude"], skipna=True)
        .to_dataframe()
        .reset_index()
    )

    df["state"] = state
    records.append(df)

out = pd.concat(records, ignore_index=True)
out = out[["state", "time", "rain_mm", "temp_c"]].sort_values(["state", "time"])
out.to_csv(OUTFILE, index=False)

print(f"Saved: {OUTFILE}")
print("Rows:", len(out), "States:", out['state'].nunique(), "Days:", out['time'].nunique())

