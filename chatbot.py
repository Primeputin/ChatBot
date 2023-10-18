from logic import *
import re

def areRelatives(name1, name2):
    return Atom("Relatives", name1, name2)
def areSiblings(name1, name2):
    return Atom("Siblings", name1, name2)
def sister(sister, person):
    return Atom("Sister", sister, person)
def mother(mother, person):
    return Atom("Mother", mother, person)
def grandmother(grandmother, person):
    return Atom("Grandmother", grandmother, person)
def child(child, person):
    return Atom("Child", child ,person)
def daughter(daughter, person):
    return Atom("Daughter", daughter, person)
def uncle(uncle, person):
    return Atom("Uncle", uncle, person)
def brother(brother, person):
    return Atom("Brother", brother, person)
def father(father, person):
    return Atom("Father", father, person)
def parent(parent, child):
    return Atom("Parent", parent, child)
def grandfathter(grandfather, person):
    return Atom("Grandfather", grandfather, person)
def childrenOf(child1, child2, child3, ancestor):
    return And(child(child1, ancestor), 
               And(child(child2, ancestor), 
                   child(child3, ancestor)))
def son(son, person):
    return Atom("Son", son, person)
def aunt(aunt, person):
    return Atom("Aunt", aunt, person)

def make_lower(groups):
    return tuple(element.lower() for element in groups)
def three_not_equal(element1, element2, element3):
    return And(And(Not(Equals(element1, element2)), Not(Equals(element1, element3))), Not(Equals(element2, element3)))
kb = createResolutionKB()

response = kb.tell(Forall("$x", Not(areRelatives("$x", "$x"))))
print(response)
response = kb.tell(Forall("$x", Forall("$y", Implies(Or(father("$x", "$y"), Or(mother("$x", "$y"), Or(brother("$x", "$y"), sister("$x", "$y")))), areRelatives("$x", "$y"))))) # If there is a connection between them, they are both relatives of each other
print(response)
response = kb.tell(Forall("$x", Forall("$y", Implies(areRelatives("$x", "$y"), areRelatives("$y", "$x"))))) # they are both relatives of each other
print(response)

response = kb.tell(Forall("$x", Forall("$y", Implies(And(Not(Equals("$x", "$y")), Or(sister("$x", "$y"), brother("$x", "$y"))), areSiblings("$x", "$y"))))) # All brothers and sisters are siblings of someone
print(response)
response = kb.tell(Forall("$x", Forall("$y", Implies(areSiblings("$x", "$y"), areSiblings("$y", "$x"))))) # they are both siblings of each other
print(response)
response = kb.tell(Forall("$x", Forall("$y", Implies(brother("$x", "$y"), Not(sister("$x", "$y")))))) # a person cannot be a brother and sister at the same time
print(response)

# a sibling of someone is a sibling to all siblings
# a brother of someone is a brother to all siblings

while (True):
    prompt = input("Prompt: ")
    isMatch = re.match(r"(\w+) is (?:the|a|an) (\w+) of (\w+)", prompt)
    sibsMatch = re.match(r"(\w+) and (\w+) are siblings", prompt)
    parentsMatch = re.match(r"(\w+) and (\w+) are the parents of (\w+)", prompt)
    childrenMatch = re.match(r"(\w+), (\w+), and (\w+) are children of (\w+)", prompt)
    isQuestion = re.match(r"Is (\w+) (?:the|a|an) (\w+) of (\w+)?", prompt)
    areSibRel = re.match(r"Are (\w+) and (\w+) (\w+)?", prompt)
    areParentsMatch = re.match(r"Are (\w+) and (\w+) the parents of (\w+)?", prompt)
    areChildrenMatch = re.match(r"Are (\w+), (\w+), and (\w+) children of (\w+)?", prompt)
    if isMatch: # simple is statement
        person1, relation, person2 = isMatch.groups()
        person1 = person1.lower()
        person2 = person2.lower()
        print("person 1: ", person1)
        print("relation: ", relation)
        print("person 2:", person2)
        response = kb.tell(Atom(relation.capitalize(), person1, person2))
        print(response)
    elif sibsMatch:
        sib1, sib2 = make_lower(sibsMatch.groups())
        print("sibling 1: ", sib1)
        print("sibling 2: ", sib2)
        response = kb.tell(areSiblings(sib1, sib2))
        print(response)
    elif parentsMatch: # statements regarding parents
        parent1, parent2, child = make_lower(parentsMatch.groups())
        print("parent 1: ", parent1)
        print("parent 2: ", parent2)
        print("child:", child)
        response = kb.tell(And(Atom("Parent", parent1, child),
                                Atom("Parent", parent2, child)))
        print(response)
    elif childrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(childrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        response = kb.tell(And(child(child1, ancestor), 
                And(child(child2, ancestor), 
                    child(child3, ancestor))))
        print(response)
    elif isQuestion:
        person1, relation, person2 = isQuestion.groups()
        person1 = person1.lower()
        person2 = person2.lower()
        response = kb.ask(Atom(relation.capitalize(), person1, person2))
        print(response)
    elif areSibRel:
        person1, person2, relation = areSibRel.groups()
        person1 = person1.lower()
        person2 = person2.lower()
        response = kb.ask(Atom(relation.capitalize(), person1, person2))
        print(response)
    elif areParentsMatch:
        parent1, parent2, child = make_lower(areParentsMatch.groups())
        response = kb.ask(And(Atom("Parent", parent1, child),
                                Atom("Parent", parent2, child)))
        print(response)
    elif areChildrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(areChildrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        response = kb.ask(And(child(child1, ancestor), 
                And(child(child2, ancestor), 
                    child(child3, ancestor))))
        print(response)
    # more question pattern matching to be added regarding who's question
    else:
        print("Sentence mismatch")