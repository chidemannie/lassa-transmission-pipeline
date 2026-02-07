# Data Sources

This repository uses publicly available epidemiological and climate datasets. Raw data are not redistributed; instead, scripts reproduce all processed outputs.

---

## Lassa Fever Surveillance Data

**Citation (primary):**  
Chioma Dan-Nwafor. (2022).  
*Epidemiological data on Lassa fever in Nigeria, 2018–2021*.  
Zenodo.  
https://doi.org/10.5281/zenodo.7309567

**Description:**
- Weekly reported Lassa fever cases
- State-level aggregation
- Coverage: Nigeria, 2018–2021

**Usage in pipeline:**
- Aggregated to state-week and national-week levels
- Missing weeks assumed to represent zero reported cases
- Used for exploratory analysis, lag analysis, and model validation

---

## Climate Data (ERA5 Reanalysis)

**Source:**  
Copernicus Climate Change Service (C3S)  
ERA5 Reanalysis – Single Levels

**Variables used:**
- Total precipitation (`tp`)
- 2-meter air temperature (`t2m`)

**Access:**
- Downloaded via the Copernicus CDS API
- Monthly NetCDF files aggregated to daily and weekly summaries

**Usage in pipeline:**
- Spatially aggregated to Nigerian state boundaries
- Weekly mean temperature and weekly total rainfall computed
- Used to construct lagged and rolling climate features

---

## Geographic Boundaries

**Source:**  
GADM v4.1 – Global Administrative Areas  
https://gadm.org

**Usage:**
- Nigerian state polygons (admin level 1)
- Used for spatial aggregation of gridded ERA5 climate data

---

## Reproducibility Note

All processed datasets in `data/processed/` are generated exclusively from the sources above using scripts included in this repository.
