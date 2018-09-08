# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 22:32:55 2018

@author: Gaston Guillaux
"""

def ultimo_sorteio(loteria: str):
    return create_database(loteria).tail(1)


def create_database(loteria):
    import pandas as pd
    import os
    
    #DECLARACAO DE VARIAVEIS
    path = r'C:\temp\auxpy'
    file_lotomania = r'D_LOTMAN.HTM'
    file_lotofacil = r'D_LOTFAC.HTM'
    
    if loteria == 'lotomania':
        #LOTOMANIA
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotoma.zip'
        download_and_unzip(path,url)
        #download_lotomania_historic()
        dados_historicos = pd.read_html(os.path.join(path, file_lotomania))[0]
        #print(dados_historicos)
        clean_aux_dir()
        #return dados_historicos
        
    elif loteria == 'lotofacil':
        #LOTOFACIL
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'
        download_and_unzip(path,url)
        #download_lotofacil_historic()
        dados_historicos = pd.read_html(os.path.join(path, file_lotofacil))[0]
        #print(dados_historicos)
        clean_aux_dir()
        #return dados_historicos
    
    #NOMEIA AS COLUNAS COM OS DADOS DA PRIMEIRA LINHA
    dados_historicos.columns =  dados_historicos.loc[0]
    
    #REMOVE A PRIMEIRA LINHA QUE TEM OS NOMES DAS COLUNAS
    aux_df = dados_historicos.drop(index=0)
    
    #REMOVE TODAS AS LINHAS QUE TENHAM MAIS DE 10 VALORES NAN
    aux_df = aux_df.dropna(thresh=10)
    
    aux_df = aux_df.replace('.', '')
    
    dados_historicos = aux_df.reset_index(drop=True)
    dados_historicos = dados_historicos.set_index('Concurso')
    
    return dados_historicos

'''
==========================================================================================
'''

def computa_numeros_sorteados(loteria):
    import pandas as pd
    
    #DEFINE COLUNAS QUE SERAO BUSCADAS NO DATAFRAME
    if loteria == 'lotomania':
        dezenas = 20
    elif loteria == 'lotofacil':
        dezenas = 15
    
    #OBTEM DATAFRAME COM TODOS OS SORTEIOS DE UMA LOTERIA
    df = create_database(loteria)
    
    #DICIONARIO QUE SERA USADO PARA COMPUTAR AS REPETICOES DE NUMEROS
    numeros = {}
    
    #ITERA POR TODAS AS LINHAS COM TODOS OS SORTEIOS
    for row in df.iterrows():
        #ITERA SOMENTE PELAS COLUNAS COM AS DEZENAS
        for n in range(dezenas):
            num = row[1]['Bola' + str(n+1)]
            #CASO O NUMERO NAO EXISTA NO DICIONARIO, COLOCA-O NO DICIONARIO
            if num not in numeros:
                numeros[num] = 1
            #CASO CONTRARIO, O INCREMENTA
            else:
                numeros[num] += 1
    
    #TRANSFORMA NUMA SERIE O DICIONARIO COM NUMEROS SORTEADOS
    numeros = pd.Series(numeros)
    
    #RETORNA A SERIE
    return numeros

'''
==========================================================================================
'''

#BAIXA E EXTRAI ARQUIVO ZIP COM OS DADOS HISTORICOS
def download_and_unzip(path, url):
    import zipfile
    import requests
    import io
    r = requests.get(url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)
    z.close()    
        
'''
==========================================================================================
'''    

#LIMPA DIRETORIO AUXILIAR USADO PARA BAIXAR OS ARQUIVOS    
def clean_aux_dir():
    import shutil as sh
    import os
    path = r'C:\temp\auxpy'
    sh.rmtree(path)
    os.mkdir(path)
