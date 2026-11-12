import numpy as np
import matplotlib.pyplot as plt

# Paramètres globaux
f_signal = 1000  # Fréquence du signal en Hz
amplitude = 2    # Tension crête en Volts
duree = 0.002    # Durée de la simulation réduite à 2 ms
f_ech = 5000     # Fréquence d'échantillonnage à 5 kHz

# Paramètres du CAN / CNA
bits = 8
pleine_echelle = 5.0 # Plage de -2.5V à +2.5V
niveaux = 2**bits
quantum = pleine_echelle / (niveaux - 1)

# 1. Signal continu d'origine
t_continu = np.linspace(0, duree, 1000)
signal_continu = amplitude * np.sin(2 * np.pi * f_signal * t_continu)

# 2. Échantillonnage
t_ech = np.arange(0, duree, 1 / f_ech)
signal_ech = amplitude * np.sin(2 * np.pi * f_signal * t_ech)

# 3. Traitement CAN : Obtention du code numérique
signal_limite = np.clip(signal_ech, -pleine_echelle/2, pleine_echelle/2)
code_numerique = np.round((signal_limite + pleine_echelle/2) / quantum).astype(int)
code_numerique = np.clip(code_numerique, 0, 255)

# 4. Traitement CNA : Reconstruction analogique
tension_cna = (code_numerique * quantum) - (pleine_echelle / 2)

# Configuration de l'affichage
fig, ax = plt.subplots(figsize=(10, 6))

# Tracé du signal d'origine
ax.plot(t_continu, signal_continu, color='gray', linestyle='--', label='Signal continu d\'origine')

# Tracé de la sortie du CNA
ax.step(t_ech, tension_cna, where='post', color='blue', linewidth=2, label='Sortie analogique du CNA')

# Mise en évidence des instants de mise à jour
ax.plot(t_ech, tension_cna, 'ro', label='Impulsions de conversion')

ax.set_title("Reconstruction du signal par le CNA (0 à 0.002 s)")
ax.set_xlabel("Temps (s)")
ax.set_ylabel("Tension (V)")
ax.set_ylim(-3, 3)
ax.set_xlim(0, 0.002)
ax.grid(True)
ax.legend(loc='upper right')

plt.tight_layout()
plt.show()