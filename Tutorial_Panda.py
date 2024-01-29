import pandas as pd
import numpy as np


#carregando dados
fifa19 = pd.read_csv('FIFA19.csv', sep=',', skiprows=None)
# fifa19.head() #começo das linahs
# fifa19.tail() # ultimas linhas

#-------------------  excel
# x1 = pd.excelFile(file) #carrega o arquivo
#df = x1.parse('sheet_1') #carrega a aba
#OBS: Para ajudar na definição dos tipos e otimizar
# pd.read_csv('FIFA19.csv', dtype={"Potencial":"int", "SlidingTackle":"float64"})

#INFORMAÇÕES sobre o dataset
fifa19.info() #--> confirmar tipos para cada coluna
# ----------------------------

#Manipular as colunas e linhas
# fifa19.shape
# fifa19.shape[0]
# fifa19.shape[1]
print("Temos %0.f linhas e %0.f colunas" % (fifa19.shape[0], fifa19.shape[1]))
print(f"Temos {fifa19.shape[0]:.0f} linhas e {fifa19.shape[1]:.0f} colunas")

#coluna
fifa19.columns
#obs: funciona como lista
fifa19.columns[1]
#indice
fifa19.index
#Se quiser estabelecer uma coluna como indice é só usar set_index, por exemplo:
#df.set_index('nome da coluna')#para uma coluna
#df.set_index(['nome da coluna 1', 'nome da coluna 2', ...., 'nome da coluna n'])# para varias colunas

#Mudar a largura da coluna, aumentar numero de linhas, nmero de colunas
pd.set_option('display.max_colwidth', 10)
pd.set_option('display.max_rows', 20)
#pd.set_option('display.max_columns', 60) #sabe-se que tem 89

#print(pd.get_option('max_colwidth')) 
#print(fifa19.head(50))

def low_values_red(value):
    color = 'red' if value < 92 else 'black'
    return f'Color: {color}' #color: red ou color: black

#applymap aplica em todo o dataset a funcao feita
fifa19[['Overall', 'Potential']].head(10).style.applymap(low_values_red)
#aplicar em todos os elementos, mas para ser somente em over e potencial
fifa19.head(10).style.applymap(low_values_red, subset=['Overall', 'Potential'])
 
# checa esse booleano e depois guarda em is_max s==s.max (verificando se o valor é o maior de toda coluna)
def highlight_max(s):
    is_max = s == s.max() 
    return ['background-color: yellow' if v else '' for v in is_max]
#apply ele vai em toda coluna!
fifa19.head(10).style.apply(highlight_max, subset=['Age', 'Overall', 'Potential'])

#ambas funcoes
fifa19[['Overall', 'Potential']].head(10).style.applymap(low_values_red).apply(highlight_max)

#formatação: pandas.pydata.org/pandas-docs/stable/user_guide/style.html

# ---------------  criterios / Filtros e Selecoes ----------------------- #
#loc nome da coluna e iloc o posicao --> o final conta como n-1
fifa19.loc[0:5, 'Age']
fifa19.iloc[0:5, 1:4]


fifa19.loc[(fifa19['Age'] > 30) & (fifa19['Overall'] >= 90)]
filtered_players = fifa19.loc[(fifa19['Age'] > 30) & (fifa19['Overall'] >= 90)]

# Query filtra baseada em uma função logica --> expressao booleana 
orlder_fifa_players = fifa19.query('Age > 30')
orlder_fifa_players.head()
# Vai trazer todas as linhas que se o booleano for True
fifa19[fifa19['Age']>30]

# Filtro comparativo
fifa19[fifa19['GKDiving']==fifa19['GKHandling']]

# Filtro
fifa19.filter(['Age', 'ID', 'Name'])

overall_median = fifa19['Overall'].median() #mediana
fifa19.query("Overall > @overall_median")

# Is in --> esta na coluna
df_champs = fifa19[fifa19['Nationality'].isin(['Argentina', 'Brazil', 'Germany', 'Italy', 'England'])]
df_champs.head()

df_non_champs = fifa19[~fifa19['Nationality'].isin(['Argentina', 'Brazil', 'Germany', 'Italy', 'England'])]
df_non_champs.head()

# Só ter numeros e não ter numeros
numerics = ['int16', 'int32', 'int64', 'float16','float32','float64']
fifa19_numerics = fifa19.select_dtypes(include= numerics)
fifa19_numerics.head()

numerics = ['int16', 'int32', 'int64', 'float16','float32','float64']
fifa19_non_numerics = fifa19.select_dtypes(exclude= numerics)
fifa19_non_numerics.head()

# 10 melhores jogadores baseado no overall
fifa19.sort_values(by='Overall',ascending=False).head(10)

#Remover duplicidade
fifa19.drop_duplicates()

# ---------------------- 4 ESTATISTICA DESCRITIVA ---------------------- #

fifa19.describe() # descreve alguns valores gerais

fifa19['Age'].describe(percentiles=[0.1, 0.2, 0.8, 0.99]) #mais percentis

#ps: como dicionario
fifa19.agg({'Age':['min','max','skew','median'],
           'Overall':['mean','min']})

# -------------- fazer Agrupamentos
df_champs.groupby('Nationality')[['Age','Overall']].mean()
#ordenar do maior para o menor
df_champs.groupby('Nationality')[['Age','Overall']].mean().sort_values(by='Overall', ascending=False)

#pd.pivot_table(df_champs, index=['Nationality'], aggfunc=np.mean)
# -   tabela dinaminca
pd.pivot_table(df_champs, index=['Nationality'], values=['Age', 'Overall','Strength'], aggfunc=np.mean)

#saber a idade., overall e forca media dos jogadores por posição e por nacionalidade
pd.pivot_table(df_champs, index=['Nationality'],columns=['Position'] ,values=['Age', 'Overall','Strength'], aggfunc=np.mean)

# Variaveis categoricas 
# quantos jogadores por pais, qual percentual desses jogadores são de um pais.
df_champs.Nationality.value_counts()
#porcentagem
df_champs.Nationality.value_counts(normalize=True)

df_champs.groupby(['Club'])['Nationality'].value_counts()
# contagem por mais de um agrupamento
df_champs.groupby(['Nationality'])['Position'].value_counts()

# ----------------------------  SQL no PANDAS
# melhorar desempenho

# # import modin.pandas as pd
# # import pandas.sql as ps

# # atribuir a um objeto a querry que voce quer
# query = """"
# select ID, Age, Name from fifa19 where Age > 33 """
# #rodar de forma local
# ps.sqldf(query, locals())
