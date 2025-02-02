import numpy as np
import matplotlib.pyplot as plt

def modele_sird(beta, gamma, mu, S0, I0, R0, D0, h, t_max):
    """
    Implémentation du modèle SIRD avec la méthode d'Euler.

    Paramètres :
    - beta, gamma, mu : paramètres du modèle
    - S0, I0, R0, D0 : conditions initiales
    - h : pas de temps
    - t_max : durée de la simulation (en jours)

    Retourne :
    - time : tableau des temps
    - S, I, R, D : tableaux des valeurs de S, I, R, D au cours du temps
    """
    # Nombre total de pas
    num_steps = int(t_max / h)
    
    # Initialisation des tableaux
    time = np.arange(0, t_max, h)
    S = np.zeros(num_steps)
    I = np.zeros(num_steps)
    R = np.zeros(num_steps)
    D = np.zeros(num_steps)
    
    # Conditions initiales
    S[0], I[0], R[0], D[0] = S0, I0, R0, D0
    
    # Méthode d'Euler
    for t in range(1, num_steps):
        dS = -beta * S[t-1] * I[t-1]
        dI = beta * S[t-1] * I[t-1] - gamma * I[t-1] - mu * I[t-1]
        dR = gamma * I[t-1]
        dD = mu * I[t-1]
        
        S[t] = S[t-1] + h * dS
        I[t] = I[t-1] + h * dI
        R[t] = R[t-1] + h * dR
        D[t] = D[t-1] + h * dD
    
    return time, S, I, R, D

# Paramètres du modèle
beta = 0.5      # Taux de transmission
gamma = 0.15    # Taux de guérison
mu = 0.015      # Taux de mortalité

# Conditions initiales
S0 = 0.99       # 99% de susceptibles
I0 = 0.01       # 1% d'infectés
R0 = 0.0        # 0% de rétablis
D0 = 0.0        # 0% de décès

# Paramètres de simulation
h = 0.01        # Pas de temps (0.01 jour)
t_max = 100     # Durée de la simulation (100 jours)

# Simulation
time, S, I, R, D = modele_sird(beta, gamma, mu, S0, I0, R0, D0, h, t_max)

# Visualisation des résultats
plt.figure(figsize=(10, 6))
plt.plot(time, S, label='Susceptibles (S)')
plt.plot(time, I, label='Infectés (I)')
plt.plot(time, R, label='Rétablis (R)')
plt.plot(time, D, label='Décès (D)')
plt.xlabel('Temps (jours)')
plt.ylabel('Proportion de la population')
plt.title('Modèle SIRD - Simulation avec méthode d\'Euler')
plt.legend()
plt.grid()
plt.show()