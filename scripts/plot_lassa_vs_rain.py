import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/model/lassa_era5_weekly_panel_2018_2021.csv"
)

state = "Edo"
sub = df[df["state"] == state]

fig, ax1 = plt.subplots(figsize=(10,4))

ax1.plot(sub["week"], sub["cases"])
ax1.set_ylabel("Lassa cases")

ax2 = ax1.twinx()
ax2.plot(sub["week"], sub["rain_mm"], alpha=0.5)
ax2.set_ylabel("Rainfall (mm)")

plt.title(f"Lassa cases vs rainfall – {state}")
plt.tight_layout()
plt.show()

