:- consult('dados_parts40.pl'). 

% Dois retângulos são vizinhos se partilham pelo menos um vértice
vizinho(R1, R2) :-
    retangulo(_, R1, V1),
    retangulo(_, R2, V2),
    R1 \= R2,
    member(V, V1),
    member(V, V2), !.

% Alcance D=0: Apenas o próprio retângulo
alcance(R, 0, [R]).

% Alcance D=1: Retângulo + Vizinhança direta
alcance(R, 1, Lista) :-
    findall(V, vizinho(R, V), Vizinhos),
    sort([R | Vizinhos], Lista).

% Teste prático:
% Se pedires 'testar(1).' o Prolog imprime os vizinhos do retângulo 1
testar(ID) :-
    format('--- Teste de Alcance (D=1) para Instancia ~d ---~n', [ID]),
    retangulo(ID, R, _),
    alcance(R, 1, Lista),
    format('Retangulo ~d tem vizinhos: ~w~n', [R, Lista]),
    fail.
testar(_).