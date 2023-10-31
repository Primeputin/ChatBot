from pyswip import Prolog
import re

kb = Prolog()
kb.consult("knowledge_base.pl")

simplified = {'brother': 'sibling', 'sister': 'sibling', 'father': 'parent', 'mother': 'parent',
              'grandfather': 'grandparent', 'grandmother': 'grandparent', 'son': 'child_of',
              'daughter': 'child_of', 'child': 'child_of', 'siblings': 'sibling',
              'uncle': 'uncle', 'aunt': 'aunt'}

def make_lower(groups):
    return tuple(element.lower() for element in groups)
def show_relations(q):
    for i in q:
        print(i["X"])

def is_male(relation):
    if relation == 'brother' or relation == 'father' or relation == 'grandfather' or relation == 'son' or relation == 'uncle':
        return True
    return False

def is_female(relation):
    if relation == 'sister' or relation == 'mother' or relation == 'grandmother' or relation == 'daughter' or relation == 'aunt':
        return True
    return False

def tell_response(kb, statement, person1, relation, person2):
    if person1 == person2 or bool(list(kb.query(f'not_' + statement))):
        return -1 # contradiction
    if bool(list(kb.query(statement))):
        return 1 # entailment
    gender = morf(kb, person1, relation)
    right = bool(list(kb.query(f'{simplified[relation]}({person1}, {person2})')))
    not_right = bool(list(kb.query(f'not_{simplified[relation]}({person1}, {person2})')))
    if right and not not_right and gender != -1:
        return 1 # entailment
    if not right and not_right or gender == -1:  
        return -1 # contradiction
    else:
        kb.assertz(f'{simplified[relation]}({person1}, {person2})')
        return 0 # contingency   
    
def tell(response):
    if response == -1:
        print("That's impossible!")  # contradiction
    elif response == 0:
        print("Ok, I learned something.") # contingency
    elif response == 1:
        print("I already knew that") # entailment

def morf(kb, person, relation):
    if is_male(relation):
        male = bool(list(kb.query(f'male({person})')))
        not_male = bool(list(kb.query(f'not_male({person})')))
        if male and not not_male:
            return 2 # meaning male fact already exist
        elif not male and not not_male:
            kb.assertz(f'male({person})')
            kb.assertz(f'not(not_male({person}))')
            return 1 # meaning male fact is asserted
        elif not male and not_male:
            return -1 # not male
    elif is_female(relation):
        male = bool(list(kb.query(f'male({person})')))
        not_male = bool(list(kb.query(f'not_male({person})')))
        if not_male and not male:
            return 2 # meaning female fact already exist
        elif not not_male and not male:
            kb.assertz(f'not_male({person})')
            kb.assertz(f'not(male({person}))')
            return 1 # meaning female fact is asserted
        elif not not_male and male:
            return -1 # not female
    return 0 # meaning no gender needed for the relation

def compound_respond(kb, people, relation, person):
    learned = False
    for i in people:
        check = f'{relation}({person}, {i})'
        response = check_tell_response(kb, check, i, relation, person)
        if response == 0:
            learned = True
        elif response == -1:
            break
    if learned and response != -1:
        for i in people:
            check = f'{relation}({person}, {i})'
            tell_response(kb, check, i, relation, person)
        return 0 # contingency
    elif not learned and response != -1:
        return 1 # entailment
    else:
        return -1 # contadiction

# doesn't assert anything, just checking
def check_tell_response(kb, statement, person1, relation, person2):
    if person1 == person2 or bool(list(kb.query(f'not_' + statement))):
        return -1 # contradiction
    if bool(list(kb.query(statement))):
        return 1 # entailment
    gender = check_morf(kb, person1, relation)
    right = bool(list(kb.query(f'{simplified[relation]}({person1}, {person2})')))
    not_right = bool(list(kb.query(f'not_{simplified[relation]}({person1}, {person2})')))
    if right and not not_right and gender != -1:
        return 1 # entailment
    if not right and not_right or gender == -1:  
        return -1 # contradiction
    else:
        return 0 # contingency

# doesn't assert anything, just checking 
def check_morf(kb, person, relation):
    if is_male(relation):
        male = bool(list(kb.query(f'male({person})')))
        not_male = bool(list(kb.query(f'not_male({person})')))
        if male and not not_male:
            return 2 # meaning male fact already exist
        elif not male and not not_male:
            return 1 # meaning male fact is asserted
        elif not male and not_male:
            return -1 # not male
    elif is_female(relation):
        male = bool(list(kb.query(f'male({person})')))
        not_male = bool(list(kb.query(f'not_male({person})')))
        if not_male and not male:
            return 2 # meaning female fact already exist
        elif not not_male and not male:
            return 1 # meaning female fact is asserted
        elif not not_male and male:
            return -1 # not female
    return 0 # meaning no gender needed for the relation

def ask_response(kb, person1, relation, person2):
    if person1 == person2:
        print('No')
    else:
        right = bool(list(kb.query(f"{relation}({person1}, {person2})")))
        not_right = bool(list(kb.query(f"not_{relation}({person1}, {person2})")))
        if right and not not_right:
            print('Yes')
        elif not right and not not_right:
            print('I don\'t know')
        elif not right and not_right:
            print('No')
def compound_ask(kb, people, relation, person):
    rel = ''
    not_rel = ''
    for i in people:
        rel += f'{relation}({i}, {person}),'
        not_rel += f'not_{relation}({i}, {person});'
    if rel and not_rel:
        rel = rel[:-1]
        not_rel = not_rel[:-1]
        right = bool(list(kb.query(rel)))
        not_right = bool(list(kb.query(not_rel)))
        if right and not not_right:
            print('Yes')
        elif not right and not not_right:
            print('I don\'t know')
        elif not right and not not_right:
            print('No')
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
        check = f"{relation}({person1}, {person2})"
        tell(tell_response(kb, check, person1, relation, person2))
    elif sibsMatch:
        sib1, sib2 = make_lower(sibsMatch.groups())
        print("sibling 1: ", sib1)
        print("sibling 2: ", sib2)
        check = f"siblings({sib1}, {sib2})"
        tell(tell_response(kb, check, sib1, 'siblings', sib2))
    elif parentsMatch: # statements regarding parents
        parent1, parent2, child = make_lower(parentsMatch.groups())
        print("parent 1: ", parent1)
        print("parent 2: ", parent2)
        print("child:", child)
        tell(compound_respond(kb, [parent1, parent2], 'parent', child))
    elif childrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(childrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        tell(compound_respond(kb, [child1, child2, child3], 'child', ancestor))
    elif isQuestion:
        person1, relation, person2 = make_lower(isQuestion.groups())
        ask_response(kb, person1, relation, person2)
    elif areSibRel:
        person1, person2, relation = make_lower(areSibRel.groups())
        print(person1)
        print(relation)
        print(person2)
        ask_response(kb, person1, relation, person2)
    elif areParentsMatch:
        parent1, parent2, child = make_lower(areParentsMatch.groups())
        compound_ask(kb, [parent1, parent2], 'parent', child)
    elif areChildrenMatch: # statements regarding children
        child1, child2, child3, ancestor = make_lower(areChildrenMatch.groups())
        print("child 1: ", child1)
        print("child 2: ", child2)
        print("child 3: ", child3)
        print("ancestor: ", ancestor)
        compound_ask(kb, [child1, child2, child3], 'child', ancestor)
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