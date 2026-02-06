import os
import re
import sys
import zipfile
import xarray as xr

def parse_year_month(zip_path: str) -> str:
    """
    Extract YYYY_MM from filenames like:
    era5_nigeria_2018_01.zip
    """
    m = re.search(r"(\d{4}_\d{2})", os.path.basename(zip_path))
    if not m:
        raise ValueError(f"Could not parse YYYY_MM from filename: {zip_path}")
    return m.group(1)

def ensure_unzipped(zip_path: str, out_dir: str) -> None:
    """
    Unzip only if needed.
    """
    os.makedirs(out_dir, exist_ok=True)

    needed = {
        "data_stream-oper_stepType-instant.nc",
        "data_stream-oper_stepType-accum.nc",
    }

    existing = set(os.listdir(out_dir))
    if needed.issubset(existing):
        return

    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(out_dir)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/aggregate_era5_zip_month_to_daily.py <path_to_zip>")
        sys.exit(1)

    zip_path = sys.argv[1]
    if not os.path.exists(zip_path):
        raise FileNotFoundError(zip_path)

    ym = parse_year_month(zip_path)

    in_dir = f"data/external/era5/daily/unzipped/{ym}"
    out_dir = "data/processed/era5/daily"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"era5_nigeria_{ym}_daily.nc")

    ensure_unzipped(zip_path, in_dir)

    instant_path = os.path.join(in_dir, "data_stream-oper_stepType-instant.nc")
    accum_path = os.path.join(in_dir, "data_stream-oper_stepType-accum.nc")

    instant = xr.open_dataset(instant_path, engine="netcdf4")
    accum = xr.open_dataset(accum_path, engine="netcdf4")

    # ERA5 sometimes uses 'valid_time' instead of 'time'
    if "valid_time" in instant.coords:
        instant = instant.rename({"valid_time": "time"})
    if "valid_time" in accum.coords:
        accum = accum.rename({"valid_time": "time"})

    # Hourly -> daily
    t_daily = instant.resample(time="1D").mean()
    p_daily = accum.resample(time="1D").sum()

    # Unit conversions
    rain_mm = p_daily["tp"] * 1000.0      # meters -> mm
    temp_c = t_daily["t2m"] - 273.15      # Kelvin -> Celsius

    out = xr.Dataset({"rain_mm": rain_mm, "temp_c": temp_c})
    out.to_netcdf(out_file)
    print(f"Saved: {out_file}")

if __name__ == "__main__":
    main()

