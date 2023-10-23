:- dynamic grandfather/2.
:- dynamic grandmother/2.
:- dynamic uncle/2.
:- dynamic aunt/2.
:- dynamic son/2.
:- dynamic daughter/2.
:- dynamic father/2.
:- dynamic mother/2.
:- dynamic brother/2.
:- dynamic sister/2.
:- dynamic siblings/2.
:- dynamic relatives/2.

parent(X, Y) :- father(X, Y).
parent(X, Y) :- mother(X, Y).
child(X, Y) :- parent(Y, X).
siblings(Person1, Person2) :- parent(X, Person1), parent(X, Person2), Person1 \= Person2.
siblings(Person1, Person2) :- brother(Person1, Person2). % the four lines are reflexive relationship for siblings
siblings(Person1, Person2) :- brother(Person2, Person1).
siblings(Person1, Person2) :- sister(Person1, Person2).
siblings(Person1, Person2) :- sister(Person2, Person1).

relatives(Person1, Person2) :- siblings(Person1, Person2).
relatives(Person1, Person2) :- parent(Person1, Person2).
relatives(Person1, Person2) :- parent(Person2, Person1).
relatives(Person1, Person2) :- child(Person1, Person2).
relatives(Person1, Person2) :- child(Person2, Person1).
