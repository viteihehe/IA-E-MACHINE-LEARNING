import random as r
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
import math as m
from sklearn.model_selection import train_test_split
import numpy as np
from abc import ABC, abstractmethod

#Carregando DataSet
dados = load_digits()

#Formula utilizada para ativação não linear
def tanh(pu):
    x = ((m.exp(pu) - m.exp(-pu))/(m.exp(pu) + m.exp(-pu)))
    return x

#Tranformando o Target (valor escalar) para um vetor
def normalizacao_target(valor):
    retorno = []
    for i in range(10):
        if i != valor:
            retorno.append(-1)
        else:
            retorno.append(1)
    return retorno

#Metodo que retorna o indice do neuronio com maior valor
def argmax(lista):
    maior = -2
    indice = 0
    
    for i, valor in enumerate(lista):
        if maior < valor:
            maior = valor
            indice = i
    
    return indice

#Metodo para calculo de erro
def media(oraculo, resultado):
    soma = 0
    for i in range(10):
        soma += abs(oraculo[i] - resultado[i])
    return soma/10

quantidade_camada_oculta = 20

#Classe abstrata de um neurônio artificial
class Neuronio(ABC):
    
    #Inicialização de pesos e bias (Deve ocorrer de maneira aleatoria)
    def __init__(self, total_pesos):
        self.w = []
        for i in range(total_pesos):
            self.w.append(r.uniform(-1, 1))
        self.b = r.uniform(-1, 1)
        self.taxa = 0.1
    
    #Somatorio de pesos com o valor de entrada
    def somatorio(self, lista_entrada):
        self.soma = 0
        for i, valor in enumerate(lista_entrada):
            self.soma += self.w[i]*valor
        self.soma += self.b
    
    #Ativação: tomada de decisão do neurônio
    def ativador(self):
        self.previsao = tanh(self.soma)
        return self.previsao

    #Atualização dos pesos: O verdadeiro aprendizado
    @abstractmethod
    def atualizar_pesos(self , a ,b):
        pass

#Primeira camada que processa as features e permite aprendizado não linear
class CamadaOculta(Neuronio):
    
    def atualizar_pesos(self, erro_oculto, vetor_entrada):
        delta_oculto = erro_oculto * (1 - self.previsao**2)
        for i, valor in enumerate(vetor_entrada):
            self.w[i] = self.w[i] + self.taxa*valor*delta_oculto
        self.b = self.b + self.taxa*delta_oculto

#Camada que fornece a saida
class CamadaSaida(Neuronio):
    
    def atualizar_pesos(self, delta_saida, vetor_previsoes):
        for i, valor in enumerate(vetor_previsoes):
            self.w[i] = self.w[i] + self.taxa*valor*delta_saida
        self.b  += self.taxa*delta_saida

    def saida(self, oraculo):
        erro = oraculo-self.previsao
        delta_saida = erro * (1 - self.previsao**2)
        erros_ocultos = []
        for i in range(quantidade_camada_oculta):
            erros_ocultos.append(delta_saida*self.w[i])
        return delta_saida, erros_ocultos

