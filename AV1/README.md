# API de Qualidade do Ar — MLOps

Pipeline completo de Machine Learning para previsão da concentração de CO(GT)
(monóxido de carbono em mg/m³) usando o dataset Air Quality UCI.

---

## Estrutura do Projeto

```
entrega/
├── airquality_final.ipynb   ← Notebook completo (EDA + treino + exportação)
├── app.py                   ← API Flask com rotas SVR e KNN
├── Dockerfile               ← Imagem do container
├── docker-compose.yml       ← Orquestração do container
├── requirements.txt         ← Dependências Python
├── bom.json                 ← Exemplo de JSON com ar de boa qualidade
├── ruim.json                ← Exemplo de JSON com ar de má qualidade
└── models/
    ├── modelo_svr.pkl       ← Modelo SVR treinado (modelo principal)
    ├── modelo_knn.pkl       ← Modelo KNN treinado (comparação)
    └── scaler_ar.pkl        ← StandardScaler ajustado no treino
```

---

## Como Executar

### 1. Subir o container

```bash
docker-compose up -d --build
```

### 2. Verificar se está rodando

```bash
docker-compose ps
docker-compose logs
```

### 3. Testar a API

**Ver exemplos de JSON:**
```bash
curl http://localhost:5000/example
```

**Previsão com SVR — ar ruim (alto CO):**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d @ruim.json http://localhost:5000/predict/svr
```

**Previsão com SVR — ar bom (baixo CO):**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d @bom.json http://localhost:5000/predict/svr
```

**Previsão com KNN — ar ruim:**
```bash
curl -X POST -H "Content-Type: application/json" \
     -d @ruim.json http://localhost:5000/predict/knn
```

**Enviando os dados diretamente (sem arquivo):**
```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "PT08.S1(CO)": 1360.0,
    "C6H6(GT)": 11.9,
    "PT08.S2(NMHC)": 1046.0,
    "NOx(GT)": 166.0,
    "PT08.S3(NOx)": 1056.0,
    "NO2(GT)": 113.0,
    "PT08.S4(NO2)": 1692.0,
    "PT08.S5(O3)": 1268.0,
    "T": 13.6,
    "RH": 48.9,
    "AH": 0.7578,
    "Hour": 18
  }' http://localhost:5000/predict/svr
```

### 4. Parar o container

```bash
docker-compose down
```

---

## Formato do JSON de Entrada

| Campo | Descrição | Tipo |
|---|---|---|
| PT08.S1(CO) | Sensor de CO | float |
| C6H6(GT) | Benzeno em µg/m³ | float |
| PT08.S2(NMHC) | Sensor de NMHC | float |
| NOx(GT) | Óxidos de nitrogênio em ppb | float |
| PT08.S3(NOx) | Sensor de NOx | float |
| NO2(GT) | Dióxido de nitrogênio em µg/m³ | float |
| PT08.S4(NO2) | Sensor de NO2 | float |
| PT08.S5(O3) | Sensor de Ozônio | float |
| T | Temperatura em °C | float |
| RH | Umidade relativa em % | float |
| AH | Umidade absoluta em g/m³ | float |
| Hour | Hora do dia (0–23) | int |

---

## Formato da Resposta

```json
{
  "modelo_utilizado": "SVR (kernel=rbf, C=100)",
  "previsao_CO_GT_mg_m3": 4.2315,
  "qualidade_ar": "medio"
}
```

### Critério de Classificação da Qualidade do Ar

| Classificação | Condição |
|---|---|
| **bom** | CO(GT) ≤ 4 mg/m³ |
| **medio** | 4 < CO(GT) ≤ 9 mg/m³ |
| **ruim** | CO(GT) > 9 mg/m³ |

> Critério inspirado no valor-guia da OMS (4 mg/m³) e nas faixas do Air Quality Index da EPA,
> adotado aqui como critério acadêmico de interpretação.
