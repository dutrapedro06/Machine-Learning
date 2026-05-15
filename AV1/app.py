from flask import Flask, request, Response
import pickle
import pandas as pd
import json

app = Flask(__name__)

# Colunas que o modelo espera (mesma ordem do treino)
COLUNAS = [
    'PT08.S1(CO)', 'C6H6(GT)', 'PT08.S2(NMHC)', 'NOx(GT)',
    'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)',
    'T', 'RH', 'AH', 'Hour'
]

# Carregando os modelos e o Scaler
with open('models/modelo_svr.pkl', 'rb') as f:
    modelo_svr = pickle.load(f)

with open('models/modelo_knn.pkl', 'rb') as f:
    modelo_knn = pickle.load(f)

with open('models/scaler_ar.pkl', 'rb') as f:
    scaler = pickle.load(f)


def resposta(dados, status=200):
    """Retorna JSON com acentos corretamente exibidos."""
    return Response(
        json.dumps(dados, ensure_ascii=False, indent=2),
        status=status,
        mimetype='application/json'
    )


def classificar_co(valor):
    """Classifica a qualidade do ar com base no valor previsto de CO(GT).
    Critério conforme OMS / EPA (adaptado para fins acadêmicos):
      bom   : CO(GT) <= 4
      medio : 4 < CO(GT) <= 9
      ruim  : CO(GT) > 9
    """
    if valor <= 4:
        return 'bom'
    elif valor <= 9:
        return 'medio'
    else:
        return 'ruim'


# ── Rota raiz ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return resposta({
        'api': 'Previsão de Qualidade do Ar',
        'descricao': 'Prevê a concentração de CO(GT) em mg/m³',
        'rotas': {
            'POST /predict/svr': 'Previsão com modelo SVR (melhor precisão)',
            'POST /predict/knn': 'Previsão com modelo KNN',
            'GET  /example':     'Exemplos de JSON para teste'
        }
    })


# ── Rota de exemplos ─────────────────────────────────────────────────────────
@app.route('/example')
def example():
    return resposta({
        'descricao': 'Envie um POST para /predict/svr ou /predict/knn com este formato',
        'exemplo_ar_ruim': {
            'PT08.S1(CO)': 1360.0,
            'C6H6(GT)':    11.9,
            'PT08.S2(NMHC)': 1046.0,
            'NOx(GT)':     166.0,
            'PT08.S3(NOx)': 1056.0,
            'NO2(GT)':     113.0,
            'PT08.S4(NO2)': 1692.0,
            'PT08.S5(O3)': 1268.0,
            'T':    13.6,
            'RH':   48.9,
            'AH':   0.7578,
            'Hour': 18
        },
        'exemplo_ar_bom': {
            'PT08.S1(CO)': 900.0,
            'C6H6(GT)':    3.5,
            'PT08.S2(NMHC)': 750.0,
            'NOx(GT)':     60.0,
            'PT08.S3(NOx)': 1300.0,
            'NO2(GT)':     70.0,
            'PT08.S4(NO2)': 1500.0,
            'PT08.S5(O3)': 800.0,
            'T':    20.0,
            'RH':   55.0,
            'AH':   0.9,
            'Hour': 10
        }
    })


# ── Rota SVR ─────────────────────────────────────────────────────────────────
@app.route('/predict/svr', methods=['POST'])
def predict_svr():
    try:
        dados = request.get_json()
        df_input = pd.DataFrame([dados])[COLUNAS]
        dados_pad = scaler.transform(df_input)
        previsao = modelo_svr.predict(dados_pad)
        valor = float(previsao[0])

        return resposta({
            'modelo_utilizado':     'SVR (kernel=rbf, C=100)',
            'previsao_CO_GT_mg_m3': round(valor, 4),
            'qualidade_ar':         classificar_co(valor)
        })

    except KeyError as e:
        return resposta({'erro': f'Campo ausente: {str(e)}',
                         'colunas_necessarias': COLUNAS}, 400)
    except Exception as e:
        return resposta({'erro': str(e)}, 500)


# ── Rota KNN ─────────────────────────────────────────────────────────────────
@app.route('/predict/knn', methods=['POST'])
def predict_knn():
    try:
        dados = request.get_json()
        df_input = pd.DataFrame([dados])[COLUNAS]
        dados_pad = scaler.transform(df_input)
        previsao = modelo_knn.predict(dados_pad)
        valor = float(previsao[0])

        return resposta({
            'modelo_utilizado':     'KNN (k=15, weights=distance)',
            'previsao_CO_GT_mg_m3': round(valor, 4),
            'qualidade_ar':         classificar_co(valor)
        })

    except KeyError as e:
        return resposta({'erro': f'Campo ausente: {str(e)}',
                         'colunas_necessarias': COLUNAS}, 400)
    except Exception as e:
        return resposta({'erro': str(e)}, 500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
