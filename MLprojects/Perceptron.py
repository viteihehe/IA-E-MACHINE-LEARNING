import matplotlib.pyplot as plt
import random as r

class Pessoa:
    def __init__(self, ensino_medio_completo, emprego_formal):
        self.ensino_medio_completo = ensino_medio_completo
        self.emprego_formal = emprego_formal

class Perceptron:
    def __init__(self, lista_entrada, lista_oraculo):
        self.entrada = lista_entrada
        self.oraculo = lista_oraculo
        self._taxa = 0.1
    
    def inicializar_pesos(self):
            self.peso1 = r.randint(0,5)
            self.peso2 = r.randint(0,5)
            self.bias = r.randint(0,5)
        
    def somatorio(self, dado):
        self.soma = 0
        self.soma = (self.peso1*dado.ensino_medio_completo)+(self.peso2*dado.emprego_formal)+self.bias
    
    def ativador(self, dado):
        self.somatorio(dado)
        if self.soma >= 0:
            return 1
        else:
            return 0
        
    def Aprendizado(self):
        for i in range(15):
            erro_total = 0
            for indice, dado in enumerate(self.entrada):
                temp = self.ativador(dado)
                erro = self.oraculo[indice]-temp
                erro_total += erro
                self.peso1 = self.peso1+self._taxa*dado.ensino_medio_completo*erro
                self.peso2 = self.peso2+self._taxa*dado.emprego_formal*erro
                self.bias = self.bias+self._taxa*erro
            if erro_total == 0:
                break
                
    def processar(self, entrada):
        x = self.ativador(entrada)
        return x

def grafico(dado, dado2, x):
    plt.figure("Perceptron")
    plt.xlabel("Ensino médio completo")
    plt.ylabel("Emprego Formal")
    plt.grid(True)
    plt.xlim(0,2)
    plt.ylim(0,2)
    x_lista = []
    y_lista = []
    for x_linha in range(-2, 4):
        y_linha = -(dado2.peso1/dado2.peso2)*x_linha-(dado2.bias/dado2.peso2)
        x_lista.append(x_linha)
        y_lista.append(y_linha)
        
    plt.plot(x_lista, y_lista)
    if x:
        plt.scatter(dado.ensino_medio_completo, dado.emprego_formal, c='green', s=100)
    else:    
        plt.scatter(dado.ensino_medio_completo, dado.emprego_formal, c='red', s=100)    
    plt.show()    
    

def main():
    pessoa1 = Pessoa(0,0)
    pessoa2 = Pessoa(0,1)
    pessoa3 = Pessoa(1,0)
    pessoa4 = Pessoa(1,1)
    pessoa5 = Pessoa(0,1)
    pessoa6 = Pessoa(1,1)
    pessoa7 = Pessoa(0,0)
    
    entradas = [
        pessoa1, pessoa2, pessoa3, pessoa4, pessoa5, pessoa6, pessoa7
    ]
    respostas = [
        0, 0, 0, 1, 0, 1, 0
    ]
    
    agente = Perceptron(entradas, respostas)
    agente.inicializar_pesos()
    agente.Aprendizado()
    
    pessoa_teste = Pessoa(1,1)
    x = agente.processar(pessoa_teste)
    grafico(pessoa_teste, agente, x)

main()