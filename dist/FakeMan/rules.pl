%Position Layout: [Round, Depth, P1Pos, P2Pos, State, BallPositions]
:-[payoff].

payoff([@p2, Depth, _, _, gameOver, []], Val) :- Val is Depth - 100.

payoff([@p1, Depth, _, _, gameOver, BallList], Val):- BallList \= [], Val is 100 - Depth.

%List Mode
payoff([_,_, P1Pos, P2List,play, BallList], Val):-
    sort_list_by_distance(P1Pos, P2List, [Follower|Campers]),

    %Solo distanza manhattan tra follower e giocatore
    follower_Payoff(P1Pos,Follower,Val1),

    %Distanza mahnattan tra nemico e pallino più vicino al giocatore e distanza manhattan tra giocatore e lo stesso pallino
    campers_Payoff(P1Pos,Campers,BallList,Val2),

    %Palline rimanenti
    length(BallList, L),
    Val3 is (L - 3) * 0.25,

    %Tiles raggiungibili dal giocatore
    %passable_tiles_payoff(P2List, P1Pos, Val4),

    Val is Val1 + Val2 + Val3 .

mossa([@p1, Depth, P1Pos, P2Pos, play, BallList], [@p2, NewDepth, NextP1Pos, P2Pos, NewState, NewBallList]):-
    NewDepth is Depth + 1,
    adiacent(P1Pos, NextP1Pos),
    delete(BallList,NextP1Pos,NewBallList),
    (NewBallList = [] -> NewState = gameOver, !;  NewState = play).

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

