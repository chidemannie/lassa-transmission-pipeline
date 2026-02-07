### Python pipeline to simulate Lassa fever dynamics under climate and ecological scenarios
# Lassa Transmission Pipeline

**Climate-informed early warning signals for Lassa fever in Nigeria**

---

## Overview

Lassa fever remains one of Nigeria’s most persistent endemic zoonotic diseases, with marked spatial and seasonal heterogeneity. While surveillance systems capture reported cases, they often lack integrated, climate-informed analytics that can support **anticipatory action and early warning**.

This repository provides a **reproducible data pipeline** that links weekly Lassa fever surveillance data with high-resolution climate reanalysis data to support:

- exploratory analysis of climate–disease relationships  
- lagged climate signal assessment  
- development of early warning indicators suitable for operational use  

The pipeline is designed to be **extensible**, allowing new surveillance data (post-2021) or additional climate variables to be incorporated without restructuring the workflow.

---

## Why Lassa Fever Is Climate-Sensitive

Lassa fever transmission is influenced by ecological and climatic factors that affect the population dynamics and behavior of its primary rodent reservoir (*Mastomys* spp.). Rainfall patterns, temperature variability, and seasonal transitions shape food availability, rodent reproduction, and human–rodent contact, contributing to observed seasonal and geographic variation in Lassa fever incidence.

Understanding how **lagged climate signals** relate to human cases is critical for moving from reactive outbreak response toward **forecast-informed preparedness and prevention**.

---

## Repository Purpose

The purpose of this repository is to provide a **transparent, end-to-end analytical pipeline** that integrates epidemiological surveillance data with climate reanalysis data to:

- quantify temporal associations between climate variables and Lassa fever incidence  
- generate state-level, weekly datasets suitable for modeling and early warning analysis  
- serve as a foundation for predictive and scenario-based extensions  

This repository is intended for use by researchers, public health practitioners, and funders interested in **climate-sensitive infectious disease risk**, **early warning systems**, and **anticipatory humanitarian and health action**.

---

## Data Inputs

### 1. Lassa Fever Surveillance Data

Weekly, state-level Lassa fever case data for Nigeria (2018–2021):

> Chioma Dan-Nwafor (2022).  
> *Epidemiological data on Lassa fever in Nigeria, 2018–2021*.  
> Zenodo. https://doi.org/10.5281/zenodo.7309567

Raw surveillance data are **not included** in this repository and must be obtained directly from the source.

---

### 2. Administrative boundaries

State-level aggregation of climate variables uses the GADM v4.1 Nigeria
administrative boundary shapefile (level 1).

The shapefile is used only during preprocessing to spatially aggregate
ERA5 gridded climate data to Nigerian states. No shapefile data are
required for downstream analysis or modeling.

Source:
GADM – Global Administrative Areas  
https://gadm.org

### 3. Climate Data (ERA5)

Climate variables are derived from the **ERA5 reanalysis dataset** produced by the European Centre for Medium-Range Weather Forecasts (ECMWF), accessed via the Copernicus Climate Data Store.

Variables currently used include:
- total precipitation (rainfall)
- near-surface air temperature

ERA5 data must be downloaded separately. See `data/external/README.md` for detailed instructions.

---

## Pipeline Structure
lassa-transmission-pipeline/
├── README.md
├── environment.yml
├── requirements.txt
├── data/
│ ├── external/ # raw data (not version-controlled)
│ └── processed/ # derived datasets (not version-controlled)
├── scripts/
│ ├── process_lassa_weekly_state.py
│ ├── make_lassa_weekly_balanced_panel.py
│ ├── aggregate_era5_zip_month_to_daily.py
│ ├── era5_daily_to_state_daily.py
│ └── aggregate_era5_state_daily_to_weekly.py
├── notebooks/
│ ├── 01_exploration.ipynb
│ ├── 02_lag_analysis.ipynb
│ └── 03_early_warning_demo.ipynb
└── .gitignore

Each component serves a distinct role:

- `scripts/` contains fully reproducible data-processing steps
- `notebooks/` demonstrate exploratory analysis, lag assessment, and early warning concepts
- `data/` is intentionally excluded from version control to respect data governance, with clear instructions for reproduction

---

## Key Outputs

The pipeline produces:

- weekly, state-level Lassa fever case counts  
- weekly, state-level climate summaries (rainfall and temperature)  
- a **balanced state–week panel** suitable for statistical modeling  
- lagged climate features for early warning analysis  

Final modeling-ready datasets are written to:
data/processed/model/

---

## Reproducibility

This repository is designed to be **fully reproducible**:

- All data transformations are scripted  
- Raw data are excluded but fully documented  
- Software dependencies are specified in `environment.yml` and `requirements.txt`  
- Analytical steps are demonstrated in Jupyter notebooks  

A user with access to the original data sources can reproduce the full pipeline from raw inputs to modeling-ready outputs.

---

## Extensibility and Early Warning Use

The pipeline supports:

- ingestion of **new surveillance data beyond 2021**  
- incorporation of additional climate variables (e.g., soil moisture, vegetation indices)  
- development of **forecast-based early warning indicators**  

The design enables future extensions toward **probabilistic forecasting**, **scenario analysis**, and **operational early warning dashboards**.

---

## GitHub Justification (for Reviewers)

This GitHub repository provides a transparent, reproducible implementation of a climate–health data integration pipeline for Lassa fever in Nigeria. By separating raw data access from scripted processing and analysis, the repository enables independent verification, reuse, and extension while respecting data governance constraints. The structure, documentation, and modular design align with best practices for open, reproducible research and support translation from retrospective analysis to forward-looking early warning applications.

---

## License

This repository is released under the MIT License. See `LICENSE` for details.

---

## Acknowledgements

Lassa fever surveillance data were obtained from publicly available datasets curated by Chioma Dan-Nwafor and colleagues. Climate data were sourced from the ECMWF ERA5 reanalysis via the Copernicus Climate Data Store.