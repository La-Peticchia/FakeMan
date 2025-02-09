
%Euristica: distanza Manhattan
heuristic(X1/Y1, X2/Y2, H) :-
    H is abs(X1 - X2) + abs(Y1 - Y2).

% Trova la prima mossa valida con A*
a_star_prima_mossa(Start, Goal, NextMove) :-
    a_star_search_prima_mossa([node(Start, 0, 0, [])], [], Goal, _, [NextMove|_]).

a_star_costo(Start, Goal, C) :-
    a_star_search_prima_mossa([node(Start, 0, 0, [])], [], Goal, C, _).

a_star_percorso(Start, Goal, Path):-
    a_star_search_prima_mossa([node(Start, 0, 0, [])], [], Goal,_, Path).



% Modifica l'algoritmo A* per fermarsi al primo passo
a_star_search_prima_mossa([node(Pos, C, _, Path)|_], _, Pos, C, TotPath) :-
    reverse([Pos|Path], [_|TotPath]).

a_star_search_prima_mossa([node(Pos, G, _, Path)|Open], Closed, Goal, C, TotPath) :-
    findall(
        node(Next, GNew, F, [Pos|Path]),
        (   adiacente(Pos, Next, 1),        % Trova i vicini
            \+ member(node(Next, _, _, _), Closed), % Non deve essere nei chiusi
            \+ member(node(Next, _, _, _), Open),   % Non deve essere negli aperti
            GNew is G + 1,                          % Incrementa il costo
            heuristic(Next, Goal, H),               % Calcola l'euristica
            F is GNew + H                           % Calcola il costo totale
        ),
        Neighbors
    ), 
    append(Open, Neighbors, NewOpen),
    sort(2, @=<, NewOpen, SortedOpen), % Ordina per F (minore � meglio)
    a_star_search_prima_mossa(SortedOpen, [node(Pos, G, _, Path)|Closed], Goal, C, TotPath), writeln("AAAA").


% Adiacenze
adiacente(X/Y, X1/Y, 1) :- X1 is X + 1, p(X1/Y).
adiacente(X/Y, X/Y1, 1) :- Y1 is Y + 1, p(X/Y1).
adiacente(X/Y, X1/Y, 1) :- X1 is X - 1, p(X1/Y).
adiacente(X/Y, X/Y1, 1) :- Y1 is Y - 1, p(X/Y1).


