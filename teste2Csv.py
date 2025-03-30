import pandas as pd
import pdfplumber
import zipfile
import os

def extract_table_from_pdf(pdf_path):
    """Extrai tabelas de PDF usando pdfplumber"""
    all_tables = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_tables.append(table)
    
    # Converte todas as tabelas para DataFrames e concatena
    dfs = [pd.DataFrame(table[1:], columns=table[0]) for table in all_tables if table]
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def main():
    print("=== TESTE DE TRANSFORMAÇÃO DE DADOS ===")
    
    
    pdf_path = "downloads/Anexo I..pdf"
    csv_path = "Rol_de_Procedimentos.csv"
    zip_path = "Teste_Adeilton_Polovodoff.zip"  
    
    
    print("\n1. Extraindo tabelas do PDF...")
    try:
        df = extract_table_from_pdf(pdf_path)
        
        if df.empty:
            print("Nenhuma tabela encontrada no PDF.")
            return
            
        print("\nVisualização da tabela extraída (primeiras 5 linhas):")
        print(df.head())
        
        
        print("\n2. Processando e limpando os dados...")
        
        
        df = df.dropna(how='all')
        df = df.reset_index(drop=True)
        
        
        df = df.rename(columns={
            'OD': 'Odontológico',
            'AMB': 'Ambulatorial'
        })
        
        
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"\n3. Arquivo CSV salvo em: {csv_path}")
        
        
        print("\n4. Compactando o arquivo CSV...")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path)
        
        print(f"Arquivo compactado criado: {zip_path}")
        
        
        print("\n5. Verificação final:")
        df_final = pd.read_csv(csv_path)
        print(f"Total de registros no CSV: {len(df_final)}")
        print("\nPrimeiras linhas do arquivo final:")
        print(df_final.head())
        
    except Exception as e:
        print(f"\nOcorreu um erro: {str(e)}")

if __name__ == "__main__":
    main()