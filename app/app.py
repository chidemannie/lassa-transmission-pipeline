import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lassa Early Warning Demo", layout="wide")
st.title("Lassa Fever Early Warning Demo (Template-in → Signal-out)")
st.caption("Upload weekly state-level climate + cases. App computes simple alert signals (demo baseline).")

st.markdown("### Upload a weekly panel CSV")
st.markdown("Expected columns: `state, year, week, cases, rain_mm, temp_c`")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    required = {"state","year","week","cases","rain_mm","temp_c"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Missing columns: {sorted(list(missing))}")
        st.stop()

    df["state"] = df["state"].astype(str).str.strip()
    df = df.sort_values(["state","year","week"]).reset_index(drop=True)

    st.success(f"Loaded {len(df):,} rows across {df['state'].nunique()} states.")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("### Simple early warning signals (demo)")
    st.write("This demo flags unusually high cases using a rolling baseline per state.")

    window = st.slider("Baseline window (weeks)", 4, 26, 8)

    def add_alerts(g):
        g = g.copy()
        g["cases_roll_mean"] = g["cases"].rolling(window, min_periods=window).mean()
        g["cases_roll_std"]  = g["cases"].rolling(window, min_periods=window).std()
        g["z_cases"] = (g["cases"] - g["cases_roll_mean"]) / g["cases_roll_std"]
        g["alert"] = (g["z_cases"] >= 2.0).fillna(False)  # 2-sigma rule (demo)
        return g

    out = df.groupby("state", group_keys=False).apply(add_alerts)

    alerts = out[out["alert"] == True][["state","year","week","cases","z_cases","rain_mm","temp_c"]]
    st.markdown("#### Alerts (z ≥ 2, demo rule)")
    st.dataframe(alerts, use_container_width=True)

    st.download_button(
        "Download results CSV",
        data=out.to_csv(index=False).encode("utf-8"),
        file_name="early_warning_results.csv",
        mime="text/csv",
    )

    st.markdown("### Quick plots")
    sel_state = st.selectbox("Select state", sorted(out["state"].unique()))
    ss = out[out["state"] == sel_state].copy()
    ss["t"] = range(len(ss))
    st.line_chart(ss.set_index("t")[["cases"]])
    st.line_chart(ss.set_index("t")[["rain_mm","temp_c"]])

else:
    st.info("Tip: you can start by uploading `data/processed/model/lassa_era5_weekly_panel_2018_2021.csv` (locally).")
