import numpy as np
import pandas as pd
from scipy.integrate import odeint
from scipy.optimize import brute
import matplotlib.pyplot as plt

# Étape 1: Lire les données avec les bons noms de colonnes
data = pd.read_csv('sird_dataset.csv')  # Assurez-vous que le fichier est bien dans le répertoire
jours = data['Jour'].values
S_obs = data['Susceptibles'].values
I_obs = data['Infectés'].values
R_obs = data['Rétablis'].values
D_obs = data['Décès'].values

# Étape 2: Implémenter le modèle SIRD
def sird_model(y, t, N, beta, gamma, mu):
    S, I, R, D = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I - mu * I
    dRdt = gamma * I
    dDdt = mu * I
    return dSdt, dIdt, dRdt, dDdt

def solve_sird(N, beta, gamma, mu, S0, I0, R0, D0, t):
    y0 = (S0, I0, R0, D0)
    ret = odeint(sird_model, y0, t, args=(N, beta, gamma, mu))
    S, I, R, D = ret.T
    return S, I, R, D

# Étape 3: Implémenter la fonction de coût (MSE)
def cost_function(params, N, S0, I0, R0, D0, t, S_obs, I_obs, R_obs, D_obs):
    beta, gamma, mu = params
    S, I, R, D = solve_sird(N, beta, gamma, mu, S0, I0, R0, D0, t)
    mse_S = np.mean((S - S_obs) ** 2)
    mse_I = np.mean((I - I_obs) ** 2)
    mse_R = np.mean((R - R_obs) ** 2)
    mse_D = np.mean((D - D_obs) ** 2)
    return mse_S + mse_I + mse_R + mse_D  # Somme des erreurs quadratiques

# Étape 4: Optimisation par Grid Search
# Définir les plages pour beta, gamma, mu
ranges = ((0.25, 0.5), (0.08, 0.15), (0.005, 0.015))

# Conditions initiales
S0 = S_obs[0]  # Susceptibles initiaux
I0 = I_obs[0]  # Infectés initiaux
R0 = R_obs[0]  # Rétablis initiaux
D0 = D_obs[0]  # Décès initiaux
N = S0 + I0 + R0 + D0  # Population totale

# Grid Search pour trouver les meilleurs paramètres
result = brute(cost_function, ranges, args=(N, S0, I0, R0, D0, jours, S_obs, I_obs, R_obs, D_obs), finish=None)
beta_opt, gamma_opt, mu_opt = result

# Calcul du coût minimal avec les paramètres optimaux
min_cost = cost_function(result, N, S0, I0, R0, D0, jours, S_obs, I_obs, R_obs, D_obs)

print(f"Paramètres optimaux: beta={beta_opt}, gamma={gamma_opt}, mu={mu_opt}")
print(f"Coût minimal : {min_cost}")

# Étape 5: Visualisation des résultats
# Résolution du modèle avec les paramètres optimaux
S_opt, I_opt, R_opt, D_opt = solve_sird(N, beta_opt, gamma_opt, mu_opt, S0, I0, R0, D0, jours)

# Tracer les résultats
plt.figure(figsize=(12, 8))
plt.plot(jours, S_obs, 'b', label='Susceptibles observés')
plt.plot(jours, I_obs, 'r', label='Infectés observés')
plt.plot(jours, R_obs, 'g', label='Rétablis observés')
plt.plot(jours, D_obs, 'k', label='Décès observés')
plt.plot(jours, S_opt, 'b--', label='Susceptibles modèle')
plt.plot(jours, I_opt, 'r--', label='Infectés modèle')
plt.plot(jours, R_opt, 'g--', label='Rétablis modèle')
plt.plot(jours, D_opt, 'k--', label='Décès modèle')
plt.xlabel('Jours')
plt.ylabel('Population')
plt.title('Comparaison des données observées et du modèle SIRD optimisé')
plt.legend()
plt.grid()
plt.show()
