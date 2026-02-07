# Model Equations and Structure

This repository implements a simplified, climate-modulated SEIR framework for exploratory analysis and early warning demonstrations.

---

## SEIR Compartment Definitions

Let:

- **S(t)**: Susceptible population
- **E(t)**: Exposed (infected but not yet infectious)
- **I(t)**: Infectious population
- **R(t)**: Removed (recovered or deceased)
- **N**: Total population

---

## Baseline SEIR Dynamics (Discrete Weekly Time)

At weekly time step *t*:

S(t+1) = S(t) − β(t) · S(t) · I(t) / N  
E(t+1) = E(t) + β(t) · S(t) · I(t) / N − σ · E(t)  
I(t+1) = I(t) + σ · E(t) − γ · I(t)  
R(t+1) = R(t) + γ · I(t)

Where:

- **β(t)**: Time-varying transmission rate
- **σ**: Progression rate from exposed to infectious
- **γ**: Recovery/removal rate

---

## Climate-Driven Transmission Modulation

The transmission rate is decomposed as:

β(t) = β₀ · F(t)

Where:

- **β₀** is the baseline transmission rate
- **F(t)** is a climate forcing function

### Climate Forcing Function

Rainfall and temperature are standardized:

Z_rain(t) = (rain(t) − μ_rain) / σ_rain  
Z_temp(t) = (temp(t) − μ_temp) / σ_temp  

The forcing function is:

F(t) = exp( a_rain · Z_rain(t) + a_temp · Z_temp(t) )

F(t) is normalized so that:

mean(F(t)) = 1

This ensures that climate modifies transmission intensity without changing the long-term average.

---

## Interpretation

- **Baseline transmission:** β₀ governs non-climatic transmission
- **Climate-amplified transmission:** F(t) increases or decreases β(t)
- **Early warning relevance:** Peaks or sustained increases in F(t) may precede observed outbreaks

---

## Intended Use

This model is designed for:
- Pattern comparison with observed surveillance data
- Scenario analysis under alternative climate trajectories
- Demonstration of climate-informed early warning concepts

It is **not** intended as a calibrated predictive forecasting model in its current form.
