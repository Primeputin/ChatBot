:- dynamic grandparent/2.
:- dynamic not_grandparent/2.

:- dynamic grandfather/2.
:- dynamic not_grandfather/2.

:- dynamic grandmother/2.
:- dynamic not_grandmother/2.

:- dynamic uncle/2.
:- dynamic not_uncle/2.

:- dynamic aunt/2.
:- dynamic not_aunt/2.

:- dynamic son/2.
:- dynamic not_son/2.

:- dynamic daughter/2.
:- dynamic not_daughter/2.

:- dynamic father/2.
:- dynamic not_father/2.

:- dynamic mother/2.
:- dynamic not_mother/2.

:- dynamic brother/2.
:- dynamic not_brother/2.

:- dynamic sister/2.
:- dynamic not_sister/2.

:- dynamic parent/2.
:- dynamic not_parent/2.

:- dynamic sibling/2.
:- dynamic not_sibling/2.

:- dynamic siblings/2.
:- dynamic not_siblings/2.

:- dynamic relatives/2.
:- dynamic not_relatives/2.

:- dynamic child_of/2.
:- dynamic not_child_of/2.

:- dynamic child/2.
:- dynamic not_child/2.

:- dynamic male/1.
:- dynamic not_male/1.

:- dynamic married/2.
:- dynamic not_married/2.

:- dynamic two_parents/1.
:- dynamic one_father/1.
:- dynamic one_mother/1.
:- dynamic two_grandparents/1.
:- dynamic one_grandfather/1.
:- dynamic one_grandmother/1.

:- dynamic descendant/2.

two_parents(Person) :-
    findall(Parent, parent(Parent, Person), Parents),
    length(Parents, NumParents),
    NumParents = 2.
one_father(Person) :-
    findall(Father, father(Father, Person), Fathers),
    length(Fathers, NumFather),
    NumFather = 1.
one_mother(Person) :-
    findall(Mother, mother(Mother, Person), Mothers),
    length(Mothers, NumMother),
    NumMother = 1.

two_grandparents(Person) :-
    findall(GrandParent, parent(GrandParent, Person), GrandParents),
    length(GrandParents, NumGrandParents),
    NumGrandParents = 2.
one_grandfather(Person) :-
    findall(GrandFather, father(GrandFather, Person), GrandFathers),
    length(GrandFathers, NumGrandFather),
    NumGrandFather = 1.
one_grandmother(Person) :-
    findall(GrandMother, mother(GrandMother, Person), GrandMothers),
    length(GrandMothers, NumGrandMother),
    NumGrandMother = 1.

child(X, Y) :- child_of(X, Y).
child(X, Y) :- parent(Y, X).
not_child_of(X, Y) :- X = Y.
not_child_of(X, Y) :- child_of(Y, X).
not_child_of(X, Y) :- parent(X, Y).
not_child_of(X, Y) :- siblings(X, Y).
not_child_of(X, Y) :- grandparent(X, Y), grandparent(Y, X).
not_child_of(X, Y) :- uncle(X, Y); uncle(Y, X).
not_child_of(X, Y) :- aunt(X, Y); aunt(Y, X).
not_child(X, Y) :- not_child_of(X, Y).

parent(X, Y) :- child_of(Y,X).
not_parent(X, Y) :- child(X, Y).
not_parent(X, Y) :- X = Y.
not_parent(X, Y) :- two_parents(Y), \+ parent(X, Y). % there could only be a max of two parents

not_father(X, Y) :- not_parent(X, Y).
not_father(X, _) :- not_male(X).
not_father(X, Y) :- one_father(Y), \+ father(X, Y). % max of one father
not_mother(X, Y) :- not_parent(X, Y).
not_mother(X, _) :- male(X).
not_mother(X, Y) :- one_mother(Y), \+ mother(X, Y). % max of one mother

son(X, Y) :- child(X, Y), male(X).
not_son(X, _) :- not_male(X).
not_son(X, Y) :- not_child(X, Y).
daughter(X, Y) :- child(X, Y), not_male(X).
not_daughter(X, _) :- male(X).
not_daughter(X, Y) :- not_child(X, Y).

