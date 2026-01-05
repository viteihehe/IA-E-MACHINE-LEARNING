import random as r

sala = {"pos":"A", "A":"sujo", "B":"sujo"}

def main():
 
    for i in range(8):    
        posicao = sala["pos"]
        estado = sala[posicao]
        acao = aspirador(posicao, estado)
        if(acao == "aspirar"):
            sala[posicao] = "limpo"
        elif(sala["A"] == "limpo" and sala["B"] == "limpo"):
            print("Ambiente limpo")
            break
        elif(acao == "direita" and posicao != "B") :
            sala["pos"] = "B" 
        elif(acao == "esquerda" and posicao != "A"):
            sala["pos"] = "A"
        
        print(acao, end=" | ")
    return None

def aspirador(posicao, estado: str):
    if(estado.lower() == "sujo"):
        return "aspirar"
    elif(posicao == "A"):
        return "direita"
    elif(posicao == "B"):
        return "esquerda"
    return None

main()