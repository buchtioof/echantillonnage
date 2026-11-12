import numpy as np
import matplotlib.pyplot as plt

# Paramètres du signal initial
f_signal = 1000  # Fréquence en Hz
amplitude = 2    # Tension en Volts
duree = 0.005    # Durée de l'affichage (5 ms)

# Paramètres du CAN
bits = 8
pleine_echelle = 5.0
niveaux = 2**bits
quantum = pleine_echelle / (niveaux - 1)

# Fonction simulant la conversion analogique-numérique
def conversion_can(signal):
    # 1. Saturation (écrêtage) si le signal dépasse la pleine échelle
    signal_limite = np.clip(signal, -pleine_echelle/2, pleine_echelle/2)
    # 2. Quantification (arrondi au multiple du quantum le plus proche)
    signal_numerique = np.round(signal_limite / quantum) * quantum
    return signal_numerique

# Signal analogique théorique
t_continu = np.linspace(0, duree, 1000)
signal_continu = amplitude * np.sin(2 * np.pi * f_signal * t_continu)

# Affichage des échantillonnages aux différentes fréquences
f_ech_list = [2000, 3000, 5000]
couleurs = ['r', 'g', 'g']
titres = [
    'Signal à 2 kHz + CAN 8 bits (Ne respecte pas Shannon)',
    'Signal à 3 kHz + CAN 8 bits (Respecte Shannon)',
    'Signal à 5 kHz + CAN 8 bits (Respecte Shannon)'
]

fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

for i, f_ech in enumerate(f_ech_list):
    # Échantillonnage
    t_ech = np.arange(0, duree, 1 / f_ech)
    signal_echantillonne = amplitude * np.sin(2 * np.pi * f_signal * t_ech)
    
    # Passage dans le CAN
    signal_can = conversion_can(signal_echantillonne)
    
    # Affichage
    axes[i].plot(t_continu, signal_continu, color='gray', linestyle='--', label='Signal analogique')
    
    # Affichage des échantillons quantifiés
    axes[i].stem(t_ech, signal_can, linefmt=f'{couleurs[i]}-', markerfmt=f'{couleurs[i]}o', basefmt='k-', label='Sortie CAN')
    
    # Affichage en escalier (bloqueur d'ordre 0) pour bien visualiser l'effet numérique
    axes[i].step(t_ech, signal_can, where='post', color=couleurs[i], alpha=0.3, label='Maintien numérique')
    
    axes[i].set_title(titres[i])
    axes[i].set_ylabel('Tension (V)')
    axes[i].grid(True)
    axes[i].legend(loc='upper right')

axes[-1].set_xlabel('Temps (s)')
plt.tight_layout()
plt.show()