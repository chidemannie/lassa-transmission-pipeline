from pathlib import Path
import cdsapi

OUTDIR = Path("data/external/era5/daily")
OUTDIR.mkdir(parents=True, exist_ok=True)

# Nigeria bounding box in CDS order: [North, West, South, East]
NGA_BBOX = [14.0, 2.5, 4.0, 15.0]

# Years/months to download
YEARS = [2018, 2019, 2020, 2021]
MONTHS = list(range(1, 13))

# Keep this small to avoid queue pain:
# We'll request just what we need for modelling
VARS_INSTANT = ["2m_temperature"]
VARS_ACCUM = ["total_precipitation"]

c = cdsapi.Client()

def download_month(year: int, month: int):
    ym = f"{year}_{month:02d}"
    outzip = OUTDIR / f"era5_nigeria_{ym}.zip"

    if outzip.exists() and outzip.stat().st_size > 0:
        print(f"Skip (exists): {outzip}")
        return

    print(f"Requesting ERA5 month for {ym} ...")

    # CDS often returns a ZIP when multiple streams are requested.
    # We request both variables in a single call (works for your pipeline).
    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": VARS_INSTANT + VARS_ACCUM,
            "year": str(year),
            "month": f"{month:02d}",
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": [f"{h:02d}:00" for h in range(0, 24)],
            "area": NGA_BBOX,
            "format": "netcdf",  # CDS may still wrap into a zip depending on stream separation
        },
        str(outzip),
    )
    print(f"Saved: {outzip}")

if __name__ == "__main__":
    for y in YEARS:
        for m in MONTHS:
            download_month(y, m)