class RNA:
    
    def __init__(self, entradas, oraculos, classe_oraculo ,entradas_teste, oraculos_teste, 
            classe_oraculos_teste, lista_co, lista_cs):
        self.lista_co = lista_co
        self.lista_cs = lista_cs
        self.entradas = entradas
        self.oraculos = oraculos
        self.classe_oraculo = classe_oraculo
        self.entradas_teste = entradas_teste
        self.oraculos_teste = oraculos_teste
        self.classe_teste = classe_oraculos_teste
        
    def foward(self, entrada):
        self.prev1 = []
        self.prev2 = []
        
        for co in self.lista_co:
            co.somatorio(entrada)
            self.prev1.append(co.ativador())
        for i, cs in enumerate(self.lista_cs):
            cs.somatorio(self.prev1)
            self.prev2.append(cs.ativador())
        return self.prev2
    
    def backward(self, entrada, oraculo):
        vetor_aux = np.zeros(quantidade_camada_oculta)
        temp = []
        
        for i, cs in enumerate(self.lista_cs):
            delta_saida, erros_ocultos = cs.saida(oraculo[i])
            vetor_aux += erros_ocultos
            temp.append(delta_saida)
            
        for i, co in enumerate(self.lista_co):
            co.atualizar_pesos(vetor_aux[i], entrada)
            
        for i, cs in enumerate(self.lista_cs):
            cs.atualizar_pesos(temp[i], self.prev1)
            
    def aprendizado(self):
        erro_amostra = 0
        for i, dado in enumerate(self.entradas):
           resultado = self.foward(dado)
           self.backward(dado, self.classe_oraculo[i])
           erro_amostra += media(self.classe_oraculo[i], resultado)

        return erro_amostra/len(self.entradas)
    
    def score(self, entrada, classe):
        acertos = 0
        for i, dado in enumerate(entrada):
            resultado = self.foward(dado)
            x = argmax(resultado)
            
            if x == classe[i]:
                acertos += 1
            
        acuracia_total = (acertos/len(entrada))
        return acuracia_total*100
      
    def geracao(self, tempo):
        self.erros_medio_geracao = []
        self.acuracia_geracao = []
        erro = 0
        paciencia = 5
        contador = 0
        melhor_erro = 99999999999999
        
        for i in range(tempo):
            erro = self.aprendizado()
            self.erros_medio_geracao.append(erro)
            self.acuracia_geracao.append(self.score(self.entradas_teste, self.oraculos_teste))

            if erro < melhor_erro:
                melhor_erro = erro
                contador = 0
            elif erro > melhor_erro:
                contador += 1
            elif contador == paciencia:
                return self.acuracia_geracao, self.erros_medio_geracao
        
        return self.acuracia_geracao, self.erros_medio_geracao
    
#Código de normalização feitor pelo gemini
def normalizar(X_t, ret):
    X_t = np.asanyarray(X_t).astype(np.float64) 
    
    if X_t.ndim == 1:
        X_t = X_t.reshape(1, -1)

    rows, cols = X_t.shape
    
    if ret == 0:
        parametros = []
        for j in range(cols):
            mi, ma = np.min(X_t[:, j]), np.max(X_t[:, j])
            diff = ma - mi
            parametros.append((mi, ma))
            if diff != 0:
                X_t[:, j] = 2 * ((X_t[:, j] - mi) / diff) - 1
            else:
                X_t[:, j] = 0.0
        return X_t, parametros
    else:
        for j in range(cols):
            mi, ma = ret[j]
            diff = ma - mi
            if diff != 0:
                X_t[:, j] = 2 * ((X_t[:, j] - mi) / diff) - 1
            else:
                X_t[:, j] = 0.0
        return X_t, None
                
def main():
    X = dados.data
    y = dados.target
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=39)
    X_train, ret = normalizar(X_train, 0)
    X_test, _ = normalizar(X_test, ret)
    
    lista_co = []
    lista_cs = []
    classe_teste = []
    classe_treino = []
    for i in y_train:
        classe_treino.append(normalizacao_target(i))
    for i in y_test:
        classe_teste.append(normalizacao_target(i))
        
    for i in range(20):
        co = CamadaOculta(64)
        lista_co.append(co)
    for i in range(10):
        cs = CamadaSaida(quantidade_camada_oculta)
        lista_cs.append(cs)
        
    bmo = RNA(X_train, y_train, classe_treino, X_test, y_test, classe_teste, lista_co, lista_cs)
    acuracia, erros = bmo.geracao(108)
    plt.figure("Erro") 
    plt.plot(erros, color='red')
    plt.title("Evolução do Erro")
    plt.xlabel("Gerações")
    plt.ylabel("Erro")
    plt.xlim(0, len(erros)-1)
    plt.ylim(0, max(erros) * 1.1)

    
    plt.figure("Acurácia")
    plt.plot(acuracia, color='blue')
    plt.title("Acurácia x Geração")
    plt.xlabel("Gerações") 
    plt.ylabel("Acurácia")
    plt.xlim(0, len(acuracia)-1)
    plt.ylim(0, max(acuracia) * 1.1)
    plt.show()
    for i in range(108):
        print(f"Acurácia geração {i}: {acuracia[i]:.2f}")

main()
    
    