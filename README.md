# 🧪 Simulador de Filas M/M/c

## 🎯 Objetivo
Este projeto simula o atendimento de uma fila com múltiplos servidores (modelo M/M/c), utilizando dados reais para análise de desempenho e geração de métricas como tempo médio de espera, taxa de ocupação e tamanho da fila.

## 📂 Estrutura do Projeto

```text
projeto_fila/
├── simulacoes/       # Código Python da simulação
│   └── simulacao.py
├── dados/            # Dados de entrada em CSV
│   └── tempos.csv
├── resultados/       # Resultados gerados e gráficos
│   └── resultados.csv, gráficos .png
```

## 🚀 Como Executar

1. Instale as dependências:
   ```bash
   pip install pandas matplotlib

2. Execute a simulação:

   python simulacoes/simulacao.py

## 📊 Saídas Geradas
resultados.csv: registro de cada cliente (chegada, atendimento, espera)

Gráficos:

Tempo de espera por cliente

Tamanho da fila ao longo do tempo

Ocupação dos servidores

## 📈 Métricas Calculadas
P₀: Probabilidade do sistema estar vazio

P_espera: Probabilidade de um cliente esperar

Lq: Número médio de clientes na fila

Wq: Tempo médio de espera na fila

W: Tempo médio no sistema

L: Número médio de clientes no sistema

## 👨‍💻 Autores
Lucas Stoffel
Estela Argolo
Willian Endo
Rodrigo Madureira

# 📚 Referências
Teoria das Filas M/M/c (Pesquisa Operacional)

Bibliotecas: pandas, matplotlib
