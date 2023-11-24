import pandas as pd
import os

from sklearn.feature_extraction.text import TfidfVectorizer #ajuda o modelo a entender e manipular texto, transformando eles em vetores de numeros
from sklearn.linear_model import LogisticRegression #treinar o modelo para entender padrões
from sklearn.model_selection import train_test_split #separar arrays em dados de treinamento e dados de teste

links = pd.read_csv('malicious_phish.csv')

#Limpando nosso dataset por barra, hífen e ponto, tirando caracteres desnecessários
def makeTokens(f): #fazendo tokens depois de separar por barra
    tkn_porBarra=str(f.encode('utf-8')).split('/') 
    total_Tokens = []
    
    for i in tkn_porBarra: #separando por hífen
        tokens = str(i).split('-') 
        tkn_PorPonto = []
    
        for j in range(0,len(tokens)): #separando por ponto
            temp_Tokens = str(tokens[j]).split('.') 
            tkn_PorPonto = tkn_PorPonto+temp_Tokens
        total_Tokens = total_Tokens + tokens + tkn_PorPonto #removendo tokens reduntantes pois sets não podem ter 2 elementos iguais
    total_Tokens = list(set(total_Tokens))
        
    if 'com' in total_Tokens: #removendo os ".com" existentes
        total_Tokens.remove('com') 
        
    return total_Tokens
    
#separando as colunas do csv
lista_links = links['url']
y = links['label']

#convertendo o texto em vetores e usando o "makeTokens" para limpar os textos
vectorizer = TfidfVectorizer(tokenizer=makeTokens)
X = vectorizer.fit_transform(lista_links)

#separando os datasets. Treino e teste
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
#O parametro "test_size=0.2" diz que 80% do dataset vai ser usado pra treino e os 20% restantes vão ser usado para teste
logit = LogisticRegression(max_iter=40000)
logit.fit(X_train, y_train)

os.system('cls')
Previsao_X = []
print('Modelo de url: https://exemplourl.com.br/')
while True:
    input_usuario = input("Digite sua(s) URL(s) ou 'sair' pra sair:")
    if input_usuario.lower() == 'sair':
        break
    if input_usuario.strip():  # strip() remove espaços em branco antes e depois da string
        Previsao_X.append(input_usuario)

Previsao_X = vectorizer.transform(Previsao_X)
Nova_previsao = logit.predict(Previsao_X)
print(Nova_previsao)