# Model Assumptions

This repository implements a climate-informed Lassa fever transmission pipeline and a simplified SEIR-style simulation framework. The following assumptions underpin the data processing, analysis, and modeling steps.

---

## Epidemiological Assumptions

1. **Weekly aggregation is appropriate**  
   Lassa fever surveillance data and climate drivers are aggregated to epidemiological weeks. This assumes that week-level resolution captures meaningful transmission dynamics without excessive noise.

2. **Reported cases approximate true incidence trends**  
   Surveillance data are assumed to reflect temporal trends in Lassa fever transmission, acknowledging underreporting and reporting delays.

3. **Human-to-human transmission is represented implicitly**  
   The SEIR model represents aggregate transmission dynamics without explicitly modeling hospital- or household-level transmission.

---

## Climate–Disease Assumptions

4. **Rainfall and temperature influence transmission indirectly**  
   Climate variables affect Lassa transmission through ecological and behavioral pathways (e.g., rodent population dynamics, human–rodent contact), represented as a modulation of the transmission rate.

5. **Lagged climate effects matter**  
   Climate effects are not instantaneous. Lagged rainfall and temperature variables (1–8 weeks) are used to capture delayed ecological responses.

6. **Climate forcing is multiplicative, not deterministic**  
   Climate does not cause outbreaks directly; it modifies baseline transmission intensity.

---

## Modeling Assumptions

7. **Homogeneous national mixing (baseline SEIR)**  
   The current SEIR implementation assumes national-level mixing. Spatial heterogeneity is handled upstream in the data pipeline but not yet in the dynamic model.

8. **Fixed transition rates**  
   Incubation and recovery rates are held constant across time and space for interpretability.

9. **Scaling is for pattern comparison, not case prediction**  
   Simulated infection curves are scaled to observed cases for shape comparison, not exact incidence forecasting.

---

## Scope and Limitations

- This framework is designed for **early warning and scenario analysis**, not real-time operational forecasting.
- Extensions to rodent–human coupled models, spatial SEIR, and Bayesian inference are planned future work.
