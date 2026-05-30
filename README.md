# Projeto de Vigilância de Partições Retangulares

## Grupo
* Beatriz Castro
* Joana Ferreira
* Mariana Bissacot

---

## Descrição do Problema
O problema consiste em determinar o **número mínimo de guardas necessários**, posicionados exclusivamente nos vértices únicos da partição, de forma a que cada retângulo seja vigiado por pelo menos um guarda. 

Este desafio foi modelado matematicamente como uma instância específica do problema de **Cobertura de Conjuntos (Set Cover)**, adaptada para uma estrutura geométrica de retângulos e vértices: 
* **Variáveis de Decisão:** $x_i \in \{0,1\}$ (1 se um guarda for colocado no vértice único $v_i$, 0 caso contrário).
* **Função Objetivo:** Minimizar $Z = \sum_{i=1}^{n} x_i$.
* **Restrições:** $\sum_{i \in Adj(r_j)} x_i \ge 1$ para cada retângulo $r_j$.

---

## Algoritmos Implementados

O projeto explora o problema através de três lentes algorítmicas distintas:

### 1. Satisfação de Restrições (CSP Imperativo) — `solver_mac.py`
Desenvolvido em Python, este solver foca-se em algoritmos de satisfação de restrições (CSP):
* **Generalized Arc Consistency (GAC):** Algoritmo de propagação de restrições n-árias usado para deduzir valores obrigatórios e podar a árvore antes de novas ramificações.
* **Degree Heuristic (Maior Grau):** Heurística de ordenação baseada na incidência dos vértices para acelerar a convergência.

### 2. Abordagens Heurísticas (Greedy) e Programação Dinâmica
Procuram o compromisso entre tempo de computação e otimalidade:
* **Greedy por Inserção (Maior Cobertura):** Abordagem progressiva que escolhe o vértice que vigia o maior número de retângulos ainda sem cobertura.
* **Greedy por Remoção (Reverse Greedy):** Abordagem inversa que inicia com guardas em todos os vértices e remove sequencialmente os redundantes.
* **Programação Dinâmica (Bitmasking):** Resolução exata baseada na Equação de Bellman para subproblemas de tamanho reduzido.

### 3. Programação em Lógica (Prolog)
Modelação declarativa focada na definição de relações lógicas e restrições de soma:
* **Extensão 4a (Restrições de Cores):** Garante que os guardas no mesmo retângulo possuam cores distintas usando a restrição `all_distinct`.
* **Extensão 4b (Alcance de Distância $D$):** Pré-calcula a adjacência de vértices para transformar o problema numa estrutura de grafo de dominância.

---

## Resultados Experimentais

Os resultados demonstram o impacto da explosão combinatória e o compromisso entre eficiência e otimalidade face ao solver comercial **Google OR-Tools (SCIP)**:

| Instância | Vértices Únicos | Ótimo (OR-Tools) | Melhor Manual (MAC) | Greedy (Inserção) | Tempo Greedy | Nós (Greedy/PD) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **parts40** | 82 | **14** | 15 | 17 | 0.00032s | 0 (Sem Nó) |
| **step50** | 102 | **17** | 18 | 22 | 0.00049s | 0 (Sem Nó) |

---

## Como Executar

### Pré-requisitos
* Python 3.x 
* Interpretador SWI-Prolog (para os ficheiros declarativos) 
* Google OR-Tools (opcional, para validação da baseline) 

### Executar o Solver Manual (CSP/GAC)
```bash
python solver_mac.py