import os, time
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def init_db():
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    init_db()
    
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
def getDados():
    init_db()
    
    return json.loads(open("base.atitus", "r").read())