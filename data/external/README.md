# External Data Sources

This project relies on two external data sources that are **not included in this repository** due to size, licensing, and data governance considerations.

## 1. Lassa Fever Surveillance Data

Weekly Lassa fever surveillance data were obtained from a publicly archived dataset:

**Citation**  
Chioma Dan-Nwafor. (2022). *Epidemiological data on Lassa fever in Nigeria, 2018–2021*.  
Zenodo. https://doi.org/10.5281/zenodo.7309567

Users should download the dataset directly from Zenodo and place the source file in:
data/external/lassa/
The pipeline expects the original SPSS `.sav` file format.

---

## 2. Climate Reanalysis Data (ERA5)

Climate variables are derived from the **ERA5 reanalysis dataset** provided by the Copernicus Climate Data Store (CDS).

**Source**  
Copernicus Climate Change Service (C3S), ECMWF  
https://cds.climate.copernicus.eu/

### Required variables
- Total precipitation (`tp`)
- 2-metre air temperature (`t2m`)

### Spatial and temporal scope
- Country: Nigeria
- Temporal resolution: hourly (aggregated to daily and weekly)
- Period: 2018–2021

ERA5 data must be downloaded manually via the CDS API or web interface and placed under:
data/external/era5/

The provided processing scripts convert raw ERA5 NetCDF files into state-level daily and weekly summaries compatible with the Lassa surveillance data.

---

## Reproducibility Note

No raw data are stored in this repository.  
All downstream datasets can be reproduced by following the instructions above and running the processing scripts in the `scripts/` directory.


