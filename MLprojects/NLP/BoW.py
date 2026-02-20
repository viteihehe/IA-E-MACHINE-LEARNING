import random as r
import math as m

dados = []
total_documentos = 0
with open('/home/vitim/Desktop/Untitled Folder 2/IA-E-MACHINE-LEARNING/MLprojects/NLP/emails.txt', 'r', encoding='utf-8') as file:
   for linha in file:
       total_documentos += 1
       partes = linha.lower().split(maxsplit=1)
       if len(partes) == 2:
           dados.append(partes)

r.shuffle(dados)

tam_treino = (total_documentos*70)/100
tam_treino = int(tam_treino)
tam_teste = total_documentos-tam_treino
tam_teste = int(tam_teste)



def organizador(dados):
    treino = dados[:tam_treino]
    teste = dados[tam_treino:]
    
    X_train = []
    y_train = []
    X_test = []
    y_test = []
    
    for i in treino:
        X_train.append(i[1])
        y_train.append(i[0])
    
    for j in teste:
        X_test.append(j[1])
        y_test.append(j[0])
        
    return X_train, y_train, X_test, y_test


def contador(y_train):
    spam = 0
    nspam = 0
    for i in y_train:
        if i == "spam":
            spam += 1
        elif i == "nao_spam":
            nspam += 1
            
    return spam, nspam
    
vocabulario = []

def tokenizador(entrada):
    dicionario = {}
    temp = []
    for i in entrada:
        palavra = i.lower().split()
        for p in palavra:
            if p not in vocabulario:
                vocabulario.append(p)
        temp.extend(palavra)
    
    for i in temp:
        dicionario[i] = dicionario.get(i, 0)+1

    return dicionario

def separador(X, y):
    x_spam = []
    x_nspam = []
    
    for i in range(tam_treino):
        if y[i] == "spam":
            x_spam.append(X[i])
        elif y[i] == "nao_spam":
            x_nspam.append(X[i])
    
    dict_spam = tokenizador(x_spam)
    dict_nspam = tokenizador(x_nspam)
    
    return dict_spam, dict_nspam
    

def treinamento(dicionario_spam, dicionario_nspam, y_train):
    
    tamanho_dic_spam = sum(dicionario_spam.values())
    tamanho_dic_nspam = sum(dicionario_nspam.values())
    
    total_spam, total_nspam = contador(y_train)
    p_spam = total_spam/len(y_train)
    p_nspam = total_nspam/len(y_train)
    
    pw_spam = {}
    pw_nspam = {}
    
    tamanho_vocabulario = len(vocabulario)
    
    for i in vocabulario:

        cont = dicionario_spam.get(i, 0)
        pw_spam[i] = (cont + 1)/(tamanho_dic_spam+tamanho_vocabulario)
    
        cont2 = dicionario_nspam.get(i, 0)
        pw_nspam[i] = (cont2 + 1)/(tamanho_dic_nspam+tamanho_vocabulario)
        
    return p_spam, p_nspam, pw_spam, pw_nspam
    
def score(p_spam, p_nspam, pw_spam, pw_nspam, lista_X, y_test ,dic_spam, dic_nspam):
    resultados_finais = []
    
    
    tamanho_dic_spam = sum(dic_spam.values())
    tamanho_dic_nspam = sum(dic_nspam.values())
    tamanho_vocabulario = len(vocabulario)
    prob_base_s = m.log(1 / (tamanho_dic_spam + tamanho_vocabulario))
    prob_base_n = m.log(1 / (tamanho_dic_nspam + tamanho_vocabulario))

    for frase in lista_X:
        score_spam = m.log(p_spam)
        score_nspam = m.log(p_nspam)
        
        palavras = frase.lower().split()
        contagem_frase = {}
        
        for p in palavras:
            contagem_frase[p] = contagem_frase.get(p, 0) + 1
            
        for palavra, frequencia in contagem_frase.items():
            
            if palavra in pw_spam:
                score_spam += frequencia * m.log(pw_spam[palavra])
            else:
                score_spam += frequencia * prob_base_s
            
            if palavra in pw_nspam:
                score_nspam += frequencia * m.log(pw_nspam[palavra])
            else:
                score_nspam += frequencia * prob_base_n
        
        if score_spam > score_nspam:
            resultados_finais.append(1)
        else:
            resultados_finais.append(0)
            
    acertos = 0
    for i in range(len(y_test)):
        if resultados_finais[i] == 1 and y_test[i] == "spam":
            acertos += 1
        elif resultados_finais[i] == 0 and y_test[i] == "nao_spam":
            acertos += 1
        
    acuracia = (acertos/len(y_test))*100
            
    return resultados_finais, acuracia
    
def main():
   X_train, y_train, X_test, y_test = organizador(dados)
   dict_spam, dict_nspam = separador(X_train, y_train)
   p_spam, p_nspam, pw_spam, pw_nspam = treinamento(dict_spam, dict_nspam, y_train)
   resultado, acuracia = score(p_spam, p_nspam, pw_spam, pw_nspam, X_test, y_test, dict_spam, dict_nspam)
   print(f"Acurácia final: {acuracia:.2f}")

   for i in range(3):
        if resultado[i] == 1:
           print(f"Exemplo {i} é: SPAM")
        elif resultado[i] == 0:
            print(f"Exemplo {i} não é spam")
            
        print(f"Resultado real: {y_test[i]}")

        

    
main()
   
    