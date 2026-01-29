## AGENTES-REATIVOS-SIMPLES-E-BASEADOS-EM-MODELOS

Neste repositório, foram implementadas versões simples de dois tipos de agentes inteligentes: um **reativo simples** e um **reativo baseado em modelo**.

De acordo com **Russell e Norvig (2022)**:

* **Agente Reativo Simples:** Tem o papel de `INTERPRETAR-ENTRADA`, que gera uma descrição abstrata do estado atual a partir da percepção. A função `REGRA-CORRESPONDENTE` retorna a primeira regra no conjunto de regras que corresponde à descrição de estado dada. Ele funciona por meio de ação-reação imediata, indo da percepção à atuação de maneira quase instantânea.
* *Exemplo no código:* Um robô aspirador que apenas percebe o ambiente e o limpa caso seus sensores indiquem sujeira.


* **Agente Baseado em Modelo:** Mantém um **estado interno** (memória) sobre o ambiente percebido. Isso evita problemas de loops infinitos e facilita a tomada de decisão quando a percepção atual não é suficiente.
* *Exemplo no código:* Um aspirador de pó robô que armazena um estado interno indicando as salas que já foram limpas, encerrando seu funcionamento apenas quando todo o domínio em sua memória apresenta a característica "limpo".



---

## ALGORITMO-DE-BUSCA-CEGA-DIJKSTRA

O método de busca de **Dijkstra** funciona como um algoritmo de busca cega (ou de custo uniforme) em que não se tem conhecimento prévio do domínio, mas o caminho percorrido é importante. É uma solução eficaz para problemas como:

* Escolha de rotas;
* Torre de Hanói;
* Labirintos.

O sistema utiliza uma estrutura de árvore onde cada nó representa um estado. A cada instante, verifica-se se determinado nó é o objetivo; se confirmado, o código retorna o nó. Caso contrário, a árvore é expandida e a busca continua no próximo nível. Esse método possui um custo de deslocamento para cada nó. Quando o custo é unitário (como no caso do labirinto), o algoritmo se assemelha à busca em largura, distinguindo-se pela lógica de **custo uniforme**.

---