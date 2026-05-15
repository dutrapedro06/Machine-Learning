# Sleep Disorder Risk Classification

**Aluno:** Pedro Pereira Dutra

**Disciplina:** Aprendizado de Máquina — Notebook 1 (Classificação)

---

## 📋 Descrição do Projeto

Este projeto tem como objetivo prever o **risco de distúrbio do sono** de uma pessoa com base em seus hábitos de saúde, sono e estilo de vida. Os distúrbios classificados incluem:

- Dificuldade para dormir
- Acordar várias vezes durante a noite
- Sonolência excessiva durante o dia
- Comportamentos anormais (ronco, movimentos)

O problema é tratado como uma **classificação multiclasse**, com quatro categorias de risco: `Healthy`, `Mild`, `Moderate` e `Severe`.

---

## 📊 Dataset

**Nome:** Sleep Health & Daily Performance  
**Fonte:** [Kaggle](https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset)  
**Tamanho:** 100.000 registros sintéticos

Cada registro captura um instantâneo diário completo de um paciente, incluindo:
- Métricas da arquitetura do sono (duração, qualidade)
- Comportamentos de estilo de vida (exercício, cafeína, horas trabalhadas)
- Estado psicológico (estresse, condição mental)
- Resultados cognitivos do dia seguinte

### Distribuição das Classes

| Classe | Registros | Percentual |
|--------|-----------|------------|
| Healthy | 54.156 | 54% |
| Mild | 33.479 | 33% |
| Moderate | 8.299 | 8% |
| Severe | 4.066 | 4% |

---

## 🔍 Análise Exploratória (EDA)

Foram realizadas 12 visualizações para entender a relação entre as variáveis e o risco de distúrbio do sono. As principais descobertas:

- **Qualidade do sono** (`sleep_quality_score`): queda drástica da classe Healthy (média 5.8) para Severe (média 2.3) — a variável com a relação mais clara
- **Duração do sono** (`sleep_duration_hrs`): pessoas Severe dormem em média 2 horas a menos que as Healthy (4.9h vs 7.0h)
- **Nível de estresse** (`stress_score`): progressão consistente de 5.0 (Healthy) até 7.5 (Severe)
- **Condição mental**: pessoas com Ansiedade, Depressão ou ambas concentram muito mais casos Moderate e Severe
- **Cafeína antes de dormir**: consumo quase dobra do Healthy (~34mg) para o Severe (~59mg)
- **Horas trabalhadas**: carga elevada (8h+) está associada a maior risco
- **País e gênero**: baixo poder preditivo — os padrões se mantêm uniformes entre grupos

---

## ⚙️ Pré-processamento

1. **Remoção de colunas irrelevantes:** `person_id` e `country`
2. **Codificação de variáveis categóricas** com `LabelEncoder`: `gender`, `occupation`, `chronotype`, `mental_health_condition`, `season`, `day_type`
3. **Codificação da variável alvo:** `Healthy=1`, `Mild=2`, `Moderate=3`, `Severe=0` (ordem alfabética)
4. **Divisão dos dados:** 80% treino / 20% teste (estratificada)
5. **Teste com SMOTE:** O balanceamento foi avaliado, mas **piorou** o desempenho de todos os modelos — optou-se por manter os dados originais

---

## 🤖 Modelos Testados

Foram comparados 6 algoritmos no conjunto de teste sem balanceamento:

| Modelo | Acurácia | F1-Score (weighted) |
|--------|----------|----------------------|
| **Decision Tree** | **90.20%** | **90.20%** |
| **Random Forest** | **90.16%** | **89.79%** |
| Extra Trees | 83.95% | 83.11% |
| Logistic Regression | 73.97% | 72.96% |
| Naive Bayes | 71.84% | 72.34% |
| KNN | 61.60% | 58.24% |

Os dois melhores modelos (**Decision Tree** e **Random Forest**) foram selecionados para otimização de hiperparâmetros.

---

## 🔧 Otimização de Hiperparâmetros

Três métodos de busca foram aplicados a ambos os modelos:

| Método | Decision Tree | Random Forest |
|--------|--------------|---------------|
| Base | 90.20% | 89.53% |
| Bayesian Search | 90.90% (+0.70%) | 90.46% (+0.93%) |
| **Randomized Search** | **91.12% (+0.92%)** | 90.31% (+0.78%) |
| Grid Search | 90.54% (+0.34%) | 90.29% (+0.76%) |

### Melhores Hiperparâmetros — Decision Tree (Randomized Search)

```
max_depth:         None  (sem limite de profundidade)
min_samples_leaf:  4
min_samples_split: 20
criterion:         entropy
```

---

## 🏆 Resultado Final

O melhor modelo obtido foi:

> **Decision Tree + Randomized Search → 91.12% de acurácia**

A Decision Tree superou o Random Forest em todos os métodos de otimização, resultado atípico que pode ser explicado pela natureza **sintética e bem estruturada** do dataset, que favorece modelos mais simples.

O **Randomized Search** se mostrou o método mais eficiente: encontrou o melhor resultado em apenas ~48 segundos, enquanto o Grid Search levou ~72 segundos com resultado inferior — confirmando que a exploração aleatória pode ser tão eficaz quanto testar todas as combinações, com menor custo computacional.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Pandas** — manipulação de dados
- **NumPy** — operações numéricas
- **Matplotlib / Seaborn** — visualizações
- **Scikit-learn** — modelos de ML, pré-processamento e otimização
- **Imbalanced-learn (SMOTE)** — teste de balanceamento de classes
- **Scikit-optimize (BayesSearchCV)** — busca bayesiana

---

## 📁 Estrutura do Repositório

```
MACHINE LEARNING/
├── AV1/
└── AV2/
    ├── Classificacao/
    │   ├── classificacao_Pedro_Dutra.ipynb #notebok
    │   ├── README.md                       # esse arquivo
    │   └── sleep_health_dataset.csv
    ├── Clusterizacao/
    └── Regressao/
```

> **Nota:** O dataset deve ser baixado do [Kaggle](https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset) e salvo em `/content/drive/MyDrive/sleep_health_dataset.csv` (Google Drive) ou o caminho ajustado no notebook.

---

## ▶️ Como Executar

1. Abra o notebook no **Google Colab**
2. Monte o Google Drive quando solicitado
3. Faça o upload do dataset no caminho indicado acima
4. Execute as células em ordem