import xarray as xr
import os
import glob

IN_GLOB = "data/external/era5/daily/era5_nigeria_*.nc"
OUTDIR = "data/processed/era5/daily"
os.makedirs(OUTDIR, exist_ok=True)

files = sorted(glob.glob(IN_GLOB))
if not files:
    raise SystemExit(f"No files found at {IN_GLOB}")

for infile in files:
    base = os.path.basename(infile).replace(".nc", "")
    outfile = os.path.join(OUTDIR, f"{base}_daily.nc")
    if os.path.exists(outfile):
        print(f"Skipping daily agg, exists: {outfile}")
        continue
try:
    ds = xr.open_dataset(infile, engine="netcdf4")
except Exception:
    ds = xr.open_dataset(infile, engine="h5netcdf")

    daily = ds.resample(time="1D").agg({"tp": "sum", "t2m": "mean"})
    daily["rain_mm"] = daily["tp"] * 1000.0
    daily["temp_c"] = daily["t2m"] - 273.15
    daily = daily[["rain_mm", "temp_c"]]

    daily.to_netcdf(outfile)
    print(f"Saved: {outfile}")

