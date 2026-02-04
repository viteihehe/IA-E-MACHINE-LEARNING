import pandas as pd
import numpy as np

np.random.seed(42)
n_amostras = 1000

data = {
    'Area': np.random.uniform(10, 100, n_amostras),          # 10 a 100 m2
    'Quartos': np.random.randint(1, 5, n_amostras),         # 1 a 4 quartos
    'Idade': np.random.randint(1, 30, n_amostras),          # 1 a 30 anos
    'Distancia_Centro': np.random.uniform(1, 20, n_amostras) # 1 a 20 km
}

df = pd.DataFrame(data)

# Fórmula simplificada para um Target pequeno:
# Cada 10m2 valem 5 pontos, cada quarto vale 2, idade tira 0.1, distância tira 0.5
df['Target'] = (
    (df['Area'] * 0.5) + 
    (df['Quartos'] * 2.0) - 
    (df['Idade'] * 0.1) - 
    (df['Distancia_Centro'] * 0.5) + 
    10 # Valor base
)

# Garante que não existam valores negativos e arredonda
df['Target'] = df['Target'].clip(lower=1).round(2)
df = df.round(2)

df.to_csv('dados.csv', index=False)
print("Sucesso! 'dados.csv' criado com 101 linhas e Target reduzido.")