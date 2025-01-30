%Position Layout: [Round, Depth, P1Pos, P2Pos, State, BallPositions]
:-[payoff].

payoff([@p2, Depth, _, _, gameOver, []], Val) :- Val is Depth - 100.

payoff([@p1, Depth, _, _, gameOver, BallList], Val):- BallList \= [], Val is 100 - Depth.

/*
payoff([@p2, P1Pos, P2Pos, play, BallList], Val) :-
    distanza_manhattan_norm(P1Pos,P2Pos,D),
    distanza_giocatore_pallino(P1Pos, BallList, _, D1),
    Val is - (D + (1 - D1)).

payoff([@p1, P1Pos, P2Pos, play, BallList], Val) :-
    distanza_manhattan_norm(P1Pos,P2Pos,D),
    distanza_nemico_pallino(P2Pos, P1Pos, BallList, D1),
    Val is 2 - (D + D1).
*/

/*
payoff([_, _, P1Pos, P2Pos, play, BallList], Val) :-
    distanza_manhattan_norm(P1Pos,P2Pos,D),
    distanza_giocatore_pallino(P1Pos, BallList, _, D1),
    distanza_nemico_pallino(P2Pos, P1Pos, BallList, D2),
    %Val is 2 - (D + D2),
    %Val is 1 - D + (1 - D2)/2,
    Val is - D - D2/2 + D1.
*/

%List Mode
payoff([_,_, P1Pos, P2List,play, BallList], Val):-
    sort_list_by_distance(P1Pos, P2List, [Follower|Campers]),
    follower_Payoff(P1Pos,Follower,Val1),
    campers_Payoff(P1Pos,Campers,BallList,Val2),
    Val is Val1 + Val2.

mossa([@p1, Depth, P1Pos, P2Pos, play, BallList], [@p2, NewDepth, NextP1Pos, P2Pos, NewState, NewBallList]):-
    NewDepth is Depth + 1,
    adiacent(P1Pos, NextP1Pos),
    delete(BallList,NextP1Pos,NewBallList),
    (NewBallList = [] -> NewState = gameOver, !;  NewState = play).
/*
mossa([@p2, Depth, P1Pos, P2Pos, play, BallList], [@p1, NewDepth, P1Pos, NextP2Pos, gameOver, BallList]):-
    NewDepth is Depth + 1,
    adiacent(P2Pos, NextP2Pos),
    P1Pos = NextP2Pos, !.

mossa([@p2, Depth, P1Pos, P2Pos, play, BallList], [@p1, NewDepth, P1Pos, NextP2Pos, play, BallList]):-
    NewDepth is Depth + 1,
    adiacent(P2Pos, NextP2Pos).
*/

%ListMode
mossa([@p2, Depth, P1Pos, P2List, play, BallList], [@p1, NewDepth, P1Pos, NextP2List, NewState, BallList]):-
    NewDepth is Depth + 1,
    check_list_adiacent(P2List, NextP2List),
    sort(NextP2List, Sorted),
    length(NextP2List, L),
    length(Sorted, L1),
    L = L1,
    (member(P1Pos, NextP2List) -> NewState = gameOver, !; NewState = play).


tocca_a_MIN([@p1,_, _, _, _, _]).

tocca_a_MAX([@p2,_, _, _, _, _]).

adiacent(X1/Y,X2/Y) :- X2 is X1 + 1, pInv(X2/Y). % verso EST
adiacent(X/Y1,X/Y2) :- Y2 is Y1 - 1, pInv(X/Y2). % verso SUD
adiacent(X1/Y,X2/Y) :- X2 is X1 - 1, pInv(X2/Y). % verso OVEST
adiacent(X/Y1,X/Y2) :- Y2 is Y1 + 1, pInv(X/Y2). % verso NORD

check_list_adiacent1([], _):- false.
check_list_adiacent1([H|T], Pos) :-
    adiacent(H, Pos);
    check_list_adiacent1(T, Pos).

check_list_adiacent([], []).
check_list_adiacent([H|T], [NextH|NextT]):-
    adiacent(H,NextH),
    check_list_adiacent(T,NextT).



