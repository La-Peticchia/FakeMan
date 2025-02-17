:-use_module(library(pce)).
%:-[mappa_logica].
:-[mappa_grafica].
:-[rules].
:-[alphabeta].

:- dynamic playerPos/2.
:- dynamic ballPos/2.

play :-
    Window = @a,
    free_objects(Window),
    disegna_pianta(Window, "Test"),
    create_objects(Window),
    playerPos(@p1,P1Pos),
    findall(X/Y, (playerPos(Add, X/Y) , Add \= @p1), P2Pos),
    findall(X/Y, ballPos(_,X/Y), List),
    play(Window,[@p1, P1Pos, P2Pos, play, List]).

play(Window, [@p1, P1Pos, P2Pos, play, BallList]):-
    writeln("move"),
    read(Dir), nl,
    (
     asdw(Dir,P1Pos, NewP1Pos),
     movePlayer(Window, @p1, NewP1Pos),
     (
         ballPos(Ball, NewP1Pos) -> free(Ball);
         true
     ),
     delete(BallList, NewP1Pos, NewBallList),
    (
         NewBallList = [] -> writeln("You Win");
         play(Window,[@p2, NewP1Pos, P2Pos, play, NewBallList])
     )

    );
    (
     writeln("invalid movement"),
     play(Window, [@p1, P1Pos, P2Pos, play, BallList])

    ).

play(Window, [@p2, P1Pos, P2Pos, play, BallList]):-
    writeln("p2 turn"),
    bestMove([@p2, P1Pos, P2Pos, play, BallList], [_, _, NewP2Pos, _, _]),
    findall(Add, (playerPos(Add, _) , Add \= @p1), Enemies),
    moveEnemies(Window, Enemies, NewP2Pos),
    (
        check_list_adiacent1(NewP2Pos, P1Pos) -> writeln("You Lose"), true;
        play(Window,[@p1, P1Pos, NewP2Pos, play, BallList])
    ).

bestMove([Round, P1Pos, P2Pos, State, BallList], [NextRound, NextP1Pos, NextP2Pos, NextState, NextBallList]):-
    alfabeta([Round, 0, P1Pos, P2Pos, State, BallList], -100, 100,6, [NextRound,_, NextP1Pos, NextP2Pos, NextState, NextBallList], _).


moveEnemies(_, [], []).
moveEnemies(Window, [H|T], [H1|T1]):-
    movePlayer(Window, H, H1),
    moveEnemies(Window,T, T1).

movePlayer(Window, Player, X/Y):-
    PX is X*20+2.5, PY is Y*20+2.5,
    send(Window, display, Player, point(PX,PY)).


create_objects(Window) :-
    Player1 = @p1, X/Y = 1/1,
    assert(playerPos(Player1, X/Y)),
    new(Player1, box(15,15)),
    send(Player1, fill_pattern, colour(blue)),
    PX is X*20+2.5, PY is Y*20+2.5,
    send(Window, display,Player1, point(PX,PY)),

    spawnEnemies(Window, [19/14, 18/7, 0/13]),

    spawnBalls(Window, 3).


spawnBalls(_,0).
spawnBalls(Window, Count):-
    new(Ball, circle(10)),
    randomBallPos(X/Y),
    assert(ballPos(Ball,X/Y)),
    send(Ball, fill_pattern, colour(orange)),
    PX is X*20+5, PY is Y*20+5,
    send(Window, display,Ball, point(PX,PY)),

    NewCount is Count - 1,
    spawnBalls(Window, NewCount).

spawnEnemies(_, []).
spawnEnemies(Window, [X/Y|T]):-
    new(Enemy, box(15,15)),
    assert(playerPos(Enemy, X/Y)),
    send(Enemy, fill_pattern, colour(red)),
    PX is X*20+2.5, PY is Y*20+2.5,
    send(Window, display, Enemy, point(PX,PY)),
    spawnEnemies(Window, T).

free_objects(Window) :-
    free(Window),
    (playerPos(X,_),free(X), false;true),
    (ballPos(X,_), free(X), false;true),
    retractall(playerPos(_,_)),
    retractall(ballPos(_,_)).

randomBallPos(X/Y) :-
    findall(X1/Y1, pInv(X1/Y1), List),
    findall(X2/Y2, ballPos(_,X2/Y2),List1),
    findall(X3/Y3, playerPos(_,X3/Y3),List2),
    append(List1,List2,List3),
    sort(List3,List4),
    subtract(List,List4,List5),
    length(List5, L),
    random(0,L,Index),
    elementAtIndex(Index, List5, X/Y).

elementAtIndex(0, [H|_], H).
elementAtIndex(Index, [_|T], Element) :-
    NewIndex is Index - 1,
    elementAtIndex(NewIndex,T,Element).

asdw(d,X1/Y,X2/Y) :- X2 is X1 + 1, pInv(X2/Y). % verso EST
asdw(w,X/Y1,X/Y2) :- Y2 is Y1 - 1, pInv(X/Y2). % verso NORD
asdw(a,X1/Y,X2/Y) :- X2 is X1 - 1, pInv(X2/Y). % verso OVEST
asdw(s,X/Y1,X/Y2) :- Y2 is Y1 + 1, pInv(X/Y2). % verso SUD


