import random as r
import matplotlib as plt
from sklearn.datasets import load_digits
import math as m
from sklearn.model_selection import train_test_split
import numpy as np

data = load_digits()

def tanh(pu):
    x = ((m.exp(pu) - m.exp(-pu))/(m.exp(pu) + m.exp(-pu)))
    return x

total_camada_oculta = 20
total_camada_saida = 10

class Camada_oculta:
    
    def __init__(self):
        self._w = []
        for i in range(64):
            self._w.append(r.randint(-1, 1))
        self._b1 = r.randint(-1, 1)
        self._tax = 0.1
        
    def add(self, lista_entrada):
        self.soma = 0
        for i, info in enumerate(lista_entrada):
            self.soma += (self._w[i]*info)
        self.soma += self._b1
        
    def activation(self):
        self.prectidion = tanh(self.soma)
        return self.prectidion
    
    def update(self, erro_oculto, lista_entrada):
        delta_oculto = erro_oculto * (1 - self.prectidion**2)
        for i, info in enumerate(lista_entrada):
            self._w[i] = self._w[i] + self._tax*info*delta_oculto
        self._b1 += self._tax*delta_oculto

class Camada_saida:
    
    def __init__(self):
        self.w2 = []
        for i in range(total_camada_oculta):
            self.w2.append(r.randint(-1, 1))
        self._b2 = r.randint(-1, 1)
        self._tax = 0.1
    
    def add(self, saidas_camada_oculta):
        self.somas = 0
        for i in range(total_camada_oculta):
            self.somas += (self.w2[i]*saidas_camada_oculta[i])
        self.somas += self._b2
    
    def activator(self):
        self.previsao = tanh(self.somas)
        return self.previsao
    
    def updade(self, delta_saida, saidas_camada_oculta):
        for i in range(total_camada_oculta):
            self.w2[i] = self.w2[i] + self._tax*delta_saida*saidas_camada_oculta[i]
        self._b2 += self._tax*delta_saida
    
    def exit(self, oraculo):
        erro = oraculo-self.previsao
        delta_saida = erro * (1 - self.previsao**2)
        erros_ocultos = []
        for i in range(total_camada_oculta):
            erros_ocultos.append((delta_saida*self.w2[i]))
        return delta_saida, erros_ocultos
        
def classificador(valor):
    lista = []
    for i in range(10):
        if i != valor:
            lista.append(-1)
        else:
            lista.append(1)
    return lista

def argmax(vetor):
    maior = -2
    indice = 0
    
    for i, valor in enumerate(vetor):
        if valor > maior:
            maior = valor
            indice = i
    
    return indice
            
class RNA:
    
    def __init__(self, lista_entrada, lista_oraculo, lista_classe_teste,lista_co, lista_cs, entradas_teste, entradas_teste_oraculo):
        self.lista_entrada = lista_entrada
        self.lista_oraculo = lista_oraculo
        self.lista_classe_teste = lista_classe_teste
        self.lista_co = lista_co
        self.lista_cs = lista_cs
        self.entradas_teste = entradas_teste
        self.entradas_teste_oraculo = entradas_teste_oraculo
        
    
    def foward(self, entrada):
        self.previsoes1 = []
        self.previsoes2 = []
        for co in self.lista_co:
            co.add(entrada)
            self.previsoes1.append(co.activator())
        for i ,cs in enumerate(self.lista_cs):
            cs.add(self.previsoes1)
            self.previsoes2.append(cs.activator())
        return self.previsoes2
    
    def bacward(self, entrada, oraculo):
        vetor_aux = np.zeros(total_camada_oculta)
        for j ,camada_saida in enumerate(self.lista_cs):
            delta_saida, erros_ocultos = camada_saida.exit(oraculo[j])
            camada_saida.update(delta_saida, self.previsoes1)
            vetor_aux += erros_ocultos
            
        for i, camada in enumerate(self.lista_co):
            camada.update(vetor_aux[i], entrada)
        
    def aprendizado(self):
        for i, dado in enumerate(self.lista_entrada):
            resultado = self.foward(dado)
            temp = classificador(self.lista_oraculo[i])
            erro += abs(temp-resultado)
            lista = classificador(self.lista_oraculo[i])
            self.bacward(dado, lista)
        return erro
    
    def erro_medio(self, erro):
        erro_total = 0
        for i in erro:
            erro_total += i
        self.erros.append((erro_total/len(self.lista_entrada)))
        return self.erros
    
    def score(self, entrada_teste,entrada_classe):
        acertos = 0
        for i, dado in enumerate(entrada_teste):
            x = self.foward(dado)
            indice = argmax(x)
            if indice == entrada_classe[i]:
                acertos += 1
        
        acuracia_total = (acertos/len(entrada_classe))
        return acuracia_total
                
    def acuracia_por_geracao(self):
        self.acuracias.append(self.score(self.entradas_teste, self.lista_classe_teste))
        return self.acuracias
    
    def tempo(self, geracao):
        self.erro_medio = []
        self.acuracia_por_geracao = []
        melhor_erro = 99999999999
        paciencia = 5
        contador = 0
        
        for i in range(geracao):
            erro = np.zeros(10)
            erro += self.aprendizado()
            
            self.erro_medio(erro)
            self.acuracia_por_geracao()
            
            if erro < melhor_erro:
                melhor_erro = erro
                contador = 0
            elif erro > melhor_erro:
                contador += 1
            elif contador >= paciencia:
                return
            
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
    X = data.data
    y = data.target
    X_train, y_train, X_test, y_teste = train_test_split(X, y, random_state=33, test_size=0.3)
    ret = normalizar(X_train, 0)
    normalizar(X_test, ret)
    camada_oculta = []
    camada_saida = []
    
    