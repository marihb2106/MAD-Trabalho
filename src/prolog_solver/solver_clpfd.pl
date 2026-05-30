:- use_module(library(clpfd)).

:- discontiguous retangulo/3.
:- discontiguous num_vars/2.
:- discontiguous aplicar_restricoes/2.
:- discontiguous extrair_vars/3.

:- consult('dados_parts40.pl'). 

% Modelo Principal
resolver_base(ID_Instancia) :-
    num_vars(ID_Instancia, TotalVars),
    findall(Vertices, retangulo(ID_Instancia, _IdRetangulo, Vertices), ListaDeRetangulos),
    
    length(Vars, TotalVars),
    Vars ins 0..1,
    
    aplicar_restricoes(ListaDeRetangulos, Vars),
    
    % Soma manual robusta para evitar os erros de domínio do compilador
    soma_vars(Vars, SomaTotal),
    
    % O motor com a heurística First-Fail Constrained e Bisect
    labeling([ffc, bisect, min(SomaTotal)], Vars),
    
    format('--- Instância ~d ---~n', [ID_Instancia]),
    format('Guardas Necessários (Ótimo): ~d~n~n', [SomaTotal]).

% ---------------------------------------------------------
% Predicados Auxiliares
% ---------------------------------------------------------

% A nossa função de soma manual que o Prolog adora
soma_vars([], 0).
soma_vars([H|T], S) :- 
    soma_vars(T, S1), 
    S #= H + S1.

% Lógica de cobertura dos retângulos
aplicar_restricoes([], _).
aplicar_restricoes([VerticesRetangulo | Resto], VarsGlobais) :-
    extrair_vars(VerticesRetangulo, VarsGlobais, VarsDoRetangulo),
    sum(VarsDoRetangulo, #>=, 1),
    aplicar_restricoes(Resto, VarsGlobais).

% Extrair variáveis da lista global com base nos IDs
extrair_vars([], _, []).
extrair_vars([IDVertice | RestoIDs], VarsGlobais, [Var | RestoVars]) :-
    nth1(IDVertice, VarsGlobais, Var),
    extrair_vars(RestoIDs, VarsGlobais, RestoVars).