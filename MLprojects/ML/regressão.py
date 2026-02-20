import random as r
import matplotlib.pyplot as plt
import math as m
import numpy as np
import pandas as pd


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
                

normalizar(dados)
X_train = dados[1:700, :4]
y_train = dados[1:700, 4]
X_test = dados[:700, :4]
y_test = dados[:700, 4]

linhas = 697
linhas_teste = 300
    
class Gradiente:
    
    def __init__(self, entrada, oraculo):
        self.entrada = entrada
        self.oraculo = oraculo
        self.taxa = 0.001
        self.w = []
        for i in range(4):
            self.w.append(r.uniform(-1, 1))
        self.b = r.uniform(-1, 1)
        
    
    
    
    def atualizar(self, custo_x, custo_b):
        for i in range(4):
            self.w[i] = self.w[i] - self.taxa*custo_x[i]
        self.b = self.b - self.taxa*custo_b

    def calculo(self, entrada, oraculo):
        erro_total = 0
        custo_b = 0
        custo_x_total = np.zeros(4)
        for i in range(linhas):
            custo_x = []
            
            reg = 0
            for j in range(4):
                reg += self.w[j]*entrada[i, j]
            
            reg += self.b
            erro = (reg - oraculo[i])
            for j in range(4):
                custo_x.append(2*(erro)*entrada[i, j])
            custo_x_total += custo_x
            custo_b += 2*(erro)
            erro_total += erro**2
        return erro_total, custo_x_total, custo_b

    def tempo(self, geracao):
        erro_geracao = []
        menor_erro = 999999999999
        paciencia = 10
        contador = 0
        for i in range(geracao):
            erro, custo_x, custo_b = self.calculo(self.entrada, self.oraculo)
            for j in range(4):
                custo_x[j] = custo_x[j]/linhas
            custo_b = (custo_b/linhas)
            self.atualizar(custo_x, custo_b)
            erro_geracao.append(erro)
            
            if erro < menor_erro:
                menor_erro = erro
                contador = 0
            elif contador >= paciencia:
                return erro_geracao
            elif erro > menor_erro:
                contador += 1
        return erro_geracao
    
    def score(self, entrada_teste, oraculo_teste):
        erro_total = 0
        for i in range(linhas_teste):
            reg = self.ativador(entrada_teste[i])
            erro = ((reg - oraculo_teste[i])**2)
            erro_total += erro
        erro_total = erro_total*(1/linhas_teste)
        RMSE = m.sqrt(erro_total)

        return RMSE
    
    def ativador(self, entrada):
        valor = 0
        for i in range(4):
            valor += self.w[i]*entrada[i]
        valor += self.b
        return valor
        
        
def main():
       
        bmo = Gradiente(X_train, y_train)
        baseline = bmo.score(X_test, y_test)
        erro_tempo = bmo.tempo(500)
        score = bmo.score(X_test, y_test)
        
        contador = 1
        for i in erro_tempo:
            print(f"Geração {contador}: {i:.2f}")
            contador += 1
        print(f"Baseline: {baseline:.2f} Score: {score:.2f}")
    
        
        
main()