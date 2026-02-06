import pandas as pd
from pathlib import Path
import glob

IN_DIR = "data/processed/era5/state_daily"
OUTFILE = "data/processed/era5/era5_state_weekly_2018_2021.csv"

files = sorted(glob.glob(f"{IN_DIR}/era5_state_daily_*.csv"))
assert len(files) > 0, "No ERA5 state-daily files found"

dfs = []
for f in files:
    df = pd.read_csv(f, parse_dates=["time"])
    dfs.append(df)

df = pd.concat(dfs, ignore_index=True)

# ISO year/week
iso = df["time"].dt.isocalendar()
df["year"] = iso.year
df["week"] = iso.week

weekly = (
    df.groupby(["state", "year", "week"], as_index=False)
      .agg(
          rain_mm=("rain_mm", "sum"),   # weekly total rainfall
          temp_c=("temp_c", "mean")     # weekly mean temperature
      )
)

Path("data/processed/era5").mkdir(parents=True, exist_ok=True)
weekly = weekly.sort_values(["state", "year", "week"])
weekly.to_csv(OUTFILE, index=False)

print("Saved:", OUTFILE)
print("States:", weekly["state"].nunique())
print("Rows:", len(weekly))

