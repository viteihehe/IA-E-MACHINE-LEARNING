
---

# 🧠 Anotações Corrigidas: Perceptron e Redes Neurais

As **Redes Neurais Artificiais (RNA)** são modelos de aprendizado **supervisionado** (em sua maioria) inspirados na estrutura biológica do cérebro. O Perceptron é a forma mais elementar dessas redes.

## 1. O Perceptron (Single-Layer)

O Perceptron é um **classificador linear binário**. Ele é conceitualmente focado em problemas **linearmente separáveis** (onde uma linha reta pode dividir as classes). Se o problema não for linear (como o problema do XOR), um único Perceptron não consegue resolvê-lo.

### Estrutura do Modelo

* **Entradas ():** As características (*features*) dos dados.
* **Pesos ():** Valores que ponderam a importância de cada entrada.
* **Bias ():** Um termo extra que permite deslocar a função de ativação para cima ou para baixo, garantindo que o neurônio possa aprender mesmo quando as entradas são zero.
* **Junção Sumadora:** Realiza o cálculo: .

---

## 2. Funções de Ativação

A função de ativação decide a saída do neurônio com base no resultado da soma.

* **Degrau (Step Function):** Saída determinística entre 0 ou 1.
* `if soma >= 0: return 1 else: return 0`


* **Tangente Hiperbólica (tanh):** Escala a saída entre -1 e 1. Embora seja mais robusta, no Perceptron de camada única ela ainda só resolve divisões lineares.



---

## 3. O Processo de Aprendizado

Diferente do que se pensa, o Perceptron é **determinístico**: para o mesmo peso e entrada, a saída nunca muda. O "caos" aparente vem da inicialização aleatória dos pesos.

1. **Predição:** O dado entra, a soma é feita e a função de ativação gera um resultado.
2. **Cálculo do Erro:** Comparação com o "Oráculo" (valor real).
* 


3. **Regra Delta (Ajuste):** Os pesos são atualizados proporcionalmente ao erro e à taxa de aprendizado ():
* 


4. **Época:** Uma passagem completa por todo o conjunto de dados.

---

## 4. Diferenças Cruciais de Arquitetura

| Característica | Perceptron Simples | Multi-Layer Perceptron (MLP) |
| --- | --- | --- |
| **Camadas** | Apenas Entrada e Saída | Entrada, Camadas Ocultas e Saída |
| **Problemas** | Apenas Linearmente Separáveis | Problemas Não-Lineares Complexos |
| **Algoritmo** | Regra Delta | **Backpropagation** |

> **Nota:** O **Backpropagation** é o algoritmo que permite o erro "voltar" através das camadas ocultas para ajustar pesos que não estão conectados diretamente à saída.

---

## 5. Implementação (Python)

```python
class Perceptron:
    def __init__(self, taxa_aprendizado=0.1, epocas=100):
        self._taxa = taxa_aprendizado
        self._epocas = epocas
        self.pesos = None
        self.bias = 0.0

    def ativador(self, soma):
        return 1 if soma >= 0 else 0

    def treinar(self, X, y):
        # Inicializa pesos com zero ou valores aleatórios pequenos
        self.pesos = [0.0] * len(X[0])
        
        for _ in range(self._epocas):
            erros_na_epoca = 0
            for xi, target in zip(X, y):
                # Soma ponderada: sum(w * x) + b
                soma_ponderada = sum(w * x for w, x in zip(self.pesos, xi)) + self.bias
                previsao = self.ativador(soma_ponderada)
                
                erro = target - previsao
                if erro != 0:
                    # Atualização dos pesos e bias (Regra Delta)
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self._taxa * erro * xi[i]
                    self.bias += self._taxa * erro
                    erros_na_epoca += 1
            
            if erros_na_epoca == 0:
                break # Convergência atingida

```

---
