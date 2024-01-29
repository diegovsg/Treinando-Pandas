import pandas as pd
import numpy as np

#MISSING e Alterações/Criações de campos

#carregando dados
fifa19 = pd.read_csv('FIFA19.csv', sep=',', skiprows=None)

print(fifa19.columns)

df_null = fifa19[['Name','Wage','Joined']].head(10)
df_null

#Retorna  verd ou false se for nulo ou nao
df_null.isna()

# df_null.isna().sum
df_null.info()

#filtrar linhas com campo missings
df_null[pd.isna(df_null['Joined'])]

#filtra quem não tem nada faltando
df_null[df_null['Joined'].notna()]

#preencher
df_null.fillna('0')

#se estivesse numerico, preecher com media:
#df_null.fillna(df_null.mean(), implace=True)

# para cada coluna ser substituido por um valor no lugar no missing, se não por implacce não é substituido
# values = {'wage': 0, 'wage':'10000'}

fifa19['Weight'].head()
fifa19["Weight"].fillna('0lbs', inplace=True)

def substitui_lbs(value):
    x = value.replace('lbs', '')
    return int(x)

fifa19['Weight_new'] = fifa19['Weight'].apply(substitui_lbs)
fifa19.head()
fifa19[['Weight_new']].info()

# Convertendo campo salario
def converte_wage(value):
    value_2 = value.replace('€','')
    if 'M' in value_2:
        value_2 = value_2.replace('M','')
        return float(value_2)*1000000
    elif 'K' in value_2:
        value_2 = value_2.replace('K','')
        return float(value_2)*1000

fifa19['Wage_Numeric'] = fifa19['Wage'].apply(converte_wage)
fifa19.head()

#media gk
fifa19['avg_GK'] = (fifa19['GKDiving']+fifa19['GKHandling']+fifa19['GKKicking']+fifa19['GKPositioning']+fifa19['GKReflexes'])/5
fifa19.head()

# Cria um campo condicional a outro
fifa19['Age_Class'] = np.where(fifa19['Age']>30, 'Old', 'Young') # import numpy as np
fifa19.head()

fifa19['Age_Class2'] = 'Young'
fifa19.loc[fifa19['Age']>30, 'Age_Class2'] = 'Old'
fifa19.head()

