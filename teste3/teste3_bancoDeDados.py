import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
import zipfile
import requests
from datetime import datetime, timedelta

# Configurações do banco de dados
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'admin',
    'password': 'admin123',
    'database': 'ans_dados',
    'auth_plugin': 'mysql_native_password'
}

def create_db_connection():
    """Cria e retorna a conexão com o banco de dados"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("Conexão com o banco estabelecida com sucesso")
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

def download_file(url, save_path):
    """Baixa um arquivo da URL e salva localmente"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extrai arquivo ZIP para o diretório especificado"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Erro ao extrair {zip_path}: {e}")
        return False

def check_table_structure(conn):
    """Verifica a estrutura atual da tabela operadoras"""
    try:
        cursor = conn.cursor()
        cursor.execute("DESCRIBE operadoras")
        columns = cursor.fetchall()
        print("\nEstrutura atual da tabela operadoras:")
        for col in columns:
            print(f"Coluna: {col[0]}, Tipo: {col[1]}, Tamanho: {col[2]}")
    except Error as e:
        print(f"Erro ao verificar estrutura da tabela: {e}")

def setup_database_tables(conn):
    """Cria as tabelas no banco de dados com tamanhos adequados"""
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS operadoras (
            registro_ans VARCHAR(20) PRIMARY KEY,
            cnpj VARCHAR(20),
            razao_social VARCHAR(255),
            nome_fantasia VARCHAR(255),
            modalidade VARCHAR(100),
            logradouro VARCHAR(255),
            numero VARCHAR(50),
            complemento VARCHAR(255),
            bairro VARCHAR(100),
            cidade VARCHAR(100),
            uf VARCHAR(2),
            cep VARCHAR(10),
            ddd VARCHAR(5),
            telefone VARCHAR(50),
            fax VARCHAR(50),
            email VARCHAR(100),
            representante VARCHAR(255),
            cargo_representante VARCHAR(100),
            data_registro_ans DATE,
            INDEX (razao_social),
            INDEX (cnpj)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data DATE,
            registro_ans VARCHAR(20),
            conta VARCHAR(100),
            descricao VARCHAR(255),
            valor DECIMAL(15,2),
            periodo VARCHAR(20),
            FOREIGN KEY (registro_ans) REFERENCES operadoras(registro_ans),
            INDEX (data),
            INDEX (registro_ans),
            INDEX (descricao)
        )
        """)
        
        conn.commit()
        print("Tabelas criadas/verificadas com sucesso")
        return True
    except Error as e:
        print(f"Erro ao criar tabelas: {e}")
        return False

def import_operadoras(conn):
    """Importa dados das operadoras com tratamento completo"""
    try:
        file_path = "dados_ans/operadoras_ativas.csv"
        if not os.path.exists(file_path):
            url = "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
            if not download_file(url, file_path):
                return False
        
        # Ler o arquivo CSV com tratamento robusto
        try:
            df = pd.read_csv(file_path, sep=';', encoding='latin1', dtype=str)
            print(f"CSV lido com sucesso. Linhas: {len(df)}")
            
            # Padronizar nomes de colunas
            df.columns = [col.strip().replace(' ', '_').lower() for col in df.columns]
            print("Colunas encontradas:", df.columns.tolist())
            
            # Renomear colunas para padrão do banco
            column_mapping = {
                'registro_ans': 'registro_ans',
                'cnpj': 'cnpj',
                'razao_social': 'razao_social',
                'nome_fantasia': 'nome_fantasia',
                'modalidade': 'modalidade',
                'logradouro': 'logradouro',
                'numero': 'numero',
                'complemento': 'complemento',
                'bairro': 'bairro',
                'cidade': 'cidade',
                'uf': 'uf',
                'cep': 'cep',
                'ddd': 'ddd',
                'telefone': 'telefone',
                'fax': 'fax',
                'endereco_eletronico': 'email',
                'representante': 'representante',
                'cargo_representante': 'cargo_representante',
                'data_registro_ans': 'data_registro_ans'
            }
            
            df = df.rename(columns=column_mapping)
            
        except Exception as e:
            print(f"Falha ao processar CSV: {str(e)}")
            return False

        # Função para ajustar campos
        def ajustar_campo(valor, tamanho_max):
            if pd.isna(valor) or valor in [None, '', 'nan', 'NaN']:
                return None
            valor_str = str(valor).strip()
            return valor_str[:tamanho_max] if len(valor_str) > tamanho_max else valor_str

        # SQL para inserção
        insert_sql = """
        INSERT INTO operadoras (
            registro_ans, cnpj, razao_social, nome_fantasia, modalidade,
            logradouro, numero, complemento, bairro, cidade, uf, cep,
            ddd, telefone, fax, email, representante, cargo_representante, data_registro_ans
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            cnpj = VALUES(cnpj),
            razao_social = VALUES(razao_social),
            nome_fantasia = VALUES(nome_fantasia),
            modalidade = VALUES(modalidade),
            logradouro = VALUES(logradouro),
            numero = VALUES(numero),
            complemento = VALUES(complemento),
            bairro = VALUES(bairro),
            cidade = VALUES(cidade),
            uf = VALUES(uf),
            cep = VALUES(cep),
            ddd = VALUES(ddd),
            telefone = VALUES(telefone),
            fax = VALUES(fax),
            email = VALUES(email),
            representante = VALUES(representante),
            cargo_representante = VALUES(cargo_representante),
            data_registro_ans = VALUES(data_registro_ans)
        """

        cursor = conn.cursor()
        batch_size = 500
        total_rows = len(df)
        imported = 0

        print(f"Iniciando importação de {total_rows} registros...")

        for i in range(0, total_rows, batch_size):
            batch = df.iloc[i:i + batch_size]
            batch_data = []
            
            for _, row in batch.iterrows():
                try:
                    data_tuple = (
                        ajustar_campo(row.get('registro_ans'), 20),
                        ajustar_campo(row.get('cnpj'), 20),
                        ajustar_campo(row.get('razao_social'), 255),
                        ajustar_campo(row.get('nome_fantasia'), 255),
                        ajustar_campo(row.get('modalidade'), 100),
                        ajustar_campo(row.get('logradouro'), 255),
                        ajustar_campo(row.get('numero'), 50),
                        ajustar_campo(row.get('complemento'), 255),
                        ajustar_campo(row.get('bairro'), 100),
                        ajustar_campo(row.get('cidade'), 100),
                        ajustar_campo(row.get('uf'), 2),
                        ajustar_campo(row.get('cep'), 10),
                        ajustar_campo(row.get('ddd'), 5),
                        ajustar_campo(row.get('telefone'), 50),
                        ajustar_campo(row.get('fax'), 50),
                        ajustar_campo(row.get('email'), 100),
                        ajustar_campo(row.get('representante'), 255),
                        ajustar_campo(row.get('cargo_representante'), 100),
                        pd.to_datetime(row.get('data_registro_ans'), format='%d/%m/%Y', errors='coerce').to_pydatetime()
                        if not pd.isna(row.get('data_registro_ans')) else None
                    )
                    batch_data.append(data_tuple)
                except Exception as e:
                    print(f"Erro ao processar linha {_}: {str(e)}")
                    continue

            try:
                cursor.executemany(insert_sql, batch_data)
                conn.commit()
                imported += len(batch_data)
                print(f"Progresso: {min(i + batch_size, total_rows)}/{total_rows} registros")
            except Error as e:
                conn.rollback()
                print(f"Erro no lote {i//batch_size + 1}: {str(e)}")
                continue

        print(f"Importação concluída. Total de registros importados: {imported}/{total_rows}")
        return imported > 0

    except Exception as e:
        conn.rollback()
        print(f"Erro fatal ao importar operadoras: {str(e)}")
        return False

def import_demonstracoes(conn, anos=2):
    """Importa dados das demonstrações contábeis para o banco de dados"""
    try:
        base_url = "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
        current_year = datetime.now().year
        
        # 1. Primeiro verificamos quais operadoras existem no banco
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT registro_ans FROM operadoras")
        operadoras_existentes = {row['registro_ans'] for row in cursor.fetchall()}
        
        if not operadoras_existentes:
            print("Nenhuma operadora encontrada no banco. Importe as operadoras primeiro.")
            return False

        # 2. Processar arquivos por ano e trimestre
        total_imported = 0
        years_to_process = list(range(max(2023, current_year - anos + 1), min(current_year, 2024) + 1))
        
        for year in years_to_process:
            for quarter in ['1T', '2T', '3T', '4T']:
                # Não processar trimestres futuros
                if year == current_year and quarter > f"{(datetime.now().month - 1) // 3 + 1}T":
                    continue
                
                csv_filename = f"{quarter}{year}.csv"
                csv_path = f"dados_ans/{csv_filename}"
                
                # Baixar arquivo se não existir
                if not os.path.exists(csv_path):
                    zip_filename = f"{quarter}{year}.zip"
                    url = f"{base_url}{year}/{zip_filename}"
                    if not download_file(url, f"dados_ans/{zip_filename}"):
                        continue
                    if not extract_zip(f"dados_ans/{zip_filename}", "dados_ans"):
                        continue
                    os.remove(f"dados_ans/{zip_filename}")
                
                # Processar arquivo CSV
                try:
                    df = pd.read_csv(csv_path, sep=';', encoding='latin1', dtype=str)
                    df.columns = [col.strip().upper() for col in df.columns]
                    
                    # Mapeamento de colunas
                    column_map = {
                        'data': 'DATA',
                        'registro_ans': 'REG_ANS',
                        'conta': 'CD_CONTA_CONTABIL',
                        'descricao': 'DESCRICAO',
                        'valor': 'VL_SALDO_FINAL'
                    }
                    
                    # Verificar colunas
                    missing_cols = [k for k, v in column_map.items() if v not in df.columns]
                    if missing_cols:
                        print(f"Arquivo {csv_filename} não contém colunas: {missing_cols}")
                        continue
                    
                    df = df.rename(columns={v: k for k, v in column_map.items()})
                    
                    # Converter dados
                    df['data'] = pd.to_datetime(df['data'], format='%Y-%m-%d', errors='coerce')
                    df['valor'] = pd.to_numeric(
                        df['valor'].str.replace('.', '').str.replace(',', '.'), 
                        errors='coerce'
                    )
                    df['periodo'] = f"{quarter}{year}"
                    
                    # Filtrar apenas registros válidos e de operadoras existentes
                    df = df[
                        df['registro_ans'].isin(operadoras_existentes) &
                        df['descricao'].str.contains('EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS', case=False, na=False) &
                        df['data'].notna() &
                        df['valor'].notna()
                    ]
                    
                    # Inserir em lotes
                    batch_size = 1000
                    for i in range(0, len(df), batch_size):
                        batch = df.iloc[i:i + batch_size]
                        data_to_insert = batch[['data', 'registro_ans', 'conta', 'descricao', 'valor', 'periodo']].values.tolist()
                        
                        insert_sql = """
                        INSERT INTO demonstracoes_contabeis 
                        (data, registro_ans, conta, descricao, valor, periodo) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            valor = VALUES(valor),
                            descricao = VALUES(descricao)
                        """
                        
                        try:
                            cursor.executemany(insert_sql, data_to_insert)
                            conn.commit()
                            imported = len(data_to_insert)
                            total_imported += imported
                            print(f"Progresso: {min(i + batch_size, len(df))}/{len(df)} registros")
                        except Error as e:
                            conn.rollback()
                            print(f"Erro no lote {i//batch_size + 1}: {str(e)}")
                            continue
                    
                    print(f"Arquivo {csv_filename}: {len(df)} registros importados")
                    
                except Exception as e:
                    conn.rollback()
                    print(f"Erro ao processar {csv_filename}: {str(e)}")
                    continue
        
        print(f"\nTotal de registros importados: {total_imported}")
        return total_imported > 0
        
    except Exception as e:
        conn.rollback()
        print(f"Erro fatal: {str(e)}")
        return False

def run_analytical_queries(conn):
    """Executa as queries analíticas solicitadas com critérios mais flexíveis"""
    try:
        cursor = conn.cursor(dictionary=True)
        
        # 1. Verificar se existem dados nas demonstrações contábeis
        cursor.execute("SELECT COUNT(*) as total FROM demonstracoes_contabeis")
        total_registros = cursor.fetchone()['total']
        
        if total_registros == 0:
            print("\nNenhum dado de demonstrações contábeis encontrado no banco.")
            return False
            
        # 2. Obter o período mais recente com qualquer dado
        cursor.execute("""
        SELECT MAX(data) as max_date, 
               (SELECT periodo FROM demonstracoes_contabeis 
                WHERE data = (SELECT MAX(data) FROM demonstracoes_contabeis) 
                LIMIT 1) as periodo
        FROM demonstracoes_contabeis
        """)
        last_data = cursor.fetchone()
        last_date = last_data['max_date']
        last_period = last_data['periodo']
        
        print(f"\nÚltimo período com dados disponíveis: {last_period} (até {last_date})")
        print(f"Total de registros no banco: {total_registros}")
        
        # 3. Query flexível para o último trimestre - busca por termos relacionados
        query_trimestre = """
        SELECT o.razao_social, 
               SUM(d.valor) AS total_despesas,
               MAX(d.periodo) as periodo
        FROM demonstracoes_contabeis d
        JOIN operadoras o ON d.registro_ans = o.registro_ans
        WHERE (d.descricao LIKE '%EVENTOS%' 
               OR d.descricao LIKE '%SINISTROS%'
               OR d.descricao LIKE '%ASSISTÊNCIA%'
               OR d.descricao LIKE '%SAÚDE%')
        AND d.periodo = %s
        GROUP BY o.razao_social
        ORDER BY total_despesas DESC
        LIMIT 10
        """
        
        cursor.execute(query_trimestre, (last_period,))
        resultados_trimestre = cursor.fetchall()
        
        print("\nTop 10 operadoras com maiores despesas (último período disponível):")
        if resultados_trimestre:
            for i, row in enumerate(resultados_trimestre, 1):
                print(f"{i}. {row['razao_social']}: R$ {row['total_despesas']:,.2f}")
        else:
            # Se não encontrar, mostrar as 10 operadoras com maiores despesas independente da descrição
            cursor.execute("""
            SELECT o.razao_social, 
                   SUM(d.valor) AS total_despesas
            FROM demonstracoes_contabeis d
            JOIN operadoras o ON d.registro_ans = o.registro_ans
            WHERE d.periodo = %s
            GROUP BY o.razao_social
            ORDER BY total_despesas DESC
            LIMIT 10
            """, (last_period,))
            resultados_alternativos = cursor.fetchall()
            
            if resultados_alternativos:
                print("(Considerando todas as despesas do período)")
                for i, row in enumerate(resultados_alternativos, 1):
                    print(f"{i}. {row['razao_social']}: R$ {row['total_despesas']:,.2f}")
            else:
                print("Nenhuma operadora com despesas no período.")
        
        # 4. Query flexível para o último ano - busca por termos relacionados
        query_ano = """
        SELECT o.razao_social, 
        SUM(d.valor) AS total_despesas,
        YEAR(MAX(d.data)) as ano
        FROM demonstracoes_contabeis d
        JOIN operadoras o ON d.registro_ans = o.registro_ans
        WHERE (d.descricao LIKE '%EVENTOS%' 
        OR d.descricao LIKE '%SINISTROS%'
        OR d.descricao LIKE '%ASSISTÊNCIA%'
        OR d.descricao LIKE '%SAÚDE%')
        AND YEAR(d.data) = YEAR(%s)
        GROUP BY o.razao_social
        ORDER BY total_despesas DESC
        LIMIT 10
        """
        
        cursor.execute(query_ano, (last_date,))
        resultados_ano = cursor.fetchall()
        
        print("\nTop 10 operadoras com maiores despesas (último ano disponível):")
        if resultados_ano:
            for i, row in enumerate(resultados_ano, 1):
                print(f"{i}. {row['razao_social']}: R$ {row['total_despesas']:,.2f}")
        else:
            # Se não encontrar, mostrar as 10 operadoras com maiores despesas no ano
            cursor.execute("""
            SELECT o.razao_social, 
            SUM(d.valor) AS total_despesas
            FROM demonstracoes_contabeis d
            JOIN operadoras o ON d.registro_ans = o.registro_ans
            WHERE YEAR(d.data) = YEAR(%s)
            GROUP BY o.razao_social
            ORDER BY total_despesas DESC
            LIMIT 10
            """, (last_date,))
            resultados_alternativos = cursor.fetchall()
            
            if resultados_alternativos:
                print("(Considerando todas as despesas do ano)")
                for i, row in enumerate(resultados_alternativos, 1):
                    print(f"{i}. {row['razao_social']}: R$ {row['total_despesas']:,.2f}")
            else:
                print("Nenhuma operadora com despesas no ano.")
        
        return True
        
    except Error as e:
        print(f"\nErro ao executar queries analíticas: {e}")
        return False

def main():
    # Criar pasta de dados se não existir
    os.makedirs("dados_ans", exist_ok=True)
    
    # Conectar ao banco de dados
    conn = create_db_connection()
    if not conn:
        return
    
    try:
        # Criar/verificar tabelas no banco de dados
        if not setup_database_tables(conn):
            return
        
        # Importar dados das operadoras
        print("\nImportando dados das operadoras...")
        if not import_operadoras(conn):
            return
        
        # Importar dados das demonstrações contábeis
        print("\nImportando demonstrações contábeis...")
        if not import_demonstracoes(conn, anos=2):
            return
        
        # Executar queries analíticas
        print("\nExecutando queries analíticas...")
        if not run_analytical_queries(conn):
            return
        
        print("\nProcesso concluído com sucesso!")
        
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()