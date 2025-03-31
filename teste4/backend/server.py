from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from urllib.parse import unquote




app = Flask(__name__)
CORS(app)
    

def ler_csv(caminho):
    """Função melhorada para leitura de CSV com tratamento de erros robusto"""
    dados = []
    try:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")
            
        with open(caminho, 'r', encoding='utf-8-sig') as arquivo_csv:
            leitor_csv = csv.DictReader(arquivo_csv)
            print("Cabeçalhos do CSV:", leitor_csv.fieldnames)
            
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
        raise  # Re-lança a exceção para tratamento superior
        
    return dados

def carregar_dados():
    """Carrega os dados com tratamento de erros global"""
    global operadoras
    try:
        caminho_csv = os.path.join(os.path.dirname(__file__), 'operadoras.csv')
        operadoras = ler_csv(caminho_csv)
        print(f"Total de operadoras carregadas: {len(operadoras)}")
        if operadoras:
            print("Exemplo de operadora:", {k: operadoras[0][k] for k in list(operadoras[0].keys())[:3]})
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
    resultados = []
    
    try:
        for operadora in operadoras:
            try:
                # Busca em todos os campos de texto
                if any(termo_lower in str(valor).lower() 
                      for valor in operadora.values() 
                      if valor and isinstance(valor, str)):
                    resultados.append(operadora)
            except Exception as e:
                print(f"Erro ao processar operadora: {e}")
                continue
                
    except Exception as e:
        print(f"Erro na busca: {e}")
        raise
        
    return resultados

@app.route('/api/buscar', methods=['GET'])
def buscar():
    """Endpoint principal com tratamento completo de erros"""
    try:
        termo = unquote(request.args.get('termo', '').strip())
        
        if not termo:
            return jsonify({
                "status": "error",
                "message": "Parâmetro 'termo' é obrigatório",
                "code": 400
            }), 400
        
        resultados = buscar_operadoras(termo)
        
        
        if app.debug:
            print(f"Busca por '{termo}': {len(resultados)} resultados")
        
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
        return jsonify({
            "status": "error",
            "message": "Erro interno no servidor",
            "code": 500
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificação de saúde da API"""
    return jsonify({
        "status": "healthy",
        "data_loaded": bool(operadoras),
        "operadoras_count": len(operadoras) if operadoras else 0
    })

if __name__ == '__main__':
    from datetime import datetime
    try:
        print(f"\n⚡ API iniciando em {datetime.now().isoformat()}")
        print("🔍 Teste automático:")
        if operadoras:
            teste_termo = operadoras[0].get('Nome', 'saude').split()[0]
            teste_resultados = buscar_operadoras(teste_termo)
            print(f"Busca por '{teste_termo}': {len(teste_resultados)} resultados")
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Falha ao iniciar servidor: {e}")