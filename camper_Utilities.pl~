
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
    length(List, L),
    random(0,L,Index),
    elementAtIndex(Index, List, RandomPos).

seek(_,Pos, Pos).

seek(Dir, Pos1, Pos2):-
asdw(Dir, Pos1, NextPos),
seek(Dir,NextPos, Pos2).





