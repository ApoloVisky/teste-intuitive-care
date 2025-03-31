import json
import boto3
import csv
from io import StringIO
import logging

# Configuração de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        BUCKET_NAME = 'testeintuitivebucket300320252058'
        FILE_KEY = 'Relatorio_cadop.csv'
        search_term = event.get('queryStringParameters', {}).get('q', '').lower()
        
        # Baixar arquivo CSV do S3
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
        csv_data = response['Body'].read().decode('utf-8')
        
        reader = csv.DictReader(StringIO(csv_data), delimiter=';')
        fieldnames = reader.fieldnames
        rows = list(reader)
        
        results = []
        for row in rows:
            if not search_term:  
                results.append(row)
                continue
                
            for value in row.values():
                if isinstance(value, str) and search_term in value.lower():
                    results.append(row)
                    break
        
        # Limitar a 50 resultados
        results = results[:50]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'count': len(results),
                'results': results
            }, ensure_ascii=False)
        }
        
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }