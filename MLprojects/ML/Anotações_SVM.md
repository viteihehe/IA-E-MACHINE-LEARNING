## ALGORITMO-DE-ML-SVM

O algoritmo **SVM (Support Vector Machine)** é um método de **Aprendizado Supervisionado** utilizado tanto para **classificação** quanto para **regressão**. Seu objetivo principal é encontrar uma **fronteira de decisão ótima** que separe os dados de diferentes classes com a **maior margem possível**.

De acordo com **Russell e Norvig (2022)** e **Bishop (2006)**, a SVM busca maximizar a distância entre os pontos mais próximos de cada classe — chamados de **vetores de suporte** — e o hiperplano de separação.

---

### 🔹 Conceitos Fundamentais

* **Hiperplano:**  
  Em um espaço bidimensional, é uma reta; em dimensões maiores, trata-se de uma superfície que separa os dados.

* **Margem Máxima:**  
  A SVM escolhe o hiperplano que maximiza a distância mínima entre ele e os vetores de suporte.

* **Vetores de Suporte:**  
  São os exemplos de treino mais próximos da fronteira de decisão. Apenas eles influenciam diretamente o modelo final.

---

### 🔹 Classificação Linear

Quando os dados são **linearmente separáveis**, a SVM encontra um hiperplano que satisfaz:

- W . x + b = 0 

Onde:
- `w` é o vetor normal ao hiperplano  
- `b` é o termo de bias  
- `x` representa os dados de entrada  

A decisão da classe é dada pelo **sinal da função**:

* valor positivo → classe A  
* valor negativo → classe B  

---

### 🔹 Classificação Não Linear e Kernel Trick

Quando os dados **não são linearmente separáveis**, a SVM utiliza o **Kernel Trick**, que projeta os dados para um espaço de maior dimensão, onde a separação linear se torna possível.

Kernels comumente utilizados:
* **Linear**
* **Polinomial**
* **RBF (Gaussian Kernel)**
* **Sigmoid**

Essa técnica evita o cálculo explícito da projeção, reduzindo o custo computacional.

---

### 🔹 Parâmetros Importantes

* **C (Regularização):**  
  Controla o trade-off entre margem máxima e erro de classificação.
  - C alto → menos erros no treino (risco de overfitting)
  - C baixo → maior margem (melhor generalização)

* **Kernel:**  
  Define o tipo de fronteira de decisão utilizada.

* **Gamma (kernels não lineares):**  
  Controla a influência de um único exemplo de treino sobre o modelo.

---

### 🔹 Fluxo Geral do Algoritmo

1. **Divisão dos Dados:**  
   Normalmente utiliza-se o esquema **70/30** ou **80/20** (treino/teste).

2. **Normalização:**  
   Etapa fundamental, pois a SVM é sensível à escala dos dados.

3. **Treinamento:**  
   O algoritmo identifica os vetores de suporte e define o hiperplano ótimo.

4. **Predição:**  
   Novas amostras são classificadas com base na posição relativa ao hiperplano.

5. **Avaliação:**  
   Métricas comumente utilizadas:
   * Acurácia
   * Matriz de confusão
   * Erro médio (para regressão)

---

### 🔹 Observações Importantes

* A SVM apresenta excelente desempenho em **espaços de alta dimensão**.
* A escolha adequada do **kernel** e dos **hiperparâmetros** é essencial.
* Pode apresentar custo computacional elevado para grandes bases de dados.
