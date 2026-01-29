import random

class Aspirador:
    def __init__(self, posicao, ligado):
        self.posicao = posicao
        self.ligado = ligado
    
    def aspirar(self, sensor: str):
        if(sensor.lower() == "sujo"):
            return "limpo"
        else:
            return self.mover()
    
    def mover(self):
        if(self.posicao == 'A'):
            return "direita"
        elif(self.posicao == 'B'):
            return "esquerda"
        
    def __str__(self):
        return f"{self.__class__.__name__}] = {', '.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}" 
    
class Sala:
    def __init__(self, estado_A, estado_B):
        self.estado_A = estado_A
        self.estado_B = estado_B
    
    def verifica(self, mudanca, regiao):
        if(mudanca == "limpo" and regiao == "A"):
            self.estado_A = mudanca
        elif(mudanca == "limpo" and regiao == "B"):
            self.estado_B = mudanca
    
    def __str__(self):
        return f"{self.__class__.__name__} = {', '.join([f'{chave} = {valor}' for chave, valor in self.__dict__.items()])}"

def criar_sala():
    x = random.randint(1, 4)
    match x:
        case 1:
            sala = Sala("sujo", "sujo")
        case 2:
            sala = Sala("sujo", "limpo")
        case 3:
            sala = Sala("limpo", "sujo")
        case 4:
            sala = Sala("limpo", "limpo")
    
    return sala
        
def main():
    sala = criar_sala()
    aspirador = Aspirador("A", True)
    for i in range(5):
        print(f"turno {i+1}")
        print(sala, end='\n')
        print(aspirador, end='\n')
        
        if(aspirador.posicao == 'A'):
            x = aspirador.aspirar(sala.estado_A)
            if(x == "limpo"):
                sala.verifica(x, 'A')
                print("Limpando a sala")
            elif x == 'direita':
                aspirador.posicao = 'B'
                print("movendo para B")
        elif(aspirador.posicao == 'B'):
            x = aspirador.aspirar(sala.estado_B)
            if(x == "limpo"):
                sala.verifica(x, 'B')
                print("Limpando a sala")
            elif x == 'esquerda':
                aspirador.posicao = 'A'
                print("Movendo para A")

main()