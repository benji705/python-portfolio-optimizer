# python-portfolio-optimizer


import riskfolio as rp
import yfinance as yf
import pandas as pd
import warnings

# On ignore les messages d'avertissement inutiles pour y voir plus clair
warnings.filterwarnings("ignore")

print("1. Téléchargement des données en cours...")
# J'ajoute quelques actions en plus pour être sûr d'avoir des données valides
assets = ['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN',"NKE","NVDA","SBUX","BA"] 

# auto_adjust=True corrige souvent les problèmes de données
data = yf.download(assets, start='2022-11-01',end='2025-11-01', auto_adjust=True)

# GESTION DES ERREURS DE TÉLÉCHARGEMENT
# Parfois yfinance renvoie un format complexe, on s'assure de n'avoir que les prix de clôture
if isinstance(data.columns, pd.MultiIndex):
    # Si on a 'Close' ou 'Adj Close', on essaye de le récupérer
    try:
        data = data['Close']
    except KeyError:
        # Fallback si la structure est différente
        pass

print("2. Nettoyage des données...")
# C'est ICI qu'on répare l'erreur : on supprime les colonnes (actions) qui ont échoué
data = data.dropna(axis=1, how='all') 
# Puis on supprime les jours où il manque des données
data = data.dropna()

if data.empty:
    print("ERREUR CRITIQUE : Aucune donnée n'a pu être téléchargée.")
    print("Essayez de relancer le script dans quelques minutes.")
    exit()

print(f"   -> Données prêtes pour {len(data.columns)} actions : {list(data.columns)}")

# 3. Calcul des rendements
Y = data.pct_change().dropna()

# 4. Création du Portefeuille Riskfolio
print("3. Optimisation du portefeuille...")
port = rp.Portfolio(returns=Y)

# Calcul des statistiques (Moyenne / Covariance)
port.assets_stats(method_mu='hist', method_cov='hist')

# 5. Optimisation (Ratio de Sharpe)
model = 'Classic'
rm = 'MV'  # Variance
obj = 'Sharpe' 
hist = True 
rf = 0 
l = 0 

try:
    w = port.optimization(model=model, rm=rm, obj=obj, rf=rf, l=l, hist=hist)
    
    print("\nRESULTAT FINAL - Répartition optimale :")
    print("-" * 30)
    # On affiche en pourcentage pour que ce soit plus lisible
    print(round(w.T * 100, 2))
    print("-" * 30)
    print("L'optimiseur fonctionne.")

except Exception as e:
    print("\nErreur durant l'optimisation :")
    print(e)

import matplotlib.pyplot as plt

# ---------------------------------------------------------
# NOUVELLE PARTIE : Visualisation de la Frontière Efficiente
# ---------------------------------------------------------

print("\nGénération du graphique en cours...")

# 1. On calcule 50 points pour tracer la courbe
points = 50
frontier = port.efficient_frontier(model=model, rm=rm, points=points, rf=rf, hist=hist)

# 2. On trace le graphique
# label='Max Risk Adjusted Return Ratio' montre votre portefeuille optimal (l'étoile)
# Version sécurisée si mu/cov ne sont pas accessibles directement
mu = port.mu
cov = port.cov

ax = rp.plot_frontier(w_frontier=frontier, mu=mu, cov=cov, returns=Y, rm=rm,
                      rf=rf, alpha=0.05, cmap='viridis', w=w, 
                      label='Portefeuille Optimal', 
                      marker='*', s=16, c='r', height=6, width=10, ax=None)
plt.show()
print("Graphique généré ! Regardez la nouvelle fenêtre.")
plt.show()

import matplotlib.pyplot as plt

# ... (votre code précédent reste ici)

print("\nGénération du graphique de répartition (Camembert)...")

# On trace le camembert de l'allocation
# w = les poids calculés
# title = le titre du graphique
# cmap = le jeu de couleurs (tab20 est joli)
ax = rp.plot_pie(w=w, title='Mon Allocation Optimale', cmap="tab20", height=6, width=10, ax=None)

plt.show()


import numpy as np

# ---------------------------------------------------------
# ETAPE 6 : SIMULATION MONTE CARLO (Dr. Strange)
# ---------------------------------------------------------
print("\nLancement de la simulation Monte Carlo...")

# 1. Préparation des données du portefeuille
# On calcule les rendements journaliers historiques de VOTRE portefeuille optimisé
# (On multiplie les rendements de chaque action par son poids dans le portefeuille)
port_returns = (Y * w.T.values).sum(axis=1)

# On récupère les stats de ce portefeuille (Moyenne et Écart-type journaliers)
mu_p = port_returns.mean()
sigma_p = port_returns.std()

# 2. Paramètres de la simulation
n_simulations = 1000   # Nombre de scénarios (1000 futurs différents)
n_days = 252           # Nombre de jours à simuler (1 an)
start_price = 1000     # On imagine qu'on investit 1000 € aujourd'hui

# 3. La magie Mathématique (Génération des chemins)
# On génère des rendements aléatoires selon une loi Normale
random_returns = np.random.normal(mu_p, sigma_p, (n_days, n_simulations))

# On construit les prix jour après jour (Prix cumulés)
# On commence à 1000€ partout
price_paths = np.zeros((n_days, n_simulations))
price_paths[0] = start_price

for t in range(1, n_days):
    # Prix jour J = Prix veille * (1 + rendement aléatoire)
    price_paths[t] = price_paths[t-1] * (1 + random_returns[t])

# 4. Visualisation
plt.figure(figsize=(10,6))
plt.plot(price_paths, color='lightblue', alpha=0.1) # Les 1000 scénarios en transparent
plt.plot(price_paths.mean(axis=1), color='red', linewidth=2, label='Moyenne espérée') # La moyenne
plt.title(f'Simulation Monte Carlo : 1000 futurs possibles pour vos {start_price}€')
plt.xlabel('Jours futurs')
plt.ylabel('Valeur du portefeuille (€)')
plt.legend()
plt.show()

# 5. Analyse du Risque (Value at Risk)
final_prices = price_paths[-1] # Les prix au dernier jour
worst_case = np.percentile(final_prices, 5) # Le scénario "catastrophe" (les 5% les pires)

print("-" * 30)
print(f"ANALYSE DE RISQUE (Sur 1 an) :")
print(f"Investissement initial : {start_price} €")
print(f"Moyenne espérée : {round(final_prices.mean(), 2)} €")
print(f"Dans le pire des cas (95% sûreté) : vous aurez au moins {round(worst_case, 2)} €")
print("-" * 30)




----------------------------------------------------INTERPRETATION-----------------------------------------------------------------------
