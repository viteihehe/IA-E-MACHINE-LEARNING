import random as r
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

class Amostras:
    def __init__(self, dados):
        self.x1 = dados[0]
        self.x2 = dados[1]
       
        

class Perceptron:
    def __init__(self, lista_treinamento, lista_oraculo):
        self.lista_treinamento = lista_treinamento
        self.lista_oraculo = lista_oraculo
        self.score = []
        self.taxa = 0.1
    
    def pesos_iniciais(self):
        self.w1 = r.randint(0, 10)
        self.w2 = r.randint(0, 10)
        self.bias = r.randint(0, 10)
    
    def somatorio(self, dado):
        soma = ((self.w1*dado.x1) + (self.w2*dado.x2) + self.bias)
        return soma
    
    def ativador(self, soma):
        if soma >= 0:
            return 1
        else:
            return 0
    
    def treinamento(self):
        for i in range(10000):
            erro_total = 0
            for indice, dado in enumerate(self.lista_treinamento):
                soma = self.somatorio(dado)
                resposta = self.ativador(soma)
                erro = self.lista_oraculo[indice]-resposta
                if erro != 0:
                    erro_total += abs(erro)
                    self.w1 = self.w1 + self.taxa*erro*dado.x1
                    self.w2 = self.w2 +self.taxa*erro*dado.x2
                    self.bias = erro*self.taxa
                      
            if erro_total == 0:
                break
    
    def calcular_score(self):
        acertos = 0
        for indice, dado in enumerate(self.lista_treinamento):
            previsao = self.processar(dado)
            if previsao == self.lista_oraculo[indice]:
                acertos += 1
        acuracia = (acertos/len(self.lista_treinamento))*100
        return acuracia
    
    def processar(self, entrada):
        temp = self.somatorio(entrada)
        x = self.ativador(temp)
        return x
        
        
        

X, y = make_blobs(n_samples=100, centers=2, n_features=2, random_state=42)
amostras = []
lista_oraculo = []

for coordenadas, rotulo in zip(X, y):
    novo_ponto = Amostras(coordenadas)
    novo_rotulo = rotulo
    amostras.append(novo_ponto)
    lista_oraculo.append(novo_rotulo)

agente = Perceptron(amostras, lista_oraculo)
agente.pesos_iniciais()
agente.treinamento()

novo_ponto = Amostras((3, 4))
x = agente.processar(novo_ponto)
grafico(X, y, agente, x, novo_ponto)
print(f"Acurácia:{agente.calcular_score()}")


    


    

    