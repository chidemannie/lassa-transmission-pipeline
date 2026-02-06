import pandas as pd
import geopandas as gpd
from pathlib import Path

INFILE = "data/processed/lassa/lassa_weekly_state_2018_2021.csv"
SHAPEFILE = "data/external/boundaries/gadm41_NGA_1.shp"
OUTFILE = "data/processed/lassa/lassa_weekly_state_2018_2021_balanced.csv"

df = pd.read_csv(INFILE)

# Canonical state list from shapefile
shape = gpd.read_file(SHAPEFILE)
states = sorted(shape["NAME_1"].str.strip().unique())

# Determine ISO year/week range
min_year = int(df["year"].min())
max_year = int(df["year"].max())

weeks = []
for y in range(min_year, max_year + 1):
    for w in range(1, 54):
        try:
            pd.Timestamp.fromisocalendar(y, w, 1)
            weeks.append((y, w))
        except ValueError:
            pass

weeks = pd.DataFrame(weeks, columns=["year", "week"])

# Full state × year × week grid
panel = (
    pd.MultiIndex.from_product(
        [states, weeks["year"].unique(), weeks["week"].unique()],
        names=["state", "year", "week"]
    )
    .to_frame(index=False)
)

# Merge observed cases
out = panel.merge(df, on=["state", "year", "week"], how="left")
out["cases"] = out["cases"].fillna(0).astype(int)

Path("data/processed/lassa").mkdir(parents=True, exist_ok=True)
out = out.sort_values(["state", "year", "week"])
out.to_csv(OUTFILE, index=False)

print("Saved:", OUTFILE)
print("States:", out["state"].nunique())
print("Years:", out["year"].nunique())
print("Total rows:", len(out))
print("Total confirmed cases:", out["cases"].sum())

