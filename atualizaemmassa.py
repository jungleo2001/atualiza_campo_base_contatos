import logging
import time
import requests
import pandas as pd

logging.basicConfig(level=logging.DEBUG, filename='AlteraContatoEmMassa.log', format="%(asctime)s - %(levelname)s - %(message)s", encoding='utf-8')

bx24_url = 'https://b24-1d16v2.bitrix24.com.br/rest/1/62xthupgjs8gakl7/crm.contact.update'  ##MUDA EU, BOTA TEU WEBHOOK AI JOVEM, MAS DEIXA O #METODO

# Lendo o arquivo Excel

#ARQUIVO COM OS CONTATOS QUE TU QUER ATUALIZAR,
#EXPORTADO DO AMBIENTE BITRIX.

negocios = pd.read_excel(r"/home/leonardo/Downloads/CONTACT_20241210_3273b259_6758a1561a4dc.xlsx")

# negocios.dropna(axis=0, inplace=True)
print(negocios)  # Você pode substituir esta linha por display(negocios) se estiver usando um Jupyter Notebook

for i, row in negocios.iterrows():
    print(row['ID'])
    IdContato = row['ID']
    telefone = row['Telefone de trabalho']
    telefone_com_prefixo = f'+55{telefone}'

    payload = {
        'id': IdContato,
        'fields': {
            'PHONE': [
                {
                    'VALUE': telefone_com_prefixo,
                    'VALUE_TYPE': 'MOBILE'
                }
            ]
        }
    }

    response = requests.post(bx24_url, json=payload)
    logging.info(response.json())
    time.sleep(0.5)  # Pausa de 0,5 segundos entre cada requisição para alcançar a taxa de 2 requisições por segundo

    if i % 250 == 0 and i != 0:
        logging.debug("Pausa 1h")
        time.sleep(3600)

logging.info("Terminou")
