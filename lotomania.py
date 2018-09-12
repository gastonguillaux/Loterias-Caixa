# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 22:32:55 2018

@author: Gaston Guillaux
"""

def ultimo_sorteio(loteria: str):
    if loteria == 'lotomania':
        bolas = '20'
    elif loteria == 'lotofacil':
        bolas = '15'
    
    return create_database(loteria).tail(1).loc[:, 'Bola1':'Bola'+bolas]

'''
==========================================================================================
'''

def todos_sorteios(loteria: str):
    if loteria == 'lotomania':
        bolas = '20'
    elif loteria == 'lotofacil':
        bolas = '15'
    
    return create_database(loteria).loc[:, 'Bola1':'Bola' + bolas]

'''
==========================================================================================
'''

def valida_apostas_lotofacil_ultimo():
    df_apostas = importa_apostas()
    ult_sorteio = [int(i) for i in ultimo_sorteio('lotofacil').values.tolist()[0]]
    #ult_sorteio = [int(i) for i in ['01','02','03','04','06','07','08','09','10','12','13','14','17','18','22']]

    apostas = {}
    #CRIA DICIONARIO ESTRUTURADO PARA AS APOSTAS
    for index, row in df_apostas.iterrows():
        apostas[index] = {}
        apostas[index]['numeros'] = [int(j) for j in row.values.tolist()]
        apostas[index]['acertos'] = 0
    
    #VALIDA CADA APOSTA CONTRA O RESULTADO DO ULTIMO SORTEIO    
    for aposta in apostas:
        for numero in apostas[aposta]['numeros']:
            if int(numero) in ult_sorteio:
                apostas[aposta]['acertos'] += 1
    
    #IMPRIME O SCORE
    print('### ACERTOS DE CADA APOSTA ###')
    for aposta in apostas:
        print(aposta + ' = ' + str(apostas[aposta]['acertos']))
    return apostas

'''
==========================================================================================
'''   

def valida_apostas_lotofacil(ultimos_jogos=1, score=11):
    #IMPORTA DE ARQUIVO FISICO
    #df_apostas = importa_apostas()
    #arquivo_fisico = True
    
    #SIMULA COM APOSTAS RANDOMICAS
    df_apostas = gera_apostas('lotofacil', 15000)
    arquivo_fisico = False
    
    sorteios = {} 
    ult_n_sorteios = create_database('lotofacil').tail(ultimos_jogos).loc[:, 'Bola1':'Bola15']
    apostas = {}
        
    for index, row in ult_n_sorteios.iterrows():
        sorteios[index] = [int(j) for j in row.values.tolist()]
    
    if arquivo_fisico == True:
        for index, row in df_apostas.iterrows():
            apostas[index] = {}
            apostas[index]['numeros'] = [int(j) for j in row.values.tolist()]
            apostas[index]['acertos'] = 0
            apostas[index]['sucesso'] = {11:0, 12:0, 13:0, 14:0, 15:0}
    elif arquivo_fisico == False:
        apostas = df_apostas
        for index in df_apostas:
            apostas[index]['acertos'] = 0
            apostas[index]['sucesso'] = {11:0, 12:0, 13:0, 14:0, 15:0}
        
    for sorteio in sorteios:
        s = sorteios[sorteio]
        for aposta in apostas:
            for numero in apostas[aposta]['numeros']:
                if numero in s:
                    apostas[aposta]['acertos'] += 1

        '''
        #MOSTRA EM QUAIS CONCURSOS TERIAMOS >= 11 ACERTOS            
        for aposta in apostas:
            if apostas[aposta]['acertos'] >= score:
                print('### ACERTOS DO SORTEIO ' + sorteio + ' ###')    
                print(aposta + ' = ' + str(apostas[aposta]['acertos']))
                print('*' * 30)
            apostas[aposta]['acertos'] = 0     
        '''
        for aposta in apostas:
            if apostas[aposta]['acertos'] >= 11:
                apostas[aposta]['sucesso'][apostas[aposta]['acertos']] += 1
            apostas[aposta]['acertos'] = 0
    
    return apostas
 

'''
==========================================================================================
'''    

def importa_apostas():
    import pandas as pd
    p = r'c:\temp\apostas.csv'
    apostas = pd.read_csv(p, index_col=0)
    return apostas

'''
==========================================================================================
'''

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
        dados_historicos = pd.read_html(os.path.join(path, file_lotomania))[0]
        #print(dados_historicos)
        clean_aux_dir()
        
    elif loteria == 'lotofacil':
        #LOTOFACIL
        url = 'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip'
        download_and_unzip(path,url)
        dados_historicos = pd.read_html(os.path.join(path, file_lotofacil))[0]
        #print(dados_historicos)
        clean_aux_dir()
    
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
def gera_apostas(loteria, n_apostas=1):
    import statistics as s
    import random as r
    n = 1
    
    if loteria == 'lotomania':
        universo = 100
        dezenas = 50
        var_min = 730
        var_max = 860
        std_min = 27
        std_max = 30
        ini = 0
    elif loteria == 'lotofacil':
        universo = 26
        dezenas = 15
        var_min = 48
        var_max = 55
        std_min = 7
        std_max = 8
        ini = 1
    apostas = {}
    
    while len(apostas) < n_apostas:
        aux = r.sample(range(ini,universo), k=dezenas)
        aux.sort()
        if s.variance(aux) >= var_min and s.variance(aux) <= var_max:
            if s.stdev(aux) >= std_min and s.stdev(aux) <= std_max:
                apostas['Aposta' + str(n)] = {}
                apostas['Aposta' + str(n)]['numeros'] = aux
                n += 1
    return apostas
    
    
    



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
