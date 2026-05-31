====================================================================
Projeto de Vigilância de Partições Retangulares
====================================================================

GRUPO
--------------------------------------------------------------------
* Beatriz Castro (up202306399)
* Joana Ferreira (up202305202)
* Mariana Bissacot (up202306832)

ESTRUTURA DO DIRETÓRIO
--------------------------------------------------------------------
/ (Raiz)
|-- README.txt                 (Instruções de execução)
|-- relatorio.pdf   (Relatório final do projeto) -> NOTA: INSERIR AQUI
|
|-- data/
|   |-- examples/              (Instâncias de teste para os algoritmos)
|       |-- parts40
|       |-- step50
|
|-- src/
|-- generator/             (Código em C para geração de instâncias)
|-- greedy_solver/         (Heurísticas Greedy e Programação Dinâmica)
|-- manual_solver/         (Solver CSP imperativo com MAC/GAC)
|-- ortools_solver/        (Baseline ótimo utilizando Google OR-Tools)
|-- prolog_solver/         (Modelação declarativa pura e gerador de factos)

DESCRIÇÃO DO PROJETO
--------------------------------------------------------------------
Este projeto tem como objetivo otimizar os recursos necessários para 
a vigilância completa de uma área dividida geometricamente em 
retângulos. O foco principal é determinar o número mínimo de guardas 
que devem ser posicionados (exclusivamente nos vértices) para garantir 
que cada retângulo da partição seja vigiado por pelo menos um guarda.

Matematicamente, o problema foi modelado como uma instância do 
problema de Cobertura de Conjuntos (Set Cover), adaptada à estrutura 
geométrica proposta. A função objetivo visa minimizar o custo total 
(número de guardas): Minimizar Z = Sum(Xi).

ABORDAGENS IMPLEMENTADAS
--------------------------------------------------------------------
Para resolver o problema e comparar resultados, foram desenvolvidas 
quatro abordagens distintas:

1. Solver Manual (Python)
   - Focado em algoritmos de satisfação de restrições (CSP).
   - Utiliza o algoritmo Generalized Arc Consistency (GAC), uma 
     generalização do AC-3, para lidar com restrições n-árias.
   - Implementa a heurística de Maior Grau para acelerar a 
     convergência.

2. Heurísticas Gananciosas (Greedy)
   - Por Inserção (Maior Cobertura): Começa sem guardas e seleciona 
     iterativamente o vértice que vigia o maior número de retângulos 
     ainda descobertos.
   - Por Remoção (Reverse Greedy): Começa com guardas em todos os 
     vértices e remove iterativamente os guardas mais redundantes.

3. Programação Dinâmica
   - Modelação através de Bitmasking e da Equação de Bellman.
   - Exata e rápida para subproblemas pequenos, mas computacionalmente 
     inviável para partições completas devido à explosão combinatória.

4. Programação em Lógica (Prolog)
   - Abordagem declarativa utilizando 'clpfd' para modelar a restrição 
     de soma.
   - Usada estritamente para validação matemática do modelo em 
     instâncias miniatura e para o desenvolvimento de extensões.

EXTENSÕES E VARIANTES
--------------------------------------------------------------------
* Cobertura Parcial: As restrições aplicam-se apenas a um subconjunto 
  de retângulos. A redução de guardas não é linear face à fração de 
  retângulos obrigatórios.
* Guardas com Cores: Guardas no mesmo retângulo devem ter cores 
  distintas. O número de cores depende da geometria da solução.
* Guardas com Maior Alcance (D=1): Um guarda num vértice cobre também 
  os retângulos a uma distância 1. Reduz o número de guardas em 50% 
  a 75%.

FICHEIROS E INSTÂNCIAS DE REFERÊNCIA
--------------------------------------------------------------------
* solver_mac.py: Implementação do solver manual em Python.
* mini_A, mini_B, mini_C: Instâncias de validação.
* parts40: 100 instâncias aleatórias (40 retângulos e 82 vértices).
* step50: Instância complexa (50 retângulos e 102 vértices).