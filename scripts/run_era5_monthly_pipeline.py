from pathlib import Path
import subprocess
import sys

ZIP_DIR = Path("data/external/era5/daily")
zips = sorted(ZIP_DIR.glob("era5_nigeria_????_??.zip"))

if not zips:
    print("No zip files found in", ZIP_DIR)
    sys.exit(1)

for z in zips:
    print("\n=== Processing:", z.name, "===")

    # 1) zip month -> daily nc
    subprocess.run(
        ["python3", "scripts/aggregate_era5_zip_month_to_daily.py", str(z)],
        check=True
    )

    # 2) daily nc -> state daily csv
    subprocess.run(
        ["python3", "scripts/era5_daily_to_state_daily.py"],
        check=True
    )

print("\nDone. Now run weekly aggregation:")
print("python3 scripts/aggregate_era5_state_daily_to_weekly.py")

