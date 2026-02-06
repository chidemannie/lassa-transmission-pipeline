import pyreadstat
import pandas as pd

# Load Lassa line-list
df, meta = pyreadstat.read_sav(
    "data/external/lassa/Lassa Fever_Dataset_NCDC.sav"
)

# Extract state labels
state_labels = meta.variable_value_labels["Stateofresidence_updated_new"]

# Map numeric codes to names
df["state"] = df["Stateofresidence_updated_new"].map(state_labels)

# Fix capitalization / consistency
df["state"] = (
    df["state"]
    .str.strip()
    .str.title()
    .replace({
	"Fct": "Federal Capital Territory",
	"Akwa-Ibom": "Akwa Ibom"
    })
)

# Parse report date
df["report_date"] = pd.to_datetime(
    df["DateofreportMdyyyy"],
    errors="coerce"
)

# Keep confirmed cases only
df = df[df["case_classification_recode"] == 1]

# Drop rows without state or date
df = df.dropna(subset=["state", "report_date"])

# Derive ISO year and week
iso = df["report_date"].dt.isocalendar()
df["year"] = iso.year
df["week"] = iso.week

# Aggregate to weekly state counts
weekly = (
    df.groupby(["state", "year", "week"])
      .size()
      .reset_index(name="cases")
)

# Save
out = "data/processed/lassa/lassa_weekly_state_2018_2021.csv"
weekly.to_csv(out, index=False)

print("Saved:", out)
print("Rows:", len(weekly))
print("States:", weekly["state"].nunique())
print("Years:", weekly["year"].unique())

