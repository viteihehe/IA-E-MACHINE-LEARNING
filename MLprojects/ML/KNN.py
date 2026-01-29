import math as m
import random as r
import matplotlib.pyplot as plt
import numpy as np

class Cliente:
    def __init__(self, idade, notas, classe):
        self.idade = idade
        self.notas = notas
        self.classe = classe
        

class Classificador:
    def __init__(self, set_cliente):
        self.clientes = set_cliente
        self.K = 3
    
    def calcular_distancia(self, novo_ponto, ponto_existente):
        x = m.sqrt((ponto_existente.idade - novo_ponto.idade)**2+(ponto_existente.notas - novo_ponto.notas)**2)
        classe = ponto_existente.classe
        return x, classe
    
    def classificar(self, novo_ponto):
        lista_aux = []
        for i in self.clientes:
            (distancia, classe) = self.calcular_distancia(novo_ponto, i)
            lista_aux.append((distancia, classe))
        lista_aux.sort()
        cont_1 = 0
        cont_0 = 0
        for i in range(self.K):
            (distancia, classe) = lista_aux[i]
            if classe == 0:
                cont_0 += 1
            else:
                cont_1 += 1
        if cont_1 > cont_0:
            novo_ponto.classe = 1
        elif (cont_1 == cont_0):
            novo_ponto.classe = r.randint(0, 1)
        else:
            novo_ponto.classe = 0
            

def grafico(lista):
    
    
    
    plt.figure(1)
    plt.title("KNN")
    plt.xlabel("Idade:")
    plt.ylabel("Notas:")
    plt.grid(True)
    plt.xlim(10, 20)
    plt.ylim(0, 10)
    for i in lista:
        if i.classe == 0:
            plt.scatter(i.idade, i.notas, color='red', s=100)
        else:
            plt.scatter(i.idade, i.notas, color='blue', s=100)
    plt.show()

def main():
    cliente_1 = Cliente(12, 5, 1)
    cliente_2 = Cliente(12, 3, 0)
    cliente_3 = Cliente(15, 6, 1)
    cliente_4 = Cliente(15, 1, 0)
    cliente_5 = Cliente(18, 7, 1)
    cliente_6 = Cliente(18, 5, 0)
    
    clientes = [
        cliente_1, cliente_2, cliente_3, cliente_4, cliente_5, cliente_6
        ]
    
    agente = Classificador(clientes)
    
    x = 1
    while x:
        print("Sistema de classificação KNN:")
        print("1- inserir gráfico\n2 - sair")
        x = input("Insira um numero:")
        
        match int(x):
            case 1:
                nota = input("Insira a nota:\n")
                idade = input("Insira a idade:\n")
                novo_cliente = Cliente(int(idade), int(nota), None)
                agente.classificar(novo_cliente)
                clientes.append(novo_cliente)
                grafico(clientes)
                break
            case 2:
                x = False
                break
        
    
    
main()
        
