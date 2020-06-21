#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 13:48:39 2020

Comparação do número de mortos pelo COVID19 em Maio de 2020 no Brasil em relação
às estatísticas de mortos de 2008 a 2018 por outras causas.

Fonte COVID19 no Brasil: https://www.comitecientifico-ne.com.br/c4ne
Fonte outras mortes: DATASUS http://svs.aids.gov.br/dantps/centrais-de-conteudos/paineis-de-monitoramento/mortalidade/cid10/
@author: renan de jesus melo

Bibliotecas necessárias para execução:
    Python 3.0   (ou superior compatível)
    Pandas      (http://pandas.pydata.org)
    Matplotlib  (https://matplotlib.org/)
    Seaborn     (http://seaborn.pydata.org)

Licenças de uso:
    Código fonte: GPL 3.0
    Gráficos gerados: Creative Commons CC-BY-SA 4.0
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#período de abrangência dos dados do DATASUS 2008 a 2018 (inclusive)
periodo = range(2008,2019)

anos = {i:i for i in periodo}

#ponteiro dos arquivos em forma de dicionário por ano
arquivos = {k:'./dados/mortes'+str(v)+'.csv' for (k,v) in anos.items()}

#colunas úteis para nossa analise: ano, mortes em maio
cols=[1,28]
#importa os arquivos como Pandas.DataFrame organizandos-os em um dicionário por ano
#usei argumentos opcionais para lidar com separador ';', símbolo de milhar '.', ignorar colunas desnecessárias
dados = {k:pd.read_csv(v,sep=';',decimal=',',thousands='.', usecols=cols) for (k,v) in arquivos.items()}

#reescrevendo as categorias da coluna "indicador (nome)" para facilitar a exibição dos gráficos
categorias =  ['infeciosas','tumores','órgãos hematopoéticos','metabólicas'] 
categorias += ['transtornos mentais','sist. nervoso','olho e anexos','ouvidos e apófise mastóide']
categorias += ['ap. circulatório','ap. respiratório','ap. digestivo','da pele e subcutânea','osteomuscular']
categorias += ['ap. geniturinário','gravidez/parto','período perinatal','malformações congênitas','não classificados']
categorias += ['lesões e envenenamento','causas externas','contato com o serviço de saúde','códigos especiais']


for k,v in dados.items():
    # remove a linha de totais
    v.drop(v.index[0],inplace=True)
    #adiciona uma coluna com as categorias
    v['categorias'] = [x.upper() for x in categorias]
    
#agrupa esses dados num único DataFrame   
estatistica_maio=pd.concat(dados.values())

#mortos pelo COVID19 no Brasil em 2020-05 segundo CONSORCIO-NORDESTE
#total de óbitos: (2020-04-30 foi 5980) e (2020-05-31 foi 29367)
covidmaio=29367-5980

#acrescentando esses dados ao estatisticas_maio
covid19=pd.DataFrame([[2020,covidmaio,'COVID19']],columns=estatistica_maio.columns)
estatistica_maio=pd.concat([estatistica_maio,covid19])

#Desenhando o gráfico
f,ax = plt.subplots(figsize=(6,8))
f.suptitle('COVID: comparação com os óbitos de Maio entre 2008 e 2018',fontsize=16,weight='bold',x=0.35,y=0.93)
# ax.set_xscale('log')
sns.set_context('paper')
sns.set_style('whitegrid')
ax = sns.boxplot(y='categorias',x='Maio',data=estatistica_maio, linewidth=2)
ax.set_xlabel('')
ax.set_ylabel('Classificação (rótulo simplificado)')
# ax.set_title('Brasil: mortes em Maio segundo DATASUS (2008-2018)',weight='bold',size='x-large')



