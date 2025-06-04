import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import os


caminho_csv = "../resultados/resultados.csv"
df = pd.read_csv(caminho_csv)

# 1. Estatísticas descritivas
media_espera = df['tempo_espera'].mean()
mediana_espera = df['tempo_espera'].median()
moda_espera = df['tempo_espera'].mode()[0]
variancia_espera = df['tempo_espera'].var()
desvio_espera = df['tempo_espera'].std()

media_atend = (df['fim_atendimento'] - df['inicio_atendimento']).mean()
mediana_atend = (df['fim_atendimento'] - df['inicio_atendimento']).median()
moda_atend = (df['fim_atendimento'] - df['inicio_atendimento']).mode()[0]
variancia_atend = (df['fim_atendimento'] - df['inicio_atendimento']).var()
desvio_atend = (df['fim_atendimento'] - df['inicio_atendimento']).std()

# 2. Visualizações
plt.figure(figsize=(12, 8))

# Histograma do tempo de atendimento
plt.subplot(2, 2, 1)
sns.histplot(df['fim_atendimento'] - df['inicio_atendimento'], bins=20, kde=True, color='skyblue')
plt.title("Histograma - Tempo de Atendimento")
plt.xlabel("Tempo (min)")
plt.ylabel("Frequência")

# Histograma do tempo de espera
plt.subplot(2, 2, 2)
sns.histplot(df['tempo_espera'], bins=20, kde=True, color='salmon')
plt.title("Histograma - Tempo de Espera")
plt.xlabel("Tempo (min)")
plt.ylabel("Frequência")

# Boxplot comparativo
plt.subplot(2, 1, 2)
dados_plot = pd.DataFrame({
    "Tempo de Atendimento": df['fim_atendimento'] - df['inicio_atendimento'],
    "Tempo de Espera": df['tempo_espera']
})
sns.boxplot(data=dados_plot)
plt.title("Boxplot - Comparação Atendimento vs Espera")
plt.ylabel("Tempo (min)")

plt.tight_layout()
plt.savefig("graficos_estatisticos.png")  # salvar os gráficos para o PDF depois
plt.show()

# 3. Intervalos de confiança (95%)
ic_espera = stats.t.interval(
    confidence=0.95,
    df=len(df['tempo_espera'])-1,
    loc=media_espera,
    scale=stats.sem(df['tempo_espera'])
)

ic_atend = stats.t.interval(
    confidence=0.95,
    df=len(df['tempo_espera'])-1,
    loc=media_atend,
    scale=stats.sem(df['fim_atendimento'] - df['inicio_atendimento'])
)

# Impressão dos resultados
print("\n--- Estatísticas Tempo de Espera ---")
print(f"Média: {media_espera:.2f}")
print(f"Mediana: {mediana_espera:.2f}")
print(f"Moda: {moda_espera:.2f}")
print(f"Variância: {variancia_espera:.2f}")
print(f"Desvio padrão: {desvio_espera:.2f}")
print(f"Intervalo de confiança 95%: ({ic_espera[0]:.2f}, {ic_espera[1]:.2f})")

print("\n--- Estatísticas Tempo de Atendimento ---")
print(f"Média: {media_atend:.2f}")
print(f"Mediana: {mediana_atend:.2f}")
print(f"Moda: {moda_atend:.2f}")
print(f"Variância: {variancia_atend:.2f}")
print(f"Desvio padrão: {desvio_atend:.2f}")
print(f"Intervalo de confiança 95%: ({ic_atend[0]:.2f}, {ic_atend[1]:.2f})")
