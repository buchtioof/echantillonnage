import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Paramètres du signal initial
f_signal = 1000  # Fréquence en Hz
amplitude = 2    # Tension en Volts
duree = 0.005    # Durée de l'affichage (5 ms)

# Paramètres du CAN
bits = 8
pleine_echelle = 5.0 # 5V au total (de -2.5V à +2.5V)
niveaux = 2**bits
quantum = pleine_echelle / (niveaux - 1)

# Échantillonnage à 3 kHz pour l'exemple
f_ech = 3000
t_ech = np.arange(0, duree, 1 / f_ech)
signal_echantillonne = amplitude * np.sin(2 * np.pi * f_signal * t_ech)

# 1. Saturation
signal_limite = np.clip(signal_echantillonne, -pleine_echelle/2, pleine_echelle/2)
# 2. Quantification
signal_quantifie = np.round(signal_limite / quantum) * quantum

# 3. Conversion en code binaire (entier de 0 à 255)
code_entier = np.round((signal_limite + pleine_echelle/2) / quantum).astype(int)
code_entier = np.clip(code_entier, 0, 255)
code_binaire = [format(val, '08b') for val in code_entier]

# Création du DataFrame pour faciliter le formatage du tableau
df = pd.DataFrame({
    'Temps (s)': [f"{t:.5f}" for t in t_ech],
    'Tension Anal. (V)': [f"{v:.4f}" for v in signal_echantillonne],
    'Tension Quant. (V)': [f"{v:.4f}" for v in signal_quantifie],
    'Code Décimal': code_entier,
    'Code Binaire': code_binaire
})

# Configuration de la figure Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))

# Masquer les axes pour ne laisser que le tableau
ax.axis('tight')
ax.axis('off')

# Création du tableau
table = ax.table(
    cellText=df.values, 
    colLabels=df.columns, 
    loc='center', 
    cellLoc='center'
)

# Ajustement du style du tableau
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.5) # Ajuste la largeur et la hauteur des cellules

# Ajout d'un titre
plt.title("Valeurs de conversion analogique-numérique (CAN 8 bits, 5V pleine échelle)", fontsize=14, pad=20)

plt.tight_layout()
plt.show()