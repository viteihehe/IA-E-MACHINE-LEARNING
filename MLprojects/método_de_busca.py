import random
import heapq
import time
        
class No:
    
    def __init__(self, estado, pai=None, custo=0):
        self.estado = estado
        self.pai = pai
        self.custo = custo

    def criar_no(self, no_atual, novo_estado):
        novo_no = No(
            novo_estado, no_atual, no_atual.custo + 1
        )
        return novo_no
              
    
    def resolucao(self, labirinto, no):
        Filhos = []
        x,y = no.estado 
        
        if 0 <= x+1 < len(labirinto) and labirinto[x+1][y] == 0:
            novo_estado = (x+1, y)
            Filhos.append(self.criar_no(no, novo_estado))
        if  0 <= y+1 < len(labirinto[0]) and labirinto[x][y+1] == 0 :
            novo_estado = (x, y+1)
            Filhos.append(self.criar_no(no, novo_estado))
        if 0 <= x-1 <len(labirinto) and labirinto[x-1][y] == 0:
            novo_estado = (x-1, y)
            Filhos.append(self.criar_no(no, novo_estado))
        if 0 <= y-1 < len(labirinto[0]) and labirinto[x][y-1] == 0:
            novo_estado = (x, y-1)
            Filhos.append(self.criar_no(no, novo_estado))
            
        return Filhos
    
    
    def busca(self, inicio, objetivo, labirinto):
        fronteira = []
        
        visitados = set()
        contador = 0
        heapq.heappush(fronteira, (0, contador ,No(inicio)))
        contador += 1
         
        while fronteira:
            _, _, no_atual = heapq.heappop(fronteira)
            
            if no_atual.estado == objetivo:
                return no_atual
            if no_atual.estado in visitados:
                continue
            visitados.add(no_atual.estado)
            
            filhos = no_atual.resolucao(labirinto, no_atual)
            
            for filho in filhos:
                heapq.heappush(
                    fronteira,
                    (filho.custo, contador ,filho)
                )
                contador += 1
        return None
    
class Labirinto:
    def __init__(self):
        self.corpo = []
        for i in range(9):
            linha = []
            for j in range(9):
                linha.append(random.randint(0,1))
            self.corpo.append(linha)
        self.corpo[0][0] = 0
        self.corpo[8][8] = 0
    pass


def desenhar_lab(labirinto, posicao_atual):
        x_atual, y_atual = posicao_atual
        
        for i in range(len(labirinto)):
            for j in range(len(labirinto[0])):
                if (i,j) == (x_atual, y_atual):
                    print("●", end=" ")
                elif labirinto[i][j] == 1:
                    print("█", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()
        
def reconstruir_caminho(no):
        caminho = []
        while no:
            caminho.append(no.estado)
            no = no.pai
        return caminho[::-1]

    

def main():
    raiz = No((0,0))
    #labirinto = Labirinto().corpo
    labirinto = [
    [0,0,0,1,1,1,1,1,1],
    [1,1,0,1,1,1,1,1,1],
    [1,1,0,0,0,1,0,1,1],
    [1,1,1,1,0,1,0,1,1],
    [1,1,1,1,0,1,0,1,1],
    [1,1,1,1,0,0,0,0,0],
    [1,1,1,1,1,0,1,1,0],
    [1,1,1,1,1,1,1,1,0],
    [1,1,1,1,1,1,1,1,0],
]
    resuldado_busca = raiz.busca(raiz.estado, (8,8), labirinto)
    caminho = reconstruir_caminho(resuldado_busca)
    
    if resuldado_busca == None:
        print("Labirinto sem camihno")
    else:
        for pos in caminho:
            desenhar_lab(labirinto, pos)
            time.sleep(0.5)
    
 
    
main()