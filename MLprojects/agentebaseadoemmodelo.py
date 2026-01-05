class Agente:
    def __init__(self):
        self.estado_interno = {
            "A" : "desconhecido",
            "B" : "desconhecido",
            "posicao" : None
        }
        self.ligado = True
    
    def sensor(self, estado_atual):
        if estado_atual["local"] == "A":
            self.estado_interno["posicao"] = estado_atual["local"]
            self.estado_interno["A"] = estado_atual["A"]
        else:
            self.estado_interno["posicao"] = "B"
            self.estado_interno["B"] = estado_atual["B"]
            
        if self.estado_interno["A"] == "limpo" and self.estado_interno["B"] == "limpo":
            print("Desligando")
            self.ligado = False
        
    def limpar(self, estado_atual):
        self.sensor(estado_atual)
        if self.estado_interno["posicao"] == "A" and self.estado_interno["A"] == "sujo":
            print("Limpando")
            self.estado_interno["A"] = "limpo"
            estado_atual["A"] = "limpo"
        elif self.estado_interno["posicao"] == "B" and self.estado_interno["B"] == "sujo":
            print("Limpando")
            self.estado_interno["B"] = "limpo"
            estado_atual["B"] = "limpo"
        else:
            self.mover(estado_atual)
        
    def mover(self, estado_atual):
        if self.estado_interno["posicao"] == "A":
            print("Indo para direita")
            self.estado_interno["posicao"] = "B"
            estado_atual["local"] = "B"
        else:
            print("Indo para esquerda")
            self.estado_interno["posicao"] = "A"
            estado_atual["local"] = "A"
def main():
    mundo = {"A": "sujo", "B": "sujo", "local": "A"}
    aspirador = Agente()
    
    while(aspirador.ligado):
        aspirador.limpar(mundo)
    
main()