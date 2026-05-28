# COVID-19 Municipal Clustering — Brazil

**Aluno:** Pedro Pereira Dutra — RA: 24101026

**Disciplina:** Aprendizado de Máquina — Notebook 3 (Clusterização)

---

## 📋 Descrição do Projeto

Este projeto tem como objetivo **agrupar os municípios brasileiros em clusters** com base em seu perfil epidemiológico durante a pandemia de COVID-19. A clusterização permite identificar grupos de municípios com padrões similares de incidência e mortalidade, revelando diferentes realidades da pandemia no território nacional.

O problema é tratado como **aprendizado não supervisionado**, com comparação entre três algoritmos de clusterização: K-Means, DBSCAN e Agglomerative Clustering.

---

## 📊 Dataset

**Nome:** COVID-19 Open Datasets for Brazil  
**Fonte:** [Kaggle](https://www.kaggle.com/datasets/cprete/covid19-open-datasets-for-brazil)  
**Origem:** Painel oficial do Ministério da Saúde (HIST_PAINEL_COVIDBR)  
**Tamanho:** 142.799 linhas (município × data) → 4.236 municípios únicos

O dataset registra o histórico acumulado e diário de casos e óbitos de COVID-19 por município brasileiro, com dados até junho de 2020 (primeira onda).

### Indicadores utilizados na clusterização

| Variável | Descrição |
|----------|-----------|
| `casos_por_100k` | Casos acumulados por 100 mil habitantes |
| `obitos_por_100k` | Óbitos acumulados por 100 mil habitantes |
| `taxa_mortalidade` | Proporção de óbitos em relação aos casos confirmados |

---

## 🔍 Análise Exploratória (EDA)

Foram realizadas visualizações sobre distribuição dos indicadores, composição regional e correlações. As principais descobertas:

- O dataset foi **agregado de 142.799 registros temporais para 4.236 municípios únicos** com pelo menos um caso registrado
- A **normalização por 100k habitantes foi essencial**: sem ela, São Paulo e Rio de Janeiro dominariam os clusters pelo volume absoluto
- A **Região Norte** apresenta a maior taxa de mortalidade por 100k; o **Sul** tem a maior incidência de casos — reflexo de diferenças em testagem e infraestrutura hospitalar
- As distribuições são **fortemente assimétricas**: 75% dos municípios têm zero óbitos por 100k, e a taxa de mortalidade exibe comportamento bimodal
- A variável `Recuperadosnovos` foi removida das features: apenas 44 dos 142.799 registros tinham valor válido

---

## ⚙️ Pré-processamento

1. **Agregação temporal:** dados diários colapsados por município (máximo acumulado)
2. **Criação de indicadores por 100k habitantes** para comparabilidade entre municípios de tamanhos diferentes
3. **Remoção de variáveis com alta taxa de ausentes:** `Recuperadosnovos` (99,97% nulos)
4. **Imputação pela mediana** nos indicadores restantes — mais robusta que a média para dados com outliers extremos
5. **Normalização com StandardScaler** (média 0, desvio padrão 1)
6. **PCA 2D** apenas para visualização — a clusterização foi realizada no espaço original de 3 variáveis

---

## 🔢 Escolha do Número de Clusters

Três critérios foram combinados para definir k=4:

| Critério | k=3 | k=4 | k=5 |
|----------|-----|-----|-----|
| Cotovelo (Inércia) | Queda acentuada | **Ponto de inflexão** | Redução leve |
| Silhouette Score | **0,7138 (pico)** | 0,6477 | 0,6062 |
| Davies-Bouldin Index | **0,7988 (melhor)** | 0,8530 | 0,8359 |

**Decisão: k=4.** Embora k=3 produza as melhores métricas, k=4 é justificado pelo cotovelo e pela granularidade epidemiológica: com k=3, os 593 municípios de alto impacto consolidado (C3) são absorvidos por outros clusters, perdendo um perfil epidemiologicamente distinto e interpretável.

---

## 🤖 Modelos Testados

Foram comparados três algoritmos de clusterização:

| Modelo | Silhouette | Davies-Bouldin | Clusters | Observação |
|--------|------------|----------------|----------|------------|
| K-Means Base (k=4) | 0,6477 | 0,8530 | 4 | Resultado de referência |
| K-Means Otimizado | 0,6477 | 0,8530 | 4 | Converge para o mesmo mínimo |
| **Agglomerative (ward, k=4)** | **0,6722** | **0,6953** | **4** | **Melhores métricas entre modelos com k=4** |
| DBSCAN (eps=0,8, ms=5) | 0,8111* | 0,2292* | 2 | *Só sobre não-ruído; apenas 2 clusters |
| DBSCAN Otimizado (eps=2,0) | 0,8808* | — | 2 | *Idem; incomparável com demais |

> *As métricas do DBSCAN excluem pontos classificados como ruído (~75% dos dados), tornando a comparação direta com K-Means e Agglomerative inadequada.

---

## 🔧 Otimização de Parâmetros

**K-Means:** busca em grade sobre `init` e `n_init`. A inicialização `k-means++` convergiu para Silhouette = 0,6477 em todas as configurações — a base já estava no ótimo. A inicialização `random` produziu 0,6460, levemente inferior e menos reprodutível.

**DBSCAN:** a escolha de `eps=0.8` foi validada pelo **K-Distance Graph** (gráfico de cotovelo das distâncias ao 5º vizinho mais próximo). A busca em grade revelou que `eps` menor (0,5) fragmenta em micro-clusters; `eps` maior (2,0) colapsa em apenas 2 clusters com 99,8% dos pontos no maior — confirmando que o DBSCAN não se adapta bem à estrutura deste dataset.

---

## 🏆 Resultado Final

O melhor modelo para k=4 foi:

> **Agglomerative Clustering (Ward, k=4) → Silhouette 0,6722 | Davies-Bouldin 0,6953**

O **K-Means foi adotado como modelo principal** pelos seguintes motivos:
- Produz **centróides interpretáveis** — vetores de médias que traduzem diretamente o perfil epidemiológico de cada cluster
- **Eficiência computacional**: 0,1s vs. 1,9s do Agglomerative
- A concordância moderada-boa entre os dois modelos (Adjusted Rand Index = 0,6943) confirma que chegam a interpretações compatíveis, sem contradições fundamentais

---

## 🗺️ Perfis dos Clusters Identificados

| Cluster | Municípios | Casos/100k | Óbitos/100k | Taxa Mortalidade | Perfil |
|---------|------------|------------|-------------|------------------|--------|
| **C0** | 90 (2,1%) | 1.612 | 34,6 | 2,6% | Alta transmissão, mortalidade controlada |
| **C1** | 115 (2,7%) | 24 | 16,0 | 75,3% | Poucos casos, taxa inflada por subnotificação |
| **C2** | 3.438 (81,2%) | 95 | 1,5 | 2,1% | Baixo impacto — maioria dos municípios |
| **C3** | 593 (14,0%) | 362 | 23,3 | 10,2% | Alto impacto consolidado |

- **C0** concentra municípios do Norte e Nordeste com surtos intensos mas menor registro de óbitos — possivelmente por população mais jovem ou subnotificação de mortes
- **C1** é um artefato estatístico: 1–2 óbitos em municípios com 1–2 casos registrados geram taxas de mortalidade acima de 75%
- **C2** representa a vasta maioria do interior brasileiro com baixíssima exposição na primeira onda
- **C3** reúne cidades médias com alta incidência *e* mortalidade absoluta elevada — o grupo de maior urgência epidemiológica

---

## ⚠️ Limitações

- **Subnotificação sistêmica no C1:** os 115 municípios com taxa de mortalidade média de 75,3% não são mais letais — notificaram 1–2 casos antes do primeiro óbito. Em municípios com menos de 20.000 habitantes e baixa estrutura de vigilância, o indicador `taxa_mortalidade` perde confiabilidade
- **Corte temporal da primeira onda:** os dados cobrem apenas até junho de 2020. O Cluster 2 provavelmente teve composição radicalmente diferente após a segunda onda (jan–fev 2021), quando o vírus chegou ao interior mais remoto
- **Ausência de covariáveis estruturais:** sem dados de leitos de UTI, IDH e conectividade viária, os clusters capturam o *resultado* epidemiológico, não suas causas

**Melhorias futuras:**
- Incorporar o [CNES](https://cnes.datasus.gov.br/) para adicionar leitos de UTI e cobertura hospitalar como covariáveis
- Aplicar clusterização longitudinal com DTW para capturar a evolução entre as ondas
- Testar **K-Medoids (PAM)** para maior robustez a outliers como os do C1
- Avaliar **Gaussian Mixture Models** para clusters sobrepostos nas fronteiras entre C2 e C3

---

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **Pandas** — manipulação e agregação dos dados
- **NumPy** — operações numéricas
- **Matplotlib / Seaborn** — visualizações
- **Scikit-learn** — modelos de clusterização, pré-processamento, PCA e métricas
- **Scikit-optimize** — busca bayesiana de hiperparâmetros

---

## 📁 Estrutura do Repositório

```
MACHINE LEARNING/
├── AV1/
└── AV2/
    ├── Classificacao/
    ├── Clusterizacao/
    │   ├── clusterizacao_Pedro_Dutra_final.ipynb  # notebook
    │   └── README.md                               # esse arquivo
    └── Regressao/
```

> **Nota:** O dataset é baixado automaticamente do Kaggle via `opendatasets`. É necessário ter uma conta no Kaggle e fornecer as credenciais (`kaggle.json`) quando solicitado na primeira célula.

---

## ▶️ Como Executar

1. Abra o notebook no **Google Colab**
2. Execute a primeira célula para instalar as dependências e baixar o dataset
3. Forneça suas credenciais do Kaggle quando solicitado
4. Execute as células em ordem
