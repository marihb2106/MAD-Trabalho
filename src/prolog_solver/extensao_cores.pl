:- use_module(library(clpfd)).

:- discontiguous retangulo/3.
:- discontiguous num_vars/2.
:- discontiguous aplicar_cobertura/2.
:- discontiguous aplicar_cores_distintas/2.
:- discontiguous extrair_vars/3.
:- discontiguous cores_diferentes/1.
:- discontiguous restringir_cor_pares/2.

:- consult('dados_parts40.pl'). 

% Modelo Principal para a Extensão de Cores
resolver_cores(ID_Instancia, MaxCores) :-
    num_vars(ID_Instancia, TotalVars),
    findall(Vertices, retangulo(ID_Instancia, _IdRetangulo, Vertices), ListaDeRetangulos),
    
    % 1. Variáveis de Guardas (0 ou 1)
    length(Guardas, TotalVars),
    Guardas ins 0..1,
    
    % 2. Variáveis de Cores (0 = sem guarda, 1..MaxCores)
    length(Cores, TotalVars),
    Cores ins 0..MaxCores,
    
    % 3. Ligar as variáveis: Cor = 0 se e só se Guarda = 0
    ligar_guardas_cores(Guardas, Cores),
    
    % 4. Restrição de Cobertura Base
    aplicar_cobertura(ListaDeRetangulos, Guardas),
    
    % 5. Restrição da Extensão: Cores distintas no mesmo retângulo
    aplicar_cores_distintas(ListaDeRetangulos, Cores),
    
    % 6. Otimização: Minimizar a maior cor usada (e o número de guardas)
    max_member(MaiorCor, Cores),
    soma_vars(Guardas, TotalGuardas),
    
    % Pesquisa
    % Otimização Lexicográfica: Primeiro minimiza o nº de guardas, depois a cor
    append(Guardas, Cores, TodasVars),
    % Otimização: Minimizar guardas, e para as cores, obrigar a serem >= 1
    labeling([ffc, min(TotalGuardas), min(MaiorCor)], TodasVars),
    
    % Imprime a lista de cores para debug
    format('--- Extensao 4a (Cores): Instancia ~d ---~n', [ID_Instancia]),
    format('Guardas Utilizados: ~d~n', [TotalGuardas]),
    format('Cores Atribuidas: ~w~n', [Cores]),  % ~w imprime listas
    format('Cores Necessarias (Minimo): ~d~n~n', [MaiorCor]).

% ---------------------------------------------------------
% Predicados Auxiliares e Restrições
% ---------------------------------------------------------

soma_vars([], 0).
soma_vars([H|T], S) :- soma_vars(T, S1), S #= H + S1.

ligar_guardas_cores([], []).
ligar_guardas_cores([G|Gs], [C|Cs]) :-
    G #= 1 #==> C in 1..5, % Se há guarda, a cor é OBRIGATORIAMENTE entre 1 e 5
    G #= 0 #==> C #= 0,     % Se não há, é 0
    ligar_guardas_cores(Gs, Cs).

aplicar_cobertura([], _).
aplicar_cobertura([VerticesRetangulo | Resto], GuardasGlobais) :-
    extrair_vars(VerticesRetangulo, GuardasGlobais, GuardasDoRetangulo),
    sum(GuardasDoRetangulo, #>=, 1),
    aplicar_cobertura(Resto, GuardasGlobais).

aplicar_cores_distintas([], _).
aplicar_cores_distintas([VerticesRetangulo | Resto], CoresGlobais) :-
    extrair_vars(VerticesRetangulo, CoresGlobais, CoresDoRetangulo),
    cores_diferentes(CoresDoRetangulo),
    aplicar_cores_distintas(Resto, CoresGlobais).

% Garante que num grupo, as cores válidas (>0) não se repetem
cores_diferentes([]).
cores_diferentes([C1|Resto]) :-
    restringir_cor_pares(C1, Resto),
    cores_diferentes(Resto).

restringir_cor_pares(_, []).
restringir_cor_pares(C1, [C2|Resto]) :-
    % A beleza declarativa: Se ambos têm guarda, as cores têm de ser diferentes
    (C1 #> 0 #/\ C2 #> 0) #==> (C1 #\= C2),
    restringir_cor_pares(C1, Resto).

extrair_vars([], _, []).
extrair_vars([IDVertice | RestoIDs], VarsGlobais, [Var | RestoVars]) :-
    nth1(IDVertice, VarsGlobais, Var),
    extrair_vars(RestoIDs, VarsGlobais, RestoVars).