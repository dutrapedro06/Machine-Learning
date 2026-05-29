[README_repo.md](https://github.com/user-attachments/files/28371592/README_repo.md)
# 🤖 Machine Learning — Pedro Pereira Dutra

**Aluno:** Pedro Pereira Dutra

**Disciplina:** Aprendizado de Máquina  

**Instituição:** IDP

Repositório com todos os projetos desenvolvidos ao longo da disciplina, cobrindo MLOps, Classificação, Regressão e Clusterização.

---

## 📁 Estrutura do Repositório

```
Machine-Learning/
├── AV1/
│   └── Qualidade do Ar (MLOps)
│       ├── airquality_final.ipynb
│       ├── app.py
│       ├── Dockerfile
│       ├── docker-compose.yml
│       ├── requirements.txt
│       ├── bom.json / ruim.json
│       └── models/
│           ├── modelo_svr.pkl
│           ├── modelo_knn.pkl
│           └── scaler_ar.pkl
└── AV2/
    ├── Classificacao/
    │   ├── classificacao_Pedro_Dutra.ipynb
    │   ├── README.md
    │   └── sleep_health_dataset.csv
    ├── Regressao/
    │   ├── regressao_Pedro_Dutra.ipynb
    │   └── README.md
    └── Clusterizacao/
        ├── clusterizacao_Pedro_Dutra_final.ipynb
        └── README.md
```

---

## 📂 AV1 — API de Qualidade do Ar (MLOps)

**Dataset:** Air Quality UCI  
**Tarefa:** Prever a concentração de CO (mg/m³) e classificar a qualidade do ar

Pipeline completo de MLOps: treinamento de modelos, exportação, API REST com Flask e deploy em container Docker.

### Modelos
- **SVR** (modelo principal) — Support Vector Regression com kernel RBF
- **KNN** (comparação)

### API
A API expõe duas rotas de predição (`/predict/svr` e `/predict/knn`) que recebem leituras dos sensores em JSON e retornam a concentração prevista de CO e a classificação da qualidade do ar:

| Classificação | Condição |
|---|---|
| **bom** | CO ≤ 4 mg/m³ |
| **medio** | 4 < CO ≤ 9 mg/m³ |
| **ruim** | CO > 9 mg/m³ |

### Como executar
```bash
docker-compose up -d --build
curl -X POST -H "Content-Type: application/json" -d @ruim.json http://localhost:5000/predict/svr
```

→ [README completo da AV1](./AV1/README.md)

---

## 📂 AV2 — Notebooks de Machine Learning

### 📘 Notebook 1 — Classificação

**Dataset:** Sleep Health & Daily Performance (100.000 registros)  
**Tarefa:** Prever o risco de distúrbio do sono (`Healthy` / `Mild` / `Moderate` / `Severe`)

O dataset é desbalanceado (54% Healthy), por isso a métrica principal é **F1-Macro** — não acurácia. Os modelos foram treinados com `class_weight='balanced'` e otimizados via **pipeline em cascata**: Bayesian → Randomized → Grid Search, onde cada etapa alimenta a seguinte.

| Modelo | F1-Macro | Acurácia |
|--------|----------|----------|
| Random Forest (pipeline cascata) | **81,77%** | **90,19%** |
| Decision Tree (pipeline cascata) | 77,92% | 89,01% |

**Resultado final:** Random Forest com `n_estimators=176`, `max_depth=36` — F1-Macro 81,77%

→ [README completo da Classificação](./AV2/Classificacao/README.md)

---

### 📗 Notebook 2 — Regressão

**Dataset:** California Housing (20.640 registros, sklearn)  
**Tarefa:** Prever o valor mediano de imóveis em blocos residenciais da Califórnia

| Modelo | R² | RMSE | MAE |
|--------|----|------|-----|
| Regressão Linear | 0,5758 | 0,7456 | 0,5332 |
| Random Forest | 0,8051 | 0,5053 | 0,3275 |
| **XGBoost + Bayesian Search** | **0,8517** | **0,4408** | **0,2862** |

**Resultado final:** XGBoost otimizado com Bayesian Search — R² = 0,8517, ~USD 44k de erro médio. Ganho total de **-40,9% no RMSE** do modelo linear ao final.

→ [README completo da Regressão](./AV2/Regressao/README.md)

---

### 📙 Notebook 3 — Clusterização

**Dataset:** COVID-19 Municipal — Brazil (142.799 registros → 4.236 municípios únicos)  
**Tarefa:** Agrupar municípios brasileiros por perfil epidemiológico da COVID-19 (primeira onda)

Foram comparados K-Means, Agglomerative Clustering e DBSCAN. Escolha de k=4 justificada por cotovelo de inércia e granularidade epidemiológica.

| Cluster | Municípios | Perfil |
|---------|------------|--------|
| C0 | 90 (2,1%) | Alta transmissão, mortalidade controlada |
| C1 | 115 (2,7%) | Poucos casos, taxa inflada por subnotificação |
| C2 | 3.438 (81,2%) | Baixo impacto — maioria do interior |
| C3 | 593 (14,0%) | Alto impacto consolidado — maior urgência |

**Modelo principal:** K-Means (k=4) — centróides interpretáveis e eficiência computacional (0,1s).  
**Melhor métrica:** Agglomerative Ward → Silhouette 0,6722 | Davies-Bouldin 0,6953.

→ [README completo da Clusterização](./AV2/Clusterizacao/README.md)

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Pandas / NumPy** — manipulação de dados
- **Matplotlib / Seaborn** — visualizações
- **Scikit-learn** — modelos, pré-processamento, métricas
- **XGBoost** — gradient boosting (Regressão)
- **Scikit-optimize** — Bayesian Search
- **Imbalanced-learn** — SMOTE (testado na Classificação)
- **Flask** — API REST (AV1)
- **Docker** — containerização (AV1)

---

## ▶️ Como Executar (AV2)

1. Abra o notebook desejado no **Google Colab**
2. Execute as células em ordem
3. Datasets:
   - **Classificação:** baixar do [Kaggle](https://www.kaggle.com/datasets/mohankrishnathalla/sleep-health-and-daily-performance-dataset) e salvar no Drive
   - **Regressão:** carregado automaticamente via `sklearn`
   - **Clusterização:** baixado automaticamente via `opendatasets` (requer conta Kaggle)
