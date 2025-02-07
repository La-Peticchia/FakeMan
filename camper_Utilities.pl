:-[fakeman].
:-[movimentopupi2].

:- dynamic enemyTarget/3.


sort_by_distance(Pos1, List, OutList):-
    findall((Dist, Pos), (member(Pos,List), a_star_costo(Pos1, Pos, Dist)), List1),
    sort(List1,List2),
    
    findall(Pos2, member((_,Pos2), List2), OutList).

next_camper_target(CamperPos, BallList, Target):-
    
    %(seek(_,CamperPos,PlayerPos), Target = PlayerPos);

    (enemyTarget(CamperPos, n/a, _),
     findall(Pos, (member(Pos,BallList), \+enemyTarget(_,Pos,_)), FreeBalls),
     (FreeBalls = [] -> sort_by_distance(CamperPos, BallList, [NearestBall|_]);  
     sort_by_distance(CamperPos, FreeBalls, [NearestBall|_])),
     Target = NearestBall); 
     

    (enemyTarget(CamperPos,CamperPos, _), Target = n/a);
    
    enemyTarget(CamperPos, Target, _).

get_target_path(CamperPos, NewTarget, Path):-
    (enemyTarget(CamperPos, NewTarget, Path), member(NewTarget, Path));

    (NewTarget = n/a -> get_random_adiacent_pos(CamperPos, Path);
     a_star_percorso(CamperPos, NewTarget, Path)).


get_random_adiacent_pos(Pos, [RandomPos]):-
    findall(Pos1, adiacente(Pos,Pos1,_), List),
    random_member(RandomPos, List).

seek(_,Pos, Pos).

seek(Dir, Pos1, Pos2):-
asdw(Dir, Pos1, NextPos),
seek(Dir,NextPos, Pos2).


move_campers([],_,_,[]).

move_campers([H|T], P1Pos, BallList, [H1| T1]):-
    move_camper(H, P1Pos, BallList, H1),
    move_campers(T, P1Pos, BallList, T1).


move_camper(CamperPos,PlayerPos, BallList, NextPos):-
    ( \+enemyTarget(CamperPos,_,_) -> assert(enemyTarget(CamperPos , n/a, [])); true),
    next_camper_target(CamperPos,BallList,Target),
    get_target_path(CamperPos,Target, [NextPos|NextPath]), 
    (seek(_,NextPos,PlayerPos), NextTarget = PlayerPos ;NextTarget = Target),
    retractall(enemyTarget(CamperPos,_,_)),
    assert(enemyTarget(NextPos, NextTarget, NextPath)),
    findall(Pos, enemyTarget(Pos,_,_), List),
    length(List, X).


asdw(s,X1/Y,X2/Y) :- X2 is X1 + 1, p(X2/Y). % verso SUD
asdw(a,X/Y1,X/Y2) :- Y2 is Y1 - 1, p(X/Y2). % verso OVEST
asdw(w,X1/Y,X2/Y) :- X2 is X1 - 1, p(X2/Y). % verso NORD
asdw(d,X/Y1,X/Y2) :- Y2 is Y1 + 1, p(X/Y2). % verso EST



