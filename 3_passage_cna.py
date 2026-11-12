import numpy as np
import matplotlib.pyplot as plt

# Paramètres globaux
f_signal = 1000  # Fréquence du signal (1 kHz)
amplitude = 2    # Tension
duree = 0.002    # Durée (2 ms)
f_ech = 5000     # Fréquence d'échantillonnage (5 kHz) -> fe

# Paramètres du CAN
bits = 8
pleine_echelle = 5.0
quantum = pleine_echelle / ((2**bits) - 1)

# 1. Signal continu et échantillonnage
t_continu = np.linspace(0, duree, 1000)
signal_continu = amplitude * np.sin(2 * np.pi * f_signal * t_continu)

t_ech = np.arange(0, duree, 1 / f_ech)
signal_ech = amplitude * np.sin(2 * np.pi * f_signal * t_ech)

# 2. CAN (Quantification)
signal_limite = np.clip(signal_ech, -pleine_echelle/2, pleine_echelle/2)
code_numerique = np.round((signal_limite + pleine_echelle/2) / quantum).astype(int)
code_numerique = np.clip(code_numerique, 0, 255)

# 3. CNA (Sortie brute en escalier)
tension_cna = (code_numerique * quantum) - (pleine_echelle / 2)

# =====================================================================
# 4. LE FILTRE PASSE-BAS (Le "drap" lisseur avec fc = fe / 2)
# On applique la formule de Shannon pour lisser les points
# =====================================================================
signal_lisse = np.zeros(len(t_continu))
for i, t_point in enumerate(t_ech):
    # La fonction np.sinc agit mathématiquement comme le filtre physique
    signal_lisse += tension_cna[i] * np.sinc(f_ech * (t_continu - t_point))


# Configuration de l'affichage
fig, ax = plt.subplots(figsize=(10, 6))

# Tracé 1 : L'escalier brut (ce qu'on avait avant)
ax.step(t_ech, tension_cna, where='post', color='blue', alpha=0.3, label='Sortie brute du CNA (Escalier)')
ax.plot(t_ech, tension_cna, 'ro', label='Points numériques')

# Tracé 2 : Le signal filtré (après le "drap")
ax.plot(t_continu, signal_lisse, color='green', linewidth=2.5, label='Signal final lissé (Filtre fc = fe/2)')

ax.set_title("Lissage du signal : de l'escalier à la courbe fluide")
ax.set_xlabel("Temps (s)")
ax.set_ylabel("Tension (V)")
ax.set_ylim(-3, 3)
ax.set_xlim(0, 0.002)
ax.grid(True)
ax.legend(loc='upper right')

plt.tight_layout()
plt.show()