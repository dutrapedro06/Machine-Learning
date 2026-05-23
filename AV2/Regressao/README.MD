# California Housing — Regressão de Preços de Imóveis

**Aluno:** Pedro Pereira Dutra — RA: 24101026

**Disciplina:** Aprendizado de Máquina — Notebook 2 (Regressão)

---

## 📋 Descrição do Projeto

Este projeto tem como objetivo prever o **valor mediano de imóveis** em blocos residenciais da Califórnia com base em características socioeconômicas e geográficas.

O problema é tratado como uma **regressão supervisionada**, onde a variável-alvo é contínua:

- **`MedHouseVal`** — valor mediano dos imóveis no bloco, expresso em USD × 100k (ex: 2.5 = USD 250.000)

---

## 📊 Dataset

**Nome:** California Housing Dataset  
**Fonte:** `sklearn.datasets.fetch_california_housing`  
**Tamanho:** 20.640 registros (censo da Califórnia de 1990)

Cada registro representa um bloco residencial, com 8 features numéricas e sem valores ausentes.

### Features

| Feature | Descrição |
|--------|-----------|
| `MedInc` | Renda mediana do bloco |
| `HouseAge` | Idade mediana das casas |
| `AveRooms` | Média de cômodos por domicílio |
| `AveBedrms` | Média de quartos por domicílio |
| `Population` | População total do bloco |
| `AveOccup` | Média de moradores por domicílio |
| `Latitude` | Latitude geográfica do bloco |
| `Longitude` | Longitude geográfica do bloco |

---

## 🔍 Análise Exploratória (EDA)

Foram realizadas visualizações para entender a relação entre as variáveis e o preço dos imóveis. As principais descobertas:

- **Renda mediana** (`MedInc`): correlação de **+0.688** com o alvo — o preditor mais forte do dataset
- **Localização geográfica**: faixa costeira (SF, LA, San Diego) concentra os imóveis mais valiosos, padrão visível no mapa de calor geográfico
- **Truncamento em 5.0**: 1.071 registros (5.2%) têm `MedHouseVal = 5.0` (USD 500k) — teto artificial do censo que prejudica a predição de imóveis de alto padrão
- **`AveOccup`**: correlação linear quase nula (-0.024) com o alvo, mas alta importância em modelos não-lineares
- **Outliers extremos**: `AveOccup` (máx. 1.243 moradores) e `AveRooms` (máx. 141 cômodos) — mantidos pela robustez do XGBoost

---

## ⚙️ Pré-processamento

1. **Carregamento direto** via `sklearn` — sem necessidade de download externo
2. **Divisão dos dados:** 80% treino / 20% teste
3. **Padronização** com `StandardScaler` aplicado ao conjunto de treino (fit) e teste (transform)

---

## 🤖 Modelos Testados

Foram comparados 7 algoritmos no conjunto de teste:

| Grupo | Modelo | MAE | RMSE | R² |
|-------|--------|-----|------|----|
| Linear | Regressão Linear | 0.5332 | 0.7456 | 0.5758 |
| Linear | Ridge | — | — | ~0.58 |
| Linear | Lasso | — | — | ~0.57 |
| Bagging | Extra Trees | — | — | ~0.79 |
| Bagging | **Random Forest** | 0.3275 | 0.5053 | 0.8051 |
| Boosting | Gradient Boosting | — | — | ~0.80 |
| Boosting | **XGBoost** | **0.3096** | **0.4718** | **0.8301** |

> Os modelos marcados com `—` têm valores gerados dinamicamente ao executar o notebook.

Os dois melhores modelos foram **XGBoost** e **Random Forest**. O **XGBoost** foi selecionado para a etapa de otimização.

---

## 🔧 Otimização de Hiperparâmetros

Três métodos de busca foram aplicados ao XGBoost:

| Método | MAE | RMSE | R² | Tempo |
|--------|-----|------|----|-------|
| XGBoost baseline | 0.3096 | 0.4718 | 0.8301 | ~1s |
| Grid Search | 0.2943 | 0.4521 | 0.8440 | ~1min 21s |
| Randomized Search | 0.2842 | 0.4412 | 0.8515 | ~5min 36s |
| **Bayesian Search** | **0.2862** | **0.4408** | **0.8517** | ~6min 35s |

### Melhores Hiperparâmetros — XGBoost (Bayesian Search)

```
n_estimators:    ~300–500
max_depth:       ~5–7
learning_rate:   ~0.04
subsample:       ~0.8
colsample_bytree: ~0.8
```

---

## 🏆 Resultado Final

O melhor modelo obtido foi:

> **XGBoost + Bayesian Search → R² = 0.8517 | RMSE = 0.4408 (~USD 44k de erro médio)**

**Evolução do desempenho ao longo do projeto:**
- Regressão Linear → XGBoost baseline: **-36.7% no RMSE**
- XGBoost baseline → XGBoost Bayesian: **-6.6% adicional**
- **Ganho total: -40.9% no RMSE** do início ao fim

**Feature mais importante:** `MedInc` — confirma e quantifica a correlação de +0.688 observada na EDA. `Latitude` e `Longitude` juntas têm o segundo maior peso, capturando a valorização geográfica da faixa costeira.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Pandas** — manipulação de dados
- **NumPy** — operações numéricas
- **Matplotlib / Seaborn** — visualizações
- **Scikit-learn** — modelos de ML, pré-processamento e otimização
- **XGBoost** — modelo de gradient boosting
- **Scikit-optimize (BayesSearchCV)** — busca bayesiana

---

## 📁 Estrutura do Repositório

```
MACHINE LEARNING/
├── AV1/
└── AV2/
    ├── Classificacao/
    ├── Clusterizacao/
    └── Regressao/
        ├── regressao_Pedro_Dutra.ipynb  # notebook
        └── README.md                    # esse arquivo
```

> **Nota:** O dataset é carregado automaticamente via `sklearn.datasets.fetch_california_housing` — nenhum download ou arquivo externo é necessário.

---

## ▶️ Como Executar

1. Abra o notebook no **Google Colab**
2. Execute as células em ordem
3. As etapas de otimização podem levar alguns minutos (Bayesian ~6min, Randomized ~5min)