siblings(Person1, Person2) :- sibling(Person1, Person2).
siblings(Person1, Person2) :- sibling(Person2, Person1).
siblings(Person1, Person2) :- parent(X, Person1), parent(X, Person2), Person1 \= Person2.
not_sibling(Person1, Person2) :- Person1 = Person2.
not_sibling(Person1, Person2) :- parent(Person1, Person2).
not_sibling(Person1, Person2) :- child(Person1, Person2).
not_sibling(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
not_sibling(Person1, Person2) :- uncle(Person1, Person2); uncle(Person2, Person1).
not_sibling(Person1, Person2) :- aunt(Person1, Person2); uncle(Person2, Person1).


not_siblings(Person1, Person2) :- not_sibling(Person1, Person2).
not_siblings(Person1, Person2) :- not_sibling(Person2, Person1).
not_brother(Person1, Person2) :- not_siblings(Person1, Person2).
not_brother(Person1, _) :- not_male(Person1).
not_sister(Person1, Person2) :- not_siblings(Person1, Person2).
not_sister(Person1, _) :- male(Person1).

father(Person1, Person2) :-
    male(Person1),          % Check if Person1 is a male
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    parent(Person1, Person2).  
mother(Person1, Person2) :-
    not_male(Person1),          % Check if Person1 is a female
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    parent(Person1, Person2).  
brother(Person1, Person2) :-
    male(Person1),          % Check if Person1 is a male
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    siblings(Person1, Person2). % Check if they are siblings 
sister(Person1, Person2) :-
    not_male(Person1),          % Check if Person1 is a female
    Person1 \= Person2,     % Check if Person1 and Person2 are not the same
    siblings(Person1, Person2). % Check if they are siblings  

grandparent(Person1, Person2) :- parent(Person1, Person), parent(Person, Person2), Person1 \= Person2.
not_grandparent(Person1, Person2) :- grandparent(Person2, Person1).
not_grandparent(Person1, Person2) :- siblings(Person1, Person2).
not_grandparent(Person1, Person2) :- uncle(Person1, Person2); uncle(Person2, Person1).
not_grandparent(Person1, Person2) :- aunt(Person1, Person2); aunt(Person2, Person1).
not_grandparent(Person1, Person2) :- parent(Person1, Person2).
not_grandparent(Person1, Person2) :- child(Person1, Person2).
not_grandparent(Person1, Person2) :- Person1 = Person2.
not_grandparent(Person1, Person2) :- two_grandparents(Person2), \+ grandparent(Person1, Person2). % there could only be a max of two grand parents



grandfather(Person1, Person2) :- 
    male(Person1),
    Person1 \= Person2,
    grandparent(Person1, Person2).
not_grandfather(Person1, _) :- not_male(Person1).
not_grandfather(Person1, Person2) :- not_grandparent(Person1, Person2).
not_grandfather(Person1, Person2) :- one_grandfather(Person2), \+ grandfather(Person1, Person2).
grandmother(Person1, Person2) :- 
    not_male(Person1),
    Person1 \= Person2,
    grandparent(Person1, Person2).
not_grandmother(Person1, _) :- male(Person1).
not_grandmother(Person1, Person2) :- not_grandparent(Person1, Person2).
not_grandmother(Person1, Person2) :- one_grandmother(Person2, \+ grandmother(Person1, Person2)).
 
 % for some reason, can't use brother/2
uncle(Person1, Person2) :- male(Person1), siblings(Person1, Person), parent(Person, Person2), Person1 \= Person2.
uncle(Person1, Person2) :- male(Person1), married(Person1, Spouse), siblings(Spouse, Sibling), parent(Sibling, Person2), Person1 \= Person2.
not_uncle(Person1, _) :- not_male(Person1).
not_uncle(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
not_uncle(Person1, Person2) :- siblings(Person1, Person2).
not_uncle(Person1, Person2) :- uncle(Person2, Person1).
not_uncle(Person1, Person2) :- aunt(Person1, Person2), aunt(Person2, Person1).
not_uncle(Person1, Person2) :- parent(Person1, Person2).
not_uncle(Person1, Person2) :- child(Person1, Person2).
% for some reason, can't use sister/2
aunt(Person1, Person2) :- not_male(Person1), siblings(Person1, Person), parent(Person, Person2), Person1 \= Person2.
aunt(Person1, Person2) :- not_male(Person1), married(Person1, Spouse), siblings(Spouse, Sibling), parent(Sibling, Person2), Person1 \= Person2.
not_aunt(Person1, _) :- male(Person1).
not_aunt(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
not_aunt(Person1, Person2) :- siblings(Person1, Person2).
not_aunt(Person1, Person2) :- uncle(Person2, Person1), uncle(Person2, Person1).
not_aunt(Person1, Person2) :- aunt(Person1, Person2).
not_aunt(Person1, Person2) :- parent(Person1, Person2).
not_aunt(Person1, Person2) :- child(Person1, Person2).

married(Person1, Person2) :- (parent(Person1, Person), parent(Person2, Person)); (parent(Person2, Person), mother(Person1, Person)), Person1 \= Person2.
not_married(Person1, _) :- \+ married(Person1, _).

% Define a rule to check if X is a descendant of Y
descendant(X, Y) :-
    parent(Y, X). % X is a direct child of Y

descendant(X, Y) :-
    parent(Z, X), % X has a parent Z
    descendant(Z, Y). % Z is a descendant of Y

relatives(Person1, Person2) :- siblings(Person1, Person2).
relatives(Person1, Person2) :- grandparent(Person1, Person2); grandparent(Person2, Person1).
relatives(Person1, Person2) :- uncle(Person1, Person2); uncle(Person2, Person1).
relatives(Person1, Person2) :- aunt(Person1, Person2); aunt(Person2, Person1).
relatives(Person1, Person2) :- parent(Person1, Person2).
relatives(Person1, Person2) :- child(Person1, Person2).
relatives(Person1, Person2) :- married(Person1, Person2).
relatives(Person1, Person2) :- descendant(Person1, Person2); descendant(Person2, Person1).
not_relatives(Person1, Person2) :- Person1 = Person2.