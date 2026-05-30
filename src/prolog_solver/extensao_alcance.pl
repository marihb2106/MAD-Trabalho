% Exemplo de factos pré-calculados para Alcance D=1
% O retângulo 1 agora é coberto pelos vértices [1,2,3] ORIGINAIS + vizinhos
% Supondo que 4 é vizinho de 3, a lista expandida seria:
retangulo_alcance_d1(998, 1, [1, 2, 3, 4]). 
retangulo_alcance_d1(998, 2, [3, 4, 5, 2]).

% Predicado principal adaptado
resolver_alcance(ID_Instancia) :-
    num_vars(ID_Instancia, TotalVars),
    % Usamos os factos pré-expandidos
    findall(Vertices, retangulo_alcance_d1(ID_Instancia, _Id, Vertices), Lista),
    
    length(Vars, TotalVars),
    Vars ins 0..1,
    
    % A lógica de cobertura é idêntica, o que muda é a entrada!
    aplicar_cobertura(Lista, Vars),
    
    soma_vars(Vars, TotalGuardas),
    labeling([ffc, min(TotalGuardas)], Vars),
    format('Guardas com alcance D=1: ~d~n', [TotalGuardas]).