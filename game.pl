:-use_module(library(pce)).
:-[mappa_logica].
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
    playerPos(@p2,P2Pos),
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
    movePlayer(Window, @p2, NewP2Pos),
    (
        adiacent(P1Pos, NewP2Pos) -> writeln("You Lose"), true;
        play(Window,[@p1, P1Pos, NewP2Pos, play, BallList])
    ).

bestMove(CurrentPos, NextPos):-
    alfabeta(CurrentPos, -100, 100,3, NextPos, _).


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

    Player2 = @p2, X1/Y1 = 13/18,
    assert(playerPos(Player2, X1/Y1)),
    new(Player2, box(15,15)),
    send(Player2, fill_pattern, colour(red)),
    PX1 is X1*20+2.5, PY1 is Y1*20+2.5,
    send(Window, display,Player2, point(PX1,PY1)),

    spawnBalls(Window, 3).

/*
    Ball1 = @b1,
    new(Ball1, circle(10)),
    send(Ball1, fill_pattern, colour(orange)),
    ballPos(Ball1, X2/Y2),
    PX2 is X2*20+5, PY2 is Y2*20+5,
    send(Window, display,Ball1, point(PX2,PY2)),

    Ball2 = @b2,
    new(Ball2, circle(10)),
    send(Ball2, fill_pattern, colour(orange)),
    ballPos(Ball2, X3/Y3),
    PX3 is X3*20+5, PY3 is Y3*20+5,
    send(Window, display,Ball2, point(PX3,PY3)),

    Ball3 = @b3,
    new(Ball3, circle(10)),
    send(Ball3, fill_pattern, colour(orange)),
    ballPos(Ball3, X4/Y4),
    PX4 is X4*20+5, PY4 is Y4*20+5,
    send(Window, display,Ball3, point(PX4,PY4)).
*/

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

free_objects(Window) :-
    free(Window),
    (playerPos(X,_),free(X), false;true),
    (ballPos(X,_), free(X), false;true),
    retractall(playerPos(_,_)),
    retractall(ballPos(_,_)).

randomBallPos(X/Y) :-
    findall(X1/Y1, l(X1/Y1,_), List),
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

asdw(d,X1/Y,X2/Y) :- X2 is X1 + 1, l(X2/Y,_). % verso EST
asdw(w,X/Y1,X/Y2) :- Y2 is Y1 - 1, l(X/Y2,_). % verso NORD
asdw(a,X1/Y,X2/Y) :- X2 is X1 - 1, l(X2/Y,_). % verso OVEST
asdw(s,X/Y1,X/Y2) :- Y2 is Y1 + 1, l(X/Y2,_). % verso SUD

