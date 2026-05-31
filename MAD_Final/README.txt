================================================================================
PROJETO DE VIGILÂNCIA DE PARTIÇÕES RETANGULARES - MAD 2025/2026
================================================================================

GRUPO: 
- Beatriz Castro (up202306399)
- Joana Ferreira (up202305202)
- Mariana Bissacot (up202306832)

--------------------------------------------------------------------------------
1. ESTRUTURA DO DIRETÓRIO
--------------------------------------------------------------------------------
.
|-- README.txt                 (Este ficheiro com instruções de execução)
|-- relatorio.pdf              (Relatório final do projeto)
|
|-- data/
|   |-- examples/              (Instâncias de teste)
|       |-- parts40
|       |-- step50
|
|-- src/
    |-- generator/             (Código em C para geração de instâncias)
    |-- greedy_solver/         (Heurísticas Greedy e Programação Dinâmica)
    |-- manual_solver/         (Solver CSP imperativo com MAC/GAC)
    |-- ortools_solver/        (Baseline ótimo utilizando Google OR-Tools)
    |-- prolog_solver/         (Modelação declarativa pura e extensões)

--------------------------------------------------------------------------------
2. INSTRUÇÕES DE EXECUÇÃO DOS PROGRAMAS
--------------------------------------------------------------------------------
PRÉ-REQUISITOS:
- Python 3.x
- Interpretador SWI-Prolog
- Biblioteca OR-Tools (para executar a baseline): pip install ortools

A. EXECUTAR O SOLVER MANUAL (MAC / GAC - Generalização AC-3)
Para correr o motor de restrições desenvolvido manualmente:
> python src/manual_solver/solver_mac.py --instance data/examples/step50

B. EXECUTAR OS ALGORITMOS GANANCIOSOS (Greedy / DP)
Para correr a abordagem heurística rápida ou a Programação Dinâmica:
> python src/greedy_solver/solver_greedy.py --instance data/examples/step50

C. EXECUTAR A BASELINE (Google OR-Tools - Cobertura Total e Parcial)
Para verificar o resultado ótimo utilizando a ferramenta comercial:
> python src/ortools_solver/solver_ortools.py --instance data/examples/step50

D. EXECUTAR A MODELAÇÃO DECLARATIVA E EXTENSÕES (Prolog)
Navegue para a pasta do Prolog e abra o interpretador:
> cd src/prolog_solver
> swipl

Dentro do interpretador, carregue o solver base e os dados (ex. parts40):
?- [solver_clpfd].
?- [dados_parts40].
?- resolver_instancia(Solucao).

Para testar as Extensões 4a (Cores) e 4b (Alcance D=1):
Carregue os respetivos ficheiros e execute os predicados de teste:
?- [extensao_cores].
?- [extensao_alcance].
?- [test_alcance].

--------------------------------------------------------------------------------
3. DESTAQUES DO MODELO
--------------------------------------------------------------------------------
Conforme detalhado no relatorio.pdf, este projeto implementa:
- Variante de Cobertura Parcial: Onde as restrições se aplicam apenas a um 
  subconjunto de retângulos (25%, 50%, 75%).
- GAC (Generalized Arc Consistency): Sendo o problema de Cobertura de Conjuntos
  baseado em restrições n-árias, o algoritmo AC-3 clássico foi generalizado.
- Extensões Lógicas: Otimização simultânea de guardas e cores, e expansão de
  vizinhança para alcance D=1.
================================================================================