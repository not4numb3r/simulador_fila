import pandas as pd
import matplotlib.pyplot as plt
import random
import csv
import os

# Parâmetros
NUM_SERVIDORES = 2  # c
TEMPO_SIMULACAO = 1000  # minutos, simulação contínua
CAMINHO_DADOS = "dados/tempos.csv"
CAMINHO_RESULTADOS = "resultados/resultados.csv"

# Ler dados reais
dados = pd.read_csv(CAMINHO_DADOS)
tempos_chegada = dados['tempo_entre_chegadas'].tolist()
tempos_atendimento = dados['tempo_atendimento'].tolist()

# Se os dados forem menores que a simulação, repetir aleatoriamente
while len(tempos_chegada) < TEMPO_SIMULACAO:
    tempos_chegada.extend(random.sample(tempos_chegada, len(tempos_chegada)))
    tempos_atendimento.extend(random.sample(tempos_atendimento, len(tempos_atendimento)))

# Simulação
tempo_atual = 0
fila = []
servidores = [0] * NUM_SERVIDORES
historico_espera = []
historico_fila = []
ocupacao_servidores = [[] for _ in range(NUM_SERVIDORES)]
chegada = 0
indice_cliente = 0

# Assegura que a pasta de resultados existe
os.makedirs(os.path.dirname(CAMINHO_RESULTADOS), exist_ok=True)

with open(CAMINHO_RESULTADOS, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['cliente', 'tempo_chegada', 'inicio_atendimento', 'fim_atendimento', 'tempo_espera'])

    while tempo_atual < TEMPO_SIMULACAO and indice_cliente < len(tempos_chegada):
        chegada += tempos_chegada[indice_cliente]
        atendimento = tempos_atendimento[indice_cliente]
        indice_cliente += 1

        tempo_atual = chegada

        # Liberar servidores que terminaram
        for i in range(NUM_SERVIDORES):
            if servidores[i] < tempo_atual:
                servidores[i] = tempo_atual

        # Procurar servidor livre
        servidor_disponivel = next((i for i in range(NUM_SERVIDORES) if servidores[i] <= tempo_atual), None)

        if servidor_disponivel is not None:
            inicio = tempo_atual
            fim = inicio + atendimento
            tempo_espera = 0
            servidores[servidor_disponivel] = fim
            ocupacao_servidores[servidor_disponivel].append((inicio, fim))
        else:
            # Entrar na fila
            espera = min(servidores)
            servidor_disponivel = servidores.index(espera)
            tempo_espera = espera - tempo_atual
            inicio = espera
            fim = inicio + atendimento
            servidores[servidor_disponivel] = fim
            ocupacao_servidores[servidor_disponivel].append((inicio, fim))

        fila.append((tempo_atual, len([s for s in servidores if s > tempo_atual])))
        historico_espera.append(tempo_espera)
        writer.writerow([indice_cliente, tempo_atual, inicio, fim, tempo_espera])
        historico_fila.append(len([s for s in servidores if s > tempo_atual]))

# Métricas
Lq = sum(historico_fila) / len(historico_fila)
Wq = sum(historico_espera) / len(historico_espera)
W = Wq + (sum(tempos_atendimento[:indice_cliente]) / indice_cliente)
L = W * (indice_cliente / chegada)
P0 = 1.0 if all(s == 0 for s in servidores) else 0.0
P_espera = sum(1 for e in historico_espera if e > 0) / len(historico_espera)

print(f"\n--- MÉTRICAS ---")
print(f"P₀ (prob sistema vazio): {P0:.4f}")
print(f"P_espera (probabilidade de esperar): {P_espera:.4f}")
print(f"Lq (nº médio na fila): {Lq:.2f}")
print(f"Wq (tempo médio de espera): {Wq:.2f} min")
print(f"W (tempo médio no sistema): {W:.2f} min")
print(f"L (nº médio no sistema): {L:.2f}")

# Visualizações
plt.figure(figsize=(12, 6))

# Tempo de espera
plt.subplot(1, 3, 1)
plt.plot(historico_espera, color='tab:blue')
plt.title("Tempo de Espera por Cliente")
plt.xlabel("Cliente")
plt.ylabel("Tempo de Espera (min)")

# Tamanho da fila
plt.subplot(1, 3, 2)
plt.step([t[0] for t in fila], [t[1] for t in fila], where='post', color='tab:orange')
plt.title("Evolução do Tamanho da Fila ao Longo do Tempo")
plt.xlabel("Tempo (min)")
plt.ylabel("Clientes na fila")




# Ocupação dos servidores (melhorado)
plt.subplot(1, 3, 3)
for i, ocupacoes in enumerate(ocupacao_servidores):
    for o in ocupacoes:
        # plota uma linha horizontal mais grossa para cada período de atendimento do servidor i
        plt.hlines(y=i+1, xmin=o[0], xmax=o[1], linewidth=6, color='tab:purple')
plt.title("Tempo de Ocupação dos Servidores")
plt.xlabel("Tempo (min)")
plt.ylabel("Servidor")
plt.yticks(range(1, NUM_SERVIDORES + 1))
plt.ylim(0.5, NUM_SERVIDORES + 0.5)
plt.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
