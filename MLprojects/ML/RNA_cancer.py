from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import math as m
import random as r
import numpy as np

dados = load_breast_cancer()

def grafico(dados):
    graf = pd.DataFrame(data=dados.data, columns=dados.feature_names)
    graf['Target'] = dados.target
    graf["Target Names"] = pd.Categorical.from_codes(dados.target, dados.target_names)
    print(graf.head())
    graf.plot.scatter('mean radius', 'mean texture', c=dados.target, cmap='viridis')
    plt.show()



def tanh(pu):
    x = (m.exp(pu) - m.exp(-pu))/(m.exp(pu)+ m.exp(-pu))
    return x

class Atributos:
    def __init__(self, dados):
        self.dados = dados
        
#Camadas
class Camada_oculta:
    def __init__(self):
        self.w = []
        for i in range(30):
            self.w.append(r.randint(-1, 1))
        self.b1 = r.randint(-1, 1)
        self._taxa = 0.1
        
    
    def somatorio(self, entrada):
        self.soma = 0
        for i, dado in enumerate(entrada):
            self.soma += (self.w[i]*dado)
        self.soma += self.b1
    
    def ativador(self):
        self.previsao = tanh(self.soma)
        return self.previsao
    
    def atualizar_pesos(self, erro_oculto, entrada):
        delta_oculto = erro_oculto * (1-self.previsao**2)
        for i, dado in enumerate(entrada):
            self.w[i] = self.w[i] + self._taxa*delta_oculto*dado
        self.b1 = self.b1 + self._taxa*delta_oculto
        
class Camada_saida:
    def __init__(self):
        self.w2 = []
        for i in range(5):
            self.w2.append(r.randint(-1, 1))
        self.b2 = r.randint(-1, 1)
        self._taxa = 0.1
    
    def somatorio(self, valores_passados):
        self.somas = 0
        for i in range(5):
            self.somas += self.w2[i]*valores_passados[i]
        self.somas += self.b2
            
    def atualizar_pesos(self, deslta_saida, valores_passados):
        for i in range(5):
            self.w2[i] = self.w2[i] + self._taxa*deslta_saida*valores_passados[i]
        self.b2 = self.b2 + self._taxa*deslta_saida
    
    def ativador(self):
       self.previsao = tanh(self.somas)
       return self.previsao

    def saida(self, oraculo):
        erro = oraculo-self.previsao
        delta_saida = erro * (1 - self.previsao**2)
        erros_ocultos = []
        for i in range(5):
            x = delta_saida*self.w2[i]
            erros_ocultos.append(x)
        return delta_saida, erros_ocultos
    
    
    
class RNA:
    def __init__(self, lista_entrada, lista_oraculos, lista_co, cs, entradas_teste, oraculo_teste):
        self.lista_entrada = lista_entrada
        self.lista_oraculo = lista_oraculos
        self.lista_co = lista_co
        self.cs = cs
        self.entradas_teste = entradas_teste
        self.oraculo_teste = oraculo_teste
        
    def foward(self, entrada):
        self.previsoes = []
        for camada in self.lista_co:
            camada.somatorio(entrada)
            x = camada.ativador()
            self.previsoes.append(x)
        self.cs.somatorio(self.previsoes)
        y = self.cs.ativador()
        return y
    def backward(self, oraculo, entrada):
        delta_saida, erro_ocultos = self.cs.saida(oraculo)
        for i, camada in enumerate(self.lista_co):
            camada.atualizar_pesos(erro_ocultos[i], entrada)
        self.cs.atualizar_pesos(delta_saida, self.previsoes)
        
    def aprendizado(self, geracao):
        melhor_erro = 99999999999
        paciencia = 5
        contador = 0
        self.lista_erros = []
        self.lista_acuracia = []
        for i in range(geracao):
            erro = 0
            for indice, dado in enumerate(self.lista_entrada):
                resultado = self.foward(dado)
                erro += abs(self.lista_oraculo[indice]-resultado)
                self.backward(self.lista_oraculo[indice], dado)
                
            erro_medio = erro/len(self.lista_entrada)
            self.lista_acuracia.append(self.score(self.entradas_teste, self.oraculo_teste))
            self.lista_erros.append(erro_medio)
            
            if erro < melhor_erro:
                melhor_erro = erro
                contador = 0
            elif erro > melhor_erro:
                contador += 1
            elif contador == paciencia:
                return self.lista_erros, self.lista_acuracia
            
            
        return self.lista_erros, self.lista_acuracia
                
    def score(self, entradas_teste, oraculo_teste):
        acertos = 0
        for i, dados in enumerate(entradas_teste):
            x = self.foward(dados)
            if x < 0 and oraculo_teste[i] == 0:
                acertos += 1
            elif x >= 0 and oraculo_teste[i] == 1:
                acertos += 1
        acuracia = (acertos/len(entradas_teste))*100
        return acuracia
                
                
def normalizar(X_t, ret):
    retorno = []
    if ret == 0:
        for j in range(X_t.shape[1]):
            mi = min(X_t[:, j])
            ma = max(X_t[:, j])
            retorno.append((mi, ma))
            for i in range(X_t.shape[0]):
                X_t[i, j] = 2*((X_t[i, j]-mi)/(ma-mi))-1
        return retorno
    else:
        for j in range(X_t.shape[1]):
            mi, ma = ret[j]
            for i in range(X_t.shape[0]):
                X_t[i, j] = 2*((X_t[i, j]-mi)/(ma-mi))-1

def main():
    X = dados.data
    y = dados.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=33, test_size=0.3)   
    ret = normalizar(X_test , 0)
    normalizar(X_train, ret)
    co_1 = Camada_oculta()
    co_2 = Camada_oculta()
    co_3 = Camada_oculta()
    co_4 = Camada_oculta()
    co_5 = Camada_oculta()
    CO = [co_1, co_2, co_3, co_4, co_5]
    cs = Camada_saida()
    
    
    BMO = RNA(X_train, y_train, CO, cs, X_test, y_test)
    erros, acuracia = BMO.aprendizado(108)
    x = BMO.score(X_test, y_test)
    plt.figure("erro x geração")
    plt.xlim(0, len(erros)-1)
    plt.ylim(0, max(erros))
    plt.xlabel("Gerações")
    plt.ylabel("Erros:")
    plt.plot(erros)
    plt.show()
    for i in range(108):
        print(f"Acurácia geração {i}: {acuracia[i]:.2f}")
    print(f"Score final: {x:.2f}")
    
main()