import os
import cdsapi

# Nigeria bounding box (N, W, S, E)
AREA = [14.0, 2.5, 4.0, 15.0]
OUTDIR = "data/external/era5/daily"
os.makedirs(OUTDIR, exist_ok=True)

c = cdsapi.Client()

def download_month(year: int, month: int) -> None:
    outfile = os.path.join(OUTDIR, f"era5_nigeria_{year}_{month:02d}.nc")
    if os.path.exists(outfile):
        print(f"Skipping {year}-{month:02d}, exists: {outfile}")
        return

    print(f"Requesting ERA5 hourly (for daily aggregation) for {year}-{month:02d} ...")
    c.retrieve(
        "reanalysis-era5-single-levels",
        {
            "product_type": "reanalysis",
            "variable": [
                "total_precipitation",
                "2m_temperature",
            ],
            "year": str(year),
            "month": f"{month:02d}",
            "day": [f"{d:02d}" for d in range(1, 32)],
            "time": [f"{h:02d}:00" for h in range(24)],
            "area": AREA,
            "format": "netcdf",
        },
        outfile,
    )
    print(f"Saved: {outfile}")

if __name__ == "__main__":
    # Start with ONE month as a proof-of-download
    download_month(2021, 1)

