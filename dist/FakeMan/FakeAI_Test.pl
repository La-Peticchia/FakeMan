:-use_module(library(pce)).
%:- [mappa].
:- [fakeman].
:- [mappa_grafica].
:- [movimentopupi2].
:- [camper_utilities].
:- [follower_utilities].

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
    play(Window, [@p1, P1Pos, P2Pos, List]).

play(Window, [@p1, P1Pos, P2Pos, BallList]) :-
    writeln("move"),
    read(Dir), nl,
    (asdw(Dir,P1Pos, NewP1Pos),
    movePlayer(Window, @p1, NewP1Pos),
     (
         ballPos(Ball, NewP1Pos) -> free(Ball);
         true
     ),
     delete(BallList, NewP1Pos, NewBallList),
    (
         NewBallList = [] -> writeln("You Win");
         play(Window,[@p2, NewP1Pos, P2Pos, NewBallList])
     )
    );

    writeln("invalid movement"),
    play(Window,  [@p1, P1Pos, P2Pos, BallList]).

play(Window, [@p2, P1Pos, P2Pos, BallList]) :-
    writeln("p2 turn"),
    split_list(P2Pos, Followers, Campers),
    move_followers(Followers, P1Pos, NewFolPos),

    move_campers(Campers, P1Pos, BallList, NewCamPos),
    findall(Add, (playerPos(Add, _) , Add \= @p1), Enemies),
    append(NewFolPos, NewCamPos, NewP2Pos),
    moveEnemies(Window, Enemies, NewP2Pos),
    (
        check_list_adiacent(NewP2Pos, P1Pos) -> writeln("You Lose"), true;
        play(Window,[@p1, P1Pos, NewP2Pos, BallList])
    ).


moveEnemies(_, [], []).
moveEnemies(Window, [H|T], [H1|T1]):-
    movePlayer(Window, H, H1),
    moveEnemies(Window,T, T1).

movePlayer(Window, Player, Y/X):-
    PX is X*20+2.5, PY is Y*20+2.5,
    send(Window, display, Player, point(PX,PY)).


create_objects(Window) :-
    Player1 = @p1, X/Y = 1/1,
    assertz(playerPos(Player1, Y/X)),
    new(Player1, box(15,15)),
    send(Player1, fill_pattern, colour(blue)),
    PX is X*20+2.5, PY is Y*20+2.5,
    send(Window, display,Player1, point(PX,PY)),

    spawnEnemies(Window, [ 5/13, 14/12, 18/11, 18/7]),

    spawnBalls(Window, 3).


spawnBalls(_,0).
spawnBalls(Window, Count):-
    new(Ball, circle(10)),
    randomBallPos(X/Y),
    assert(ballPos(Ball,Y/X)),
    send(Ball, fill_pattern, colour(orange)),
    PX is X*20+5, PY is Y*20+5,
    send(Window, display,Ball, point(PX,PY)),

    NewCount is Count - 1,
    spawnBalls(Window, NewCount).

spawnEnemies(_, []).
spawnEnemies(Window, [X/Y|T]):-
    new(Enemy, box(15,15)),
    assert(playerPos(Enemy, Y/X)),
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

/*
asdw(d,X1/Y,X2/Y) :- X2 is X1 + 1, pInv(X2/Y). % verso EST
asdw(w,X/Y1,X/Y2) :- Y2 is Y1 - 1, pInv(X/Y2). % verso NORD
asdw(a,X1/Y,X2/Y) :- X2 is X1 - 1, pInv(X2/Y). % verso OVEST
asdw(s,X/Y1,X/Y2) :- Y2 is Y1 + 1, pInv(X/Y2). % verso SUD
*/


asdw(s,X1/Y,X2/Y) :- X2 is X1 + 1, p(X2/Y). % verso SUD
asdw(a,X/Y1,X/Y2) :- Y2 is Y1 - 1, p(X/Y2). % verso OVEST
asdw(w,X1/Y,X2/Y) :- X2 is X1 - 1, p(X2/Y). % verso NORD
asdw(d,X/Y1,X/Y2) :- Y2 is Y1 + 1, p(X/Y2). % verso EST

check_list_adiacent([], _):- false.
check_list_adiacent([H|T], Pos) :-
    adiacente(H, Pos, _);
    check_list_adiacent(T, Pos).

split_list(List, First, Second):-
    length(List, N),
    split(List, floor(N/2), First, Second).


split(T, 0, [], T).
split([H|T], N, [H1|T1], Second):-
    H1 = H,
    N1 is N - 1,
    split(T, N1, T1, Second).
