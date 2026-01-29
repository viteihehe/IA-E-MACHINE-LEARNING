## ALGORITMO-DE-ML-KNN

O algoritmo **KNN** (*K-Nearest Neighbors*) opera por meio de **Aprendizado Supervisionado**. É uma técnica de aprendizagem por memorização (sem generalização prévia), utilizada para classificação e regressão, retornando valores determinísticos.

### Estrutura do Modelo:

* **Divisão de Dados:** Geralmente utiliza-se o sistema **70/30** (70% das instâncias para treinamento e 30% para teste).
* **Objetivo:** Classificar objetos com base nos exemplos de treinamento mais próximos em termos de características.
* **Regressão:** Caso seja usado para regressão, o valor de saída é baseado na média dos valores dos vizinhos mais próximos.

### Criação e Funcionamento:

1. **Dados Rotulados:** Necessita de uma base de dados previamente classificada.
2. **Métrica de Distância:** Define-se uma métrica para calcular a proximidade, geralmente a **Distância Euclidiana**:



Ou a **Distância de Manhattan** (soma das diferenças absolutas).
3. **Definição de K:** Escolha do número de vizinhos (preferencialmente ímpares para evitar empates).
4. **Votação:** O rótulo do novo dado é determinado pela maioria entre os vizinhos mais próximos ou decisão aleatória em caso de empate técnico.

---
