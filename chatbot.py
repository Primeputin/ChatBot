from pyswip import Prolog
import re

kb = Prolog()
kb.consult("knowledge_base.pl")
def make_lower(groups):
    return tuple(element.lower() for element in groups)
def show_relations(q):
    for i in q:
        print(i["X"])

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

    whoSibs = re.match(r"Who are the siblings of (\w+)?", prompt)
    whoSis = re.match(r"Who are the sisters of (\w+)?", prompt)
    whoBro = re.match(r"Who are the brothers of (\w+)?", prompt)
    whoParents = re.match(r"Who are the parents of (\w+)?", prompt)
    whoSons = re.match(r"Who are the sons of (\w+)?", prompt)
    whoDaughters = re.match(r"Who are the daughters of (\w+)?", prompt)
    whoChild = re.match(r"Who are the children of (\w+)?", prompt)
    whoPaMa = re.match(r"Who is the (\w+) of (\w+)?", prompt)

    if whoPaMa: # this is first than isMatch because isMatch may overlap with this one
        relation, person = make_lower(whoPaMa.groups())
        show_relations(list(kb.query(f"{relation}(X, {person})")))
    elif isMatch: # simple is statement
        person1, relation, person2 = make_lower(isMatch.groups())
        print("person 1: ", person1)
        print("relation: ", relation)
        print("person 2:", person2)
        kb.assertz(f"{relation}({person1}, {person2})")
    elif sibsMatch:
        sib1, sib2 = make_lower(sibsMatch.groups())
        print("sibling 1: ", sib1)
        print("sibling 2: ", sib2)
        kb.assertz(f"sibling({sib1}, {sib2})")
    elif parentsMatch: # statements regarding parents
        parent1, parent2, child = make_lower(parentsMatch.groups())
        print("parent 1: ", parent1)
        print("parent 2: ", parent2)
        print("child:", child)
        kb.assertz(f"parent({parent1}, {child}), parent({parent2}, {child})")
    elif childrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(childrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        kb.assertz(f"child({child1}, {ancestor}), child({child2}, {ancestor}), child({child3}, {ancestor})")
    elif isQuestion:
        person1, relation, person2 = make_lower(isQuestion.groups())
        print(bool(list(kb.query(f"{relation}({person1}, {person2})"))))
    elif areSibRel:
        person1, person2, relation = make_lower(areSibRel.groups())
        print(person1)
        print(relation)
        print(person2)
        print(bool(list(kb.query(f"{relation}({person1}, {person2})"))))
    elif areParentsMatch:
        parent1, parent2, child = make_lower(areParentsMatch.groups())
        print(bool(list(kb.query(f"parent({parent1}, {child}), parent({parent2}, {child})"))))
    elif areChildrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(areChildrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        print(bool(list(kb.query(f"child({child1}, {ancestor}), child({child2}, {ancestor}), child({child3}, {ancestor})"))))
    elif whoSibs:
        person = whoSibs.group(1).lower() # getting the inputted match only
        show_relations(list(kb.query(f"siblings(X, {person})")))
    elif whoSis:
        person = whoSis.group(1).lower()
        show_relations(list(kb.query(f"sister(X, {person})")))
    elif whoBro:
        person = whoBro.group(1).lower()
        show_relations(list(kb.query(f"brother(X, {person})")))
    elif whoParents:
        person = whoParents.group(1).lower()
        show_relations(list(kb.query(f"parent(X, {person})")))
    elif whoSons:
        person = whoSons.group(1).lower()
        show_relations(list(kb.query(f"son(X, {person})")))
    elif whoDaughters:
        person = whoDaughters.group(1).lower()
        show_relations(list(kb.query(f"daughter(X, {person})")))
    elif whoChild:
        person = whoChild.group(1).lower()
        show_relations(list(kb.query(f"child(X, {person})")))
    else:
        print("Sentence mismatch")