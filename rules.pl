%Position Layout: [Round, P1Pos, P2Pos, State, BallPositions]

payoff([@p1, _, _, gameOver, [_|_]], 100).

payoff([@p1, P1Pos, P2Pos, play, BallList], Val) :-
    distanza_manhattan_norm(P1Pos,P2Pos,D),
    distanza_player_pallino(P2Pos, BallList, D1),
    Val is 2 - (D + D1).

payoff([@p2, _, _, gameOver, []], -100).

payoff([@p2, P1Pos, P2Pos, play, BallList], Val) :-
    distanza_manhattan_norm(P1Pos,P2Pos,D),
    distanza_player_pallino(P1Pos, BallList, D1),
    Val is - (D + D1).

next_player(@p1,@p2).

next_player(@p2,@p1).

mossa([@p1, P1Pos, P2Pos, play, BallList], [@p2, NextP1Pos, P2Pos, NewState, NewBallList]):-
    adiacent(P1Pos, NextP1Pos),
    delete(BallList,NextP1Pos,NewBallList),
    (NewBallList = [] -> NewState = gameOver, !;  NewState = play).

mossa([@p2, P1Pos, P2Pos, play, BallList], [@p1, P1Pos, NextP2Pos, gameOver, BallList]):-
    adiacent(P2Pos, NextP2Pos),
    P1Pos = NextP2Pos, !.

mossa([@p2, P1Pos, P2Pos, play, BallList], [@p1, P1Pos, NextP2Pos, play, BallList]):-
    adiacent(P2Pos, NextP2Pos).


tocca_a_MIN([@p1, _, _, _, _]).

tocca_a_MAX([@p2, _, _, _, _]).

adiacent(X1/Y,X2/Y) :- X2 is X1 + 1, l(X2/Y,_). % verso EST
adiacent(X/Y1,X/Y2) :- Y2 is Y1 - 1, l(X/Y2,_). % verso SUD
adiacent(X1/Y,X2/Y) :- X2 is X1 - 1, l(X2/Y,_). % verso OVEST
adiacent(X/Y1,X/Y2) :- Y2 is Y1 + 1, l(X/Y2,_). % verso NORD

% Distanza Manhattan tra due punti
distanza_manhattan_norm(X1/Y1, X2/Y2, D) :-
    D is (abs(X1 - X2) + abs(Y1 - Y2)) / 38.

% Funzione di utilit�: distanza tra il nemico e il pallino pi� vicino
distanza_player_pallino(Pos, Pallini, DistanzaMinima) :-
    findall(Distanza, (member(Pallino, Pallini), distanza_manhattan_norm(Pos, Pallino, Distanza)), Distanze),%genera una lista di distanze tra il nemico e tutti i pallini
    min_list(Distanze, DistanzaMinima).%trova la distanza minima da quella lista, che rappresenta il pallino pi� vicino al nemico
