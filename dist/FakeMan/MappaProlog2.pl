pInv(X/Y) :- p(Y/X).

p(0/Y) :- member(Y, [1, 2, 3, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]).

p(1/Y) :- member(Y, [1, 3, 5, 10, 16, 18, 19]).

p(2/Y) :- member(Y, [3, 5, 6, 7, 9, 10, 12, 13, 14, 15, 16, 18, 19]).

p(3/Y) :- member(Y, [1, 3, 5, 7, 12, 13, 14, 15, 16, 17, 18, 19]).

p(4/Y) :- member(Y, [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 15, 18, 19]).

p(5/Y) :- member(Y, [1, 13, 15, 16, 18, 19]).

p(6/Y) :- member(Y, [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 13, 14, 15, 18]).

p(7/Y) :- member(Y, [3, 5, 6, 7, 11, 12, 13, 14, 15, 17, 18]).

p(8/Y) :- member(Y, [1, 3, 7, 8, 9, 17, 18]).

p(9/Y) :- member(Y, [1, 3, 5, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19]).

p(10/Y) :- member(Y, [1, 3, 5, 6, 7, 9, 11, 12, 13, 14, 17, 18, 19]).

p(11/Y) :- member(Y, [1, 2, 3, 4, 5, 7, 9, 11, 14, 15, 16, 17, 18, 19]).

p(12/Y) :- member(Y, [3, 7, 9, 11, 12, 13, 14, 15, 16, 17]).

p(13/Y) :- member(Y, [0, 1, 2, 3, 5, 7, 9, 10, 11, 12, 13, 14, 17, 18, 19]).

p(14/Y) :- member(Y, [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]).

