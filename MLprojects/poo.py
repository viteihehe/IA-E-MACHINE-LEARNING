class bicicleta:
    def __init__(self, /, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
        pass
    def buzinar(self):
        print("buzina")
        pass
    def correr(self):
        print("Correndo")
        pass
    def parar(self):
        print("Parando")
        pass
    def __str__(self):
        return f"{self.__class__.__name__} = {', '.join([f'{chave}={valor}' for chave, valor in self.__dict__.items()])}"
        #representa as classes

def main():
    bici = bicicleta(modelo="monarl", cor="vermelha", ano="1998", valor=560)
    print(bici)
    bici.buzinar()
    bici.correr()
    bici.parar()

main()