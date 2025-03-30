import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile



url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'


output = 'downloads'
os.makedirs(output, exist_ok=True)


# Fazer a requisição à página
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.content, 'html.parser')

pdf_links = []
for link in soup.find_all('a', href=True):
    href = link['href']
    if 'Anexo I' in link.text or 'Anexo II' in link.text:
        full_url = href if href.startswith('http') else f'https://www.gov.br{href}'
        pdf_links.append((link.text.strip(), full_url))


for title, link in pdf_links:
    filename = os.path.join(output, f"{title}.pdf")
    pdf_response = requests.get(link)
    pdf_response.raise_for_status()

    with open(filename, 'wb') as pdf_file:
        pdf_file.write(pdf_response.content)
    print(f'Download concluído: {filename}')


zip_filename = 'anexos.zip'

with ZipFile(zip_filename, 'w') as zipf:
    for title, _ in pdf_links:
        pdf_path = os.path.join(output, f"{title}.pdf")
        zipf.write(pdf_path, os.path.basename(pdf_path))
        print(f'Arquivo adicionado ao ZIP: {pdf_path}')

print(f'Arquivo ZIP criado: {zip_filename}')
