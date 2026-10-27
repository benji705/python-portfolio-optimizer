# 📈 Python Portfolio Optimizer

Outil d'optimisation de portefeuille basé sur la théorie de Markowitz et simulations Monte Carlo.

## 🚀 Fonctionnalités
* Récupération automatique des données via `yfinance`.
* Optimisation du Ratio de Sharpe avec `Riskfolio-Lib`.
* Simulations de trajectoires futures (Monte Carlo).

## 📊 Interprétation des Résultats

### 1. Frontière Efficiente
<img width="1000" alt="frontiere" src="https://github.com/user-attachments/assets/1157b47e-ee1d-45de-9e3a-6f012046f901" />

**Analyse :**
* **Le compromis Risque/Rendement :** Le portefeuille optimal se situe dans la partie supérieure de la courbe. Cela indique une stratégie offensive (volatilité de ~38% pour un rendement annuel moyen de ~80%).
* **L'efficacité :** L'étoile rouge maximise le *Risk Adjusted Return Ratio* (~2.1).

### 2. Répartition du Portefeuille
<img width="1000" alt="camember" src="https://github.com/user-attachments/assets/800d20cd-f4ec-466d-9941-77eef1751694" />
Voici la répartition optimale des actifs calculée pour maximiser le rendement ajusté au risque.

### 3. Simulation Monte Carlo
<img width="1000" alt="monte_carlo" src="https://github.com/user-attachments/assets/06d682d9-9ce4-47a5-b963-979cf4b944ed" />

**Analyse :**
* **La Tendance :** Au bout de 252 jours, un capital de 1000€ est projeté vers une moyenne de 2200€.
* **La Sécurité :** La grande majorité des scénarios finit au-dessus du capital initial, indiquant une probabilité de perte totale faible sur la période étudiée.



## ⚙️ Installation et utilisation

```bash
git clone https://github.com/benji705/python-portfolio-optimizer.git
cd python-portfolio-optimizer
pip install -r requirements.txt
python main.py
```

Les graphiques sont enregistrés dans le dossier courant (`frontiere_efficiente.png`, `repartition.png`, `monte_carlo.png`).
