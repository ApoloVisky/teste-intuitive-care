from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from urllib.parse import unquote
from flasgger import Swagger
from datetime import datetime

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

def ler_csv(caminho):
    """Função melhorada para leitura de CSV com tratamento de erros robusto"""
    dados = []
    try:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")

        with open(caminho, 'r', encoding='utf-8-sig') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            for linha in leitor_csv:
                if linha:
                    linha_limpa = {
                        k.strip(): v.strip() if v and isinstance(v, str) else v
                        for k, v in linha.items()
                        if k and k.strip()
                    }
                    if linha_limpa:
                        dados.append(linha_limpa)
    except Exception as e:
        print(f"Erro crítico ao ler o arquivo CSV: {e}")
        raise
    return dados

def carregar_dados():
    """Carrega os dados com tratamento de erros global"""
    global operadoras
    try:
        caminho_csv = os.path.join(os.path.dirname(__file__), 'operadoras.csv')
        operadoras = ler_csv(caminho_csv)
    except Exception as e:
        print(f"Falha ao carregar dados: {e}")
        operadoras = []

# Carrega os dados ao iniciar
carregar_dados()

def buscar_operadoras(termo):
    """Busca otimizada com tratamento de erros"""
    if not termo or not operadoras:
        return []
    
    termo_lower = termo.lower().strip()
    return [op for op in operadoras if any(termo_lower in str(valor).lower() for valor in op.values() if isinstance(valor, str))]

@app.route('/api/buscar', methods=['GET'])
def buscar():
    """
    Busca operadoras pelo termo fornecido.
    ---
    parameters:
      - name: termo
        in: query
        type: string
        required: true
        description: Termo de busca para encontrar operadoras
    responses:
      200:
        description: Lista de operadoras encontradas
        schema:
          type: object
          properties:
            status:
              type: string
              example: success
            data:
              type: object
              properties:
                resultados:
                  type: array
                  items:
                    type: object
                total:
                  type: integer
            meta:
              type: object
              properties:
                termo_buscado:
                  type: string
                timestamp:
                  type: string
                  format: date-time
      400:
        description: Erro - termo não informado
      500:
        description: Erro interno no servidor
    """
    try:
        termo = unquote(request.args.get('termo', '').strip())

        if not termo:
            return jsonify({"status": "error", "message": "Parâmetro 'termo' é obrigatório", "code": 400}), 400

        resultados = buscar_operadoras(termo)

        return jsonify({
            "status": "success",
            "data": {
                "resultados": resultados,
                "total": len(resultados)
            },
            "meta": {
                "termo_buscado": termo,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        print(f"Erro no endpoint /buscar: {e}")
        return jsonify({"status": "error", "message": "Erro interno no servidor", "code": 500}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Verifica o status da API e a carga de dados.
    ---
    responses:
      200:
        description: Status da API
        schema:
          type: object
          properties:
            status:
              type: string
              example: healthy
            data_loaded:
              type: boolean
            operadoras_count:
              type: integer
    """
    return jsonify({
        "status": "healthy",
        "data_loaded": bool(operadoras),
        "operadoras_count": len(operadoras) if operadoras else 0
    })

if __name__ == '__main__':
    try:
        print(f"\n⚡ API iniciando em {datetime.now().isoformat()}")
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Falha ao iniciar servidor: {e}")
