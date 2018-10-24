import requests
import re
import datetime
import csv
import sys
import boto3
from slackclient import SlackClient

header = {'user-agent':'Mozilla/5.0'}
try:
    r = requests.get('https://m.investing.com/currencies/usd-brl', headers= header)
    r2 = requests.get('https://m.investing.com/currencies/eur-brl', headers= header)
except ValueError:
    print('Serviço de request indisponível.')
match = re.search('(lastInst)', r.text)
date = datetime.datetime.now()
def dolar():
    if (match):
        p1 = r.text.find('lastInst')
        p2 = r.text.find('quotesChange')
        pf = r.text[p1:p2]
        x1 = pf.find('>')
        x2 = pf.find('</')
        xf = pf[x1 + 1:x2]
        dolar = xf.strip()
        print('Dolar: ' + dolar)
        print(date)
        with open(r'cotacao.csv', 'a') as data:
            writer = csv.writer(data)
            writer.writerow(['USD/BRL', dolar, date])
    else:
        print('Não foi encontrado')

def euro():
    if (match):
            p1 = r2.text.find('lastInst')
            p2 = r2.text.find('quotesChange')
            pf = r2.text[p1:p2]
            x1 = pf.find('>')
            x2 = pf.find('</')
            xf = pf[x1+1:x2]
            euro = xf.strip()
            print('Euro: ' + euro)
            print(date)
            with open(r'cotacao.csv', 'a') as data:
                writer = csv.writer(data)
                writer.writerow(['EUR/BRL', euro, date])
    else:
            print('Não foi encontrado')
def log(data, x = 0):
    arq = open("log" + date.strftime("%Y-%m-%d %H-%M-%S") + ".txt", "w")
    arq.write("HORÁRIO DE EXECUÇÃO: " + str(date))
    arq.write("\n")
    if x == 'euro':
        arq.write("AÇÃO REALIZADA: Cotação do euro")
        arq.write("\n")
    else:
        arq.write("AÇÃO REALIZADA: Cotação do dolar")
        arq.write("\n")
    arq.write("TEMPO FINAL: " + str(data))
    arq.write("\n")
    duracao = (data - date)
    arq.write("DURAÇÃO: " + str(duracao.total_seconds()))

def boto():
    session = boto3.Session(
        aws_access_key_id='AKIAJIVVRKW4LRWAZI5A',
        aws_secret_access_key='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',
    )
    s3 = session.resource('s3')
    s3.upload_file('cotacao.csv', 'Bucket', 'cotacao.csv')

def slack():
    token = 'xoxb-406592957301-446000490982-9gtTksnLHRmGO3naumTfZXzu'
    slack_client = SlackClient(token)
    slack_client.api_call("chat.postMessage", channel="general", text="Foi feito o upload do arquivo cotacao.csv")

if __name__ == "__main__":
    if sys.argv[1:] == ['1']:
        dolar()
        data = datetime.datetime.now()
        log(data)
    elif sys.argv[1:] == ['2']:
        x= 'euro'
        euro()
        data = datetime.datetime.now()
        log(data,x)
    elif sys.argv[1:] == ['60']:
        boto()
        slack()
    else:
        print('Digite 1 para cotação do dolar.\nDigite 2 para cotação do euro.')
