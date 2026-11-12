import numpy as np
import pandas as pd

# Paramètres du signal initial
f_signal = 1000  # Fréquence en Hz
amplitude = 2    # Tension en Volts
duree = 0.005    # Durée de l'affichage (5 ms)

# Paramètres du CAN
bits = 8
pleine_echelle = 5.0 # 5V au total
niveaux = 2**bits
quantum = pleine_echelle / (niveaux - 1)

def conversion_can(signal):
    # 1. Saturation (écrêtage) si le signal dépasse la pleine échelle
    signal_limite = np.clip(signal, -pleine_echelle/2, pleine_echelle/2)
    # 2. Quantification (arrondi au multiple du quantum le plus proche)
    signal_quantifie = np.round(signal_limite / quantum) * quantum
    
    # 3. Conversion en code binaire (entier de 0 à 255)
    # On décale le signal pour que -2.5V corresponde à 0 et +2.5V à 255
    code_entier = np.round((signal_limite + pleine_echelle/2) / quantum).astype(int)
    
    # S'assurer que les valeurs restent dans les limites 8 bits (0-255)
    code_entier = np.clip(code_entier, 0, 255)
    
    # Convertir en chaîne binaire sur 8 bits
    code_binaire = [format(val, '08b') for val in code_entier]
    
    return signal_quantifie, code_entier, code_binaire

# Échantillonnage à 3 kHz (respecte Shannon) pour l'exemple
f_ech = 3000
t_ech = np.arange(0, duree, 1 / f_ech)
signal_echantillonne = amplitude * np.sin(2 * np.pi * f_signal * t_ech)

# Conversion CAN
signal_can, code_decimal, code_binaire = conversion_can(signal_echantillonne)

# Création du DataFrame Pandas
df = pd.DataFrame({
    'Temps (s)': t_ech,
    'Tension Anal. (V)': signal_echantillonne,
    'Tension Quant. (V)': signal_can,
    'Code Décimal': code_decimal,
    'Code Binaire (8 bits)': code_binaire
})

# Formatage des nombres flottants pour une meilleure lisibilité
df['Temps (s)'] = df['Temps (s)'].map('{:.5f}'.format)
df['Tension Anal. (V)'] = df['Tension Anal. (V)'].map('{:.4f}'.format)
df['Tension Quant. (V)'] = df['Tension Quant. (V)'].map('{:.4f}'.format)

# Affichage du tableau dans la console
print(df.to_string(index=False))