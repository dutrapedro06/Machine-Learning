# Sleep Disorder Risk Classification

**Aluno:** Pedro Pereira Dutra  
**RA:** 24101026  
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
| Healthy | 54.156 | 54,2% |
| Mild | 33.479 | 33,5% |
| Moderate | 8.299 | 8,3% |
| Severe | 4.066 | 4,1% |

> O dataset é **desbalanceado**: Healthy representa mais da metade dos registros, enquanto Severe representa apenas 4%. Por isso, **acurácia sozinha não é uma métrica confiável** — um modelo que chutasse "Healthy" para tudo atingiria 54% sem aprender nada. A métrica principal adotada neste projeto é o **F1-Macro**, que trata todas as classes igualmente.

---

## 🔍 Análise Exploratória (EDA)

Foram realizadas 12 visualizações para entender a relação entre as variáveis e o risco de distúrbio do sono. As principais descobertas:

- **Qualidade do sono** (`sleep_quality_score`): queda drástica da classe Healthy (média 5,8) para Severe (média 2,3) — a variável com a relação mais clara
- **Duração do sono** (`sleep_duration_hrs`): pessoas Severe dormem em média 2 horas a menos que as Healthy (4,9h vs 7,0h)
- **Nível de estresse** (`stress_score`): progressão consistente de 5,0 (Healthy) até 7,5 (Severe)
- **Condição mental**: pessoas com Ansiedade, Depressão ou ambas concentram muito mais casos Moderate e Severe
- **Cafeína antes de dormir**: consumo quase dobra do Healthy (~34mg) para Severe (~59mg)
- **Horas trabalhadas**: carga elevada (8h+) está associada a maior risco
- **País e gênero**: baixo poder preditivo — os padrões se mantêm uniformes entre grupos

---

## ⚙️ Pré-processamento

1. **Remoção de colunas irrelevantes:** `person_id` e `country`
2. **Codificação de variáveis categóricas** com `LabelEncoder`: `gender`, `occupation`, `chronotype`, `mental_health_condition`, `season`, `day_type`
3. **Codificação da variável alvo:** `Healthy=0`, `Mild=1`, `Moderate=2`, `Severe=3`
4. **Divisão dos dados:** 80% treino / 20% teste (estratificada)
5. **Teste com SMOTE:** O balanceamento foi avaliado, mas **piorou** o desempenho de todos os modelos — o SMOTE gerou instâncias sintéticas que não refletiram bem o padrão real dos dados. Optou-se por manter os dados originais com `class_weight='balanced'` nos modelos.

---

## 🤖 Modelos Testados

Foram comparados 6 algoritmos no conjunto de teste, usando **F1-Macro** como métrica principal e `class_weight='balanced'` para corrigir o desbalanceamento:

| Modelo | Acurácia | F1-Macro |
|--------|----------|----------|
| **Random Forest** | **89,53%** | **78,23%** |
| **Decision Tree** | **88,78%** | **76,48%** |
| Extra Trees | 83,80% | 69,95% |
| Naive Bayes | 71,84% | 61,21% |
| Logistic Regression | 69,03% | 59,35% |
| KNN | 61,60% | 36,45% |

Os dois melhores modelos em F1-Macro (**Random Forest** e **Decision Tree**) foram selecionados para o pipeline de otimização.

---

## 🔧 Otimização de Hiperparâmetros — Pipeline em Cascata

As três técnicas de otimização foram aplicadas de forma **sequencial e colaborativa** — cada etapa alimenta e refina a seguinte, em vez de competirem de forma independente:

```
Bayesian Search  →  Randomized Search  →  Grid Search
 (espaço amplo)      (região refinada)     (grade precisa)
```

- **Bayesian Search:** Explora um espaço amplo de forma inteligente, aprendendo quais regiões são mais promissoras a cada iteração
- **Randomized Search:** Recebe os melhores parâmetros do Bayesian e realiza busca aleatória em uma região estreitada ao redor desses valores
- **Grid Search:** Recebe os melhores parâmetros do Randomized e executa busca exaustiva em uma grade pequena e precisa

**Métrica de otimização: F1-Macro** em todas as etapas.

### Resultados — Decision Tree

| Etapa | F1-Macro | Acurácia | Tempo |
|-------|----------|----------|-------|
| Base (class_weight) | 76,48% | 88,78% | — |
| 1. Bayesian Search | 77,84% | 88,66% | 127,6s |
| 2. Randomized Search | 77,92% | 89,01% | 98,3s |
| 3. Grid Search | 77,92% | 89,01% | 71,6s |

**Parâmetros finais:** `criterion=entropy`, `max_depth=14`, `min_samples_leaf=1`, `min_samples_split=4`

### Resultados — Random Forest

| Etapa | F1-Macro | Acurácia | Tempo |
|-------|----------|----------|-------|
| Base (class_weight) | 78,23% | 89,53% | — |
| 1. Bayesian Search | 81,97% | 90,50% | ~30 min |
| 2. Randomized Search | 81,73% | 90,16% | ~33 min |
| 3. Grid Search | 81,77% | 90,19% | ~1h45 min |

**Parâmetros finais:** `n_estimators=176`, `max_depth=36`, `min_samples_leaf=3`, `min_samples_split=11`

---

## 🏆 Resultado Final

O melhor modelo obtido foi:

> **Random Forest + Pipeline Cascata → F1-Macro 81,77% | Acurácia 90,19%**

### Métricas por Classe — Modelo Final

| Classe | Precisão | Recall | F1 | Suporte |
|--------|----------|--------|----|---------|
| Healthy | 0,97 | 0,96 | 0,96 | 10.831 |
| Mild | 0,87 | 0,89 | 0,88 | 6.696 |
| Moderate | 0,65 | 0,67 | 0,66 | 1.660 |
| Severe | 0,81 | 0,74 | 0,77 | 813 |

O modelo demonstra que o aprendizado é **genuíno** — não é produto do desbalanceamento. A classe Moderate, por exemplo, saiu de recall 0,46 (modelo base) para 0,67 após o pipeline cascata, um ganho de +21 p.p. na classe mais difícil de detectar.

O pipeline cascata foi essencial para o Random Forest: sem o Bayesian e o Randomized estreitando o espaço antes, um Grid Search sobre o espaço amplo original seria computacionalmente inviável.

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
    │   ├── classificacao_Pedro_Dutra.ipynb  # notebook
    │   ├── README.md                        # esse arquivo
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

> ⚠️ **Atenção:** O pipeline de otimização do Random Forest é computacionalmente pesado (~2h30 no total). Recomenda-se usar GPU/TPU no Colab ou reduzir `n_iter` para prototipagem rápida.
