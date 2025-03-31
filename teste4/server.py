from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

def ler_csv(caminho):
    dados = []
    try:
        if not os.path.exists(caminho):
            raise FileNotFoundError(f"Arquivo '{caminho}' não encontrado.")
            
        with open(caminho, 'r', encoding='utf-8-sig') as arquivo_csv:  # Alterado para utf-8-sig
            leitor_csv = csv.DictReader(arquivo_csv)
            print("Cabeçalhos do CSV:", leitor_csv.fieldnames)  # Debug: mostra os cabeçalhos
            
            for linha in leitor_csv:
                if linha:  # Verifica se a linha não está vazia
                    # Remove espaços extras dos valores e chaves
                    linha_limpa = {k.strip(): v.strip() if isinstance(v, str) else v 
                                for k, v in linha.items()}
                    dados.append(linha_limpa)
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
    return dados

caminho_csv = os.path.join(os.path.dirname(__file__), 'operadoras.csv')
operadoras = ler_csv(caminho_csv)

print(f"Total de operadoras carregadas: {len(operadoras)}")
if operadoras:
    print("Exemplo de uma operadora:", operadoras[0])

def buscar_operadoras(termo):
    if not termo or not operadoras:
        return []
    
    termo_lower = termo.lower().strip()
    resultados = []
    
    for operadora in operadoras:
        try:
            # Verifica em todos os campos string (não apenas os específicos)
            for valor in operadora.values():
                if isinstance(valor, str) and termo_lower in valor.lower():
                    resultados.append(operadora)
                    break  # Se encontrou em um campo, não precisa verificar os outros
        except AttributeError:
            continue
    
    return resultados

@app.route('/buscar', methods=['GET'])
def buscar():
    termo = request.args.get('termo', '').strip()
    print(f"Termo de busca recebido: '{termo}'")  # Debug
    
    if not termo:
        return jsonify({"error": "Parâmetro 'termo' é obrigatório"}), 400
    
    resultados = buscar_operadoras(termo)
    print(f"Encontrados {len(resultados)} resultados")  # Debug
    
    # Adiciona informações de debug na resposta (apenas em desenvolvimento)
    debug_info = {
        "termo_buscado": termo,
        "total_resultados": len(resultados),
        "primeiros_resultados": resultados[:3] if resultados else []
    }
    
    return jsonify({
        "resultados": resultados,
        "_debug": debug_info if app.debug else None
    })

if __name__ == '__main__':
    # Teste rápido antes de iniciar o servidor
    if operadoras:
        teste_termo = operadoras[0]['Nome'].split()[0] if 'Nome' in operadoras[0] else 'saude'
        print(f"\nTeste automático com termo '{teste_termo}':")
        print(buscar_operadoras(teste_termo)[:1])
    
    app.run(debug=True, host='0.0.0.0', port=5000)