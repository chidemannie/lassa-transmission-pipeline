from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Dict, Tuple

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


# -------------------------
# Model
# -------------------------
@dataclass(frozen=True)
class SEIRParams:
    sigma: float  # 1/incubation_period
    gamma: float  # 1/infectious_period


def seir_rhs(t: float, y: np.ndarray, N: float, params: SEIRParams, beta_t: Callable[[float], float]) -> np.ndarray:
    S, E, I, R = y
    beta = float(beta_t(t))
    lam = beta * (I / N)

    dS = -lam * S
    dE = lam * S - params.sigma * E
    dI = params.sigma * E - params.gamma * I
    dR = params.gamma * I

    return np.array([dS, dE, dI, dR], dtype=float)


def simulate_seir(t_days: np.ndarray, y0: Tuple[float, float, float, float], N: float, params: SEIRParams, beta_t: Callable[[float], float]) -> Dict[str, np.ndarray]:
    sol = solve_ivp(
        fun=lambda t, y: seir_rhs(t, y, N=N, params=params, beta_t=beta_t),
        t_span=(float(t_days[0]), float(t_days[-1])),
        y0=np.array(y0, dtype=float),
        t_eval=t_days,
        method="RK45",
        rtol=1e-7,
        atol=1e-9,
    )
    if not sol.success:
        raise RuntimeError(sol.message)

    S, E, I, R = sol.y
    return {"t": t_days, "S": S, "E": E, "I": I, "R": R}


# -------------------------
# Forcing
# -------------------------
@dataclass(frozen=True)
class ForcingParams:
    beta0: float
    season_amp: float
    season_phase: float
    climate_coeff: float


def seasonal_factor(t: float, amp: float, phase: float) -> float:
    return 1.0 + amp * np.sin(2.0 * np.pi * (t - phase) / 365.0)


def climate_index(t: float, shock: float = 0.0) -> float:
    return np.sin(2.0 * np.pi * t / 365.0) + shock


def make_beta_function(forcing: ForcingParams, climate_shock: float = 0.0, intervention_start: float | None = None, intervention_effect: float = 0.0) -> Callable[[float], float]:
    def beta_t(t: float) -> float:
        seas = seasonal_factor(t, forcing.season_amp, forcing.season_phase)
        clim = climate_index(t, shock=climate_shock)
        clim_term = np.exp(forcing.climate_coeff * clim)
        beta = forcing.beta0 * seas * clim_term

        if intervention_start is not None and t >= intervention_start:
            beta = beta * (1.0 - intervention_effect)

        return float(max(beta, 0.0))

    return beta_t


# -------------------------
# Runner
# -------------------------
def ensure_dirs() -> None:
    os.makedirs("outputs/figures", exist_ok=True)
    os.makedirs("outputs/tables", exist_ok=True)


def main() -> None:
    ensure_dirs()

    t_days = np.arange(0, 365 + 1, 1)

    N = 1_000_000.0
    I0, E0, R0 = 10.0, 20.0, 0.0
    S0 = N - I0 - E0 - R0
    y0 = (S0, E0, I0, R0)

    epi = SEIRParams(sigma=1.0 / 10.0, gamma=1.0 / 14.0)

    forcing = ForcingParams(
        beta0=0.35,
        season_amp=0.20,
        season_phase=30.0,
        climate_coeff=0.25,
    )

    scenarios = {
        "baseline": dict(climate_shock=0.0, intervention_start=None, intervention_effect=0.0),
        "wetter_climate": dict(climate_shock=0.5, intervention_start=None, intervention_effect=0.0),
        "intervention": dict(climate_shock=0.0, intervention_start=180.0, intervention_effect=0.30),
    }

    outputs: Dict[str, Dict[str, np.ndarray]] = {}

    for name, sc in scenarios.items():
        beta_t = make_beta_function(
            forcing=forcing,
            climate_shock=sc["climate_shock"],
            intervention_start=sc["intervention_start"],
            intervention_effect=sc["intervention_effect"],
        )
        outputs[name] = simulate_seir(t_days=t_days, y0=y0, N=N, params=epi, beta_t=beta_t)

    # Save summary CSV
    rows = []
    for name, res in outputs.items():
        I = res["I"]
        peak_I = float(I.max())
        peak_day = int(res["t"][int(I.argmax())])
        rows.append({"scenario": name, "peak_I": peak_I, "peak_day": peak_day})

    df = pd.DataFrame(rows).sort_values("scenario")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    table_path = f"outputs/tables/summary_{stamp}.csv"
    fig_path = f"outputs/figures/infectious_curves_{stamp}.png"

    df.to_csv(table_path, index=False)

    # Plot
    plt.figure()
    for name, res in outputs.items():
        plt.plot(res["t"], res["I"], label=name)
    plt.xlabel("Day")
    plt.ylabel("Infectious (I)")
    plt.title("SEIR simulations with seasonal + climate forcing")
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)
    plt.close()

    print("Done.")
    print(f"Saved: {table_path}")
    print(f"Saved: {fig_path}")


if __name__ == "__main__":
    main()
