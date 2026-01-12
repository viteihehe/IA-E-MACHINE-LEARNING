import random as r
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import math as m
import numpy as np

def plot_mapa_cor(X, y, rede):
    # 1. Definir os limites do gráfico
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    
    # 2. Criar a grade de pontos (meshgrid)
    # O passo (step) 0.1 define a resolução. Quanto menor, mais suave o mapa.
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                         np.arange(y_min, y_max, 0.1))
    
    # 3. Fazer a rede classificar cada ponto da grade
    grid_points = np.c_[xx.ravel(), yy.ravel()]
    preds = []
    for pt in grid_points:
        # Transformamos o ponto em um objeto Amostra como sua rede espera
        amostra_pt = Amostra(pt)
        preds.append(rede.foward(amostra_pt))
    
    Z = np.array(preds).reshape(xx.shape)

    # 4. Plotar o mapa de cores
    plt.figure(figsize=(10, 7))
    # 'cmap' define as cores (RdBu é Red-Blue, ótimo para binário)
    plt.contourf(xx, yy, Z, alpha=0.3, cmap='RdBu') 
    
    # 5. Plotar os pontos reais por cima
    plt.scatter(X[y == 1, 0], X[y == 1, 1], c='blue', edgecolors='k', label='Classe 1')
    plt.scatter(X[y == 0, 0], X[y == 0, 1], c='red', edgecolors='k', label='Classe 0')
    
    plt.title("Mapa de Decisão da RNA (tanh)")
    plt.colorbar(label="Saída da Rede (tanh)")
    plt.legend()
    plt.show()

class Amostra:
    def __init__(self, features):
        self.x1 = features[0]
        self.x2 = features[1]
        
def tanh(pu):
    x = (m.exp(pu) - m.exp(-pu))/(m.exp(pu)+m.exp(-pu))
    return x

class Rede:
    def __init__(self, camada_oculta, camada_saida, lista_entrada, lista_saida):
        self.co = camada_oculta
        self.lista_entrada = lista_entrada
        self.lista_saida = lista_saida
        self.cs = camada_saida
        
    def foward(self, entrada):
        self.co.somatorio(entrada)
        previsao = self.co.ativador()
        self.cs.somatorio(previsao)
        x = self.cs.ativador()
        return x
    def backward(self, entrada, oraculo):
       erro_oculto, delta_saida = self.cs.saida(oraculo)
       self.co.atualizar_pesos(erro_oculto, entrada)
       self.cs.atualizar_pesos(delta_saida)
    
    def aprendizado(self, geracoes):
        for i in range(geracoes):
            for indice, dado in enumerate(self.lista_entrada):
                self.foward(dado)
                self.backward(dado, self.lista_saida[indice])
    
    def score(self):
        acertos = 0
        for indice, dado in enumerate(self.lista_entrada):
            x = self.foward(dado)
            if x  < 0 and self.lista_saida[indice] == 0:
                acertos += 1
            elif x >= 0 and self.lista_saida[indice] == 1:
                acertos += 1
                
        acuracia = (acertos/len(self.lista_entrada))*100
        return acuracia

class Camada_oculta:
    def __init__(self, lista_entradas):
        self.w1 = r.randint(-1, 1)
        self.w2 = r.randint(-1, 1)
        self.bias = r.randint(-1, 1)
        self._tax = 0.1
        self.lista_entradas = lista_entradas
    
    def somatorio(self, entrada):
        self.soma = (self.w1*entrada.x1 + self.w2*entrada.x2 + self.bias)
    
    def ativador(self):
        self.previsao = tanh(self.soma)
        return self.previsao
    
    def atualizar_pesos(self, erro_oculto, entrada):
        delta_oculto = erro_oculto * (1-self.previsao**2)
        self.w1 = self.w1 + delta_oculto*self._tax*entrada.x1
        self.w2 = self.w2 + delta_oculto*self._tax*entrada.x2
        self.bias = self.bias + delta_oculto*self._tax
        
class Camada_saida:
    def __init__(self, lista_oraculo):
        self.w3 = r.randint(-1, 1)
        self.bias2 = r.randint(-1, 1)
        self._taxa = 0.1
       
        self.lista_oraculo = lista_oraculo
        
    def somatorio(self, valor):
        self.valor = valor
        self.soma = self.w3*self.valor+self.bias2
    
    def ativador(self):
        self.previsao = tanh(self.soma)
        return self.previsao

    def atualizar_pesos(self, delta_saida):
        self.w3 = self.w3 + self._taxa*delta_saida*self.valor
        self.bias2 += self._taxa*delta_saida
    
    def saida(self, oraculo):
        erro = oraculo-self.previsao
        delta_saida = erro * (1 - self.previsao**2)
        erro_oculto = delta_saida*self.w3
        return erro_oculto, delta_saida

X, y = make_blobs(n_samples=100, n_features=2, centers=2, random_state=0)

amostras = []
lista_oraculo = []

for coordenadas, rotulo in zip(X, y):
    novo_ponto = Amostra(coordenadas)
    novo_rotulo = rotulo
    amostras.append(novo_ponto)
    lista_oraculo.append(novo_rotulo)

camada_oculta = Camada_oculta(amostras)
camada_saida = Camada_saida(lista_oraculo)
agente = Rede(camada_oculta, camada_saida, amostras, lista_oraculo)
agente.aprendizado(1000)

plot_mapa_cor(X, y, agente)