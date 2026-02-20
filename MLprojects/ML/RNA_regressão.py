import matplotlib.pyplot as ptl
import math as m 
import numpy as np
import random as r
import pandas as pd
from abc import ABC, abstractmethod

dados = np.genfromtxt('dados.csv', delimiter=',', skip_header=1)
tabela = pd.read_csv('dados.csv')

print(tabela.head())

def normalizar(entrada):
    for i in range(entrada.shape[1]):
        mi = np.min(entrada[:, i]) 
        ma = np.max(entrada[:, i]) 
        diff = ma - mi
        
        for j in range(entrada.shape[0]):
            if diff == 0:
                entrada[j, i] = 0
            else:
                entrada[j, i] = 2 * ((entrada[j, i] - mi) / diff) - 1 
                
n_co = 5
normalizar(dados)
X_train = dados[1:700, :4]
y_train = dados[1:700, 4]
X_test = dados[:700, :4]
y_test = dados[:700, 4]

linhas = 697
linhas_teste = 300            

class Regressao_linear:
    
    def __init__(self, entrada, oraculo):
        self.entrada = entrada
        self.oraculo = oraculo
        self.w = []
        for i in range(4):
            self.w.append(r.uniform(-1, 1))
        self.b = r.uniform(-1, 1)
        self.taxa = 0.001
    
    def ativador(self, valores):
        valor = 0
        for i in range(4):
            valor += self.w[i]*valores[i]
        valor += self.b
        return valor
    
    
    def calculo(self):
        erro_total = 0
        custo_b = 0
        custo_x_total = np.zeros(4)
        for i in range(linhas):
            custo_x = np.zeros(4)
            reg = 0
            for j in range(4):
                reg += self.w[j]*self.entrada[i, j]
            reg += self.b
            erro = (reg - self.oraculo[i])
            for z in range(4):
                custo_x[z] += (2*(erro)*self.entrada[i, z])
                
            custo_x_total = custo_x_total + custo_x
            
            custo_b += 2*erro
            
            erro_total += erro**2
            
        return float(erro_total), custo_x_total, custo_b
    
    def atualizar(self, custo_x, custo_b):
        for i in range(4):
            self.w[i] = self.w[i] - self.taxa*custo_x[i]
        self.b = self.b - self.taxa*custo_b
    
    def aprendizado(self, geracao):
        erro_geracao = []
        melhor_erro = 999999999999
        paciencia = 10
        contador = 0
        for i in range(geracao):
            erro, custo_x, custo_b = self.calculo()
            erro_geracao.append(erro)
            for j in range(4):
                custo_x[j] = custo_x[j]/linhas
            custo_b = custo_b/linhas
            self.atualizar(custo_x, custo_b)
            
            if erro < melhor_erro:
                melhor_erro = erro
                contador = 0
            elif contador >= paciencia:
                return erro_geracao
            elif erro > melhor_erro:
                contador += 1
        return erro_geracao
                
    def score(self, entrada_teste, oraculo_teste):
        erro_total = 0
        for i in range(linhas_teste):
            reg = self.ativador(entrada_teste[i])
            erro = (reg - oraculo_teste[i])**2
            erro_total += erro
        erro_total = erro_total*(1/linhas_teste)
        RMSE = m.sqrt(erro_total)
        
        return RMSE
        
    

class Neuronio(ABC):
    
    def __init__(self, num_features):
        if num_features == 1:
            self.w = r.uniform(-1, 1)
        else:
            self.w = []
            for i in range(num_features):
                self.w.append(r.uniform(-1, 1))
        self.b = r.uniform(-1, 1)
        self.taxa = 0.00000001
    
    def somatorio(self, entrada):
        self.soma = 0
        for i, valor in enumerate(entrada):
            self.soma += self.w[i]*valor
        self.soma += self.b
    
    @abstractmethod
    def atualizar_pesos(self):
        pass
    
    @abstractmethod
    def ativador(self):
        pass
    
class CamadaOculta(Neuronio):
    
    def __init__(self, num_features):
        super().__init__(num_features)
    
    def ativador(self):
        self.predicao = np.tanh(self.soma)
        return self.predicao
    
    def atualizar_pesos(self, erro_oculto ,entrada):
        delta_oculto = erro_oculto * (1 - self.predicao**2)
        for i in range(4):
            self.w[i] = self.w[i] + self.taxa*delta_oculto*entrada[i]
        self.b = self.b + delta_oculto*self.taxa
        
class CamadaSaida(Neuronio):
    
    def __init__(self, num_features):
        super().__init__(num_features)
    
    def ativador(self):
        self.predicao = self.soma
        return self.predicao
    
    def atualizar_pesos(self, delta_saida, entrada):
        for i in range(n_co):
            self.w[i] = self.w[i] + self.taxa*delta_saida*entrada[i]
        self.b = self.b + self.taxa*delta_saida
    
    def saida(self, oraculo):
        erro = self.predicao-oraculo
        delta_saida = erro
        erro_oculto = []
        for i in range(n_co):
            erro_oculto.append(delta_saida*self.w[i])
        return delta_saida, erro_oculto

class RNA:
    
    def __init__(self, lista_co, cs, X_train, y_train, X_test, y_test):
        self.lista_co = lista_co
        self.cs = cs
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test
        
    def foward(self, entrada):
        self.predicao = []
        for camada in self.lista_co:
            camada.somatorio(entrada)
            self.predicao.append(camada.ativador())
        
        self.cs.somatorio(self.predicao)
        retorno = self.cs.ativador()
        return retorno
    
    def backward(self, entrada, oraculo):
        delta_saida, erro_oculto = self.cs.saida(oraculo)
        
        self.cs.atualizar_pesos(delta_saida, self.predicao)
        
        for i, camada in enumerate(self.lista_co):
            camada.atualizar_pesos(erro_oculto[i], entrada)
        
        return delta_saida
    
    def score(self):
        erro_total = 0
        for i in range(linhas_teste):
            x = self.foward(X_test[i])
            erro = (x - y_test[i])**2
            erro_total += erro
        erro_total = erro_total*(1/linhas_teste)
        RMSE = m.sqrt(erro_total)
        
        return RMSE
    
    def aprendizado(self, geracao):
        erro_geracao = []
        melhor_erro = 999999999999
        paciencia = 7
        contador = 0
        
        for i in range(geracao):
            erro = 0
            for j in range(linhas):
                self.foward(self.X_train[j])
                delta = self.backward(X_train[j], y_train[j])
                erro += delta**2
                
            erro = erro/linhas
            
            erro_geracao.append(erro)
            
            if erro < melhor_erro:
                melhor_erro = erro
                contador = 0
            elif contador >= paciencia:
                return erro_geracao
            elif erro > melhor_erro:
                contador += 1
                
        return erro_geracao
    
def main():
    lista_co = []
    for i in range(n_co):
        co = CamadaOculta(4)
        lista_co.append(co)
    cs = CamadaSaida(n_co)
    
    bmo = RNA(lista_co, cs, X_train, y_train, X_test, y_test)
    x = bmo.score()
    bmo.aprendizado(3000)
    
    mo = Regressao_linear(X_train, y_train)
    y = mo.score(X_test, y_test)
    mo.aprendizado(300)
    
    print("Pré- treinamento:")
    print(f"Score rna: {x:.2f}, Gradiente score: {y:.2f}")
    print("Pós treinamento:")
    print(f"Score rna: {bmo.score():.2f}, Gradiente score: {mo.score(X_test, y_test):.2f}")
    
main()    
            
        
        
    