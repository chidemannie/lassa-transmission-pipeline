import numpy as np

def seir_weekly(
    T,
    forcing,
    N=2.0e7,
    beta0=0.35,
    sigma=1/2.0,
    gamma=1/3.0,
    I0=100,
    E0=200,
    R0=0,
):
    """
    Discrete-time weekly SEIR model.
    forcing: array of length T multiplying beta0 (climate or baseline)
    """

    S = np.zeros(T)
    E = np.zeros(T)
    I = np.zeros(T)
    R = np.zeros(T)

    S[0] = N - E0 - I0 - R0
    E[0] = E0
    I[0] = I0
    R[0] = R0

    for t in range(T - 1):
        beta_t = beta0 * forcing[t]
        new_E = beta_t * S[t] * I[t] / N
        new_I = sigma * E[t]
        new_R = gamma * I[t]

        S[t+1] = max(S[t] - new_E, 0)
        E[t+1] = max(E[t] + new_E - new_I, 0)
        I[t+1] = max(I[t] + new_I - new_R, 0)
        R[t+1] = max(R[t] + new_R, 0)

    return S, E, I, R
