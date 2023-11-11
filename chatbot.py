from pyswip import Prolog
import re

kb = Prolog()
kb.consult("knowledge_base.pl")

simplified = {'brother': 'sibling', 'sister': 'sibling', 'father': 'parent', 'mother': 'parent',
              'grandfather': 'grandparent', 'grandmother': 'grandparent', 'son': 'child',
              'daughter': 'child', 'child': 'child', 'siblings': 'sibling',
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
    if person1 == person2 or bool(list(kb.query(f'not_' + statement))): # second condition is important just in case it's already not valid
        return -1 # contradiction
    if bool(list(kb.query(statement))):
        return 1 # entailment
    gender = morf(kb, person1, relation)
    right = bool(list(kb.query(f'{simplified[relation]}({person1}, {person2})')))
    not_right = bool(list(kb.query(f'not_{simplified[relation]}({person1}, {person2})')))
    if right and not not_right and (gender == 2 or gender == 0):
        return 1 # entailment
    if not right and not_right or gender == -1:  
        return -1 # contradiction
    else:
        if simplified[relation] == 'parent':
            kb.assertz(f'child({person2}, {person1})')
        else:
            if simplified[relation] == 'child': # for when a father/mother already exist, therefore the other one should be a father/mother
                one_father = bool(list(kb.query(f'one_father({person1})')))
                one_mother = bool(list(kb.query(f'one_mother({person1})')))
                two_parents = bool(list(kb.query(f'two_parents({person1})')))
                if one_father and not two_parents:
                    if check_morf(kb, person2, 'mother') != -1:
                        kb.assertz(f'not_male({person2})') # person2 is female
                        kb.assertz(f'not(male({person2}))')
                    else:
                        return -1 # contradiction
                elif one_mother and not two_parents:
                    if check_morf(kb, person2, 'father') != -1:
                        kb.assertz(f'male({person2})') # person2 is male
                        kb.assertz(f'not(not_male({person2}))')
                    else:
                        return -1 # contradiction
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
        check = f'{relation}({i}, {person})'
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
    if right and not not_right and (gender == 2 or gender == 0):
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
    same = False
    for i in people:
        if i == person:
            same = True
            break
        rel += f'{relation}({i}, {person}),'
        not_rel += f'not_{relation}({i}, {person});'
    if same:
        print('No')
    elif rel and not_rel:
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

def have_space(name):
    for i in name:
        if i == ' ':
            return True
    return False
def all_alpha(word):
    for i in word:
        if not i.isalpha():
            return False
    return True

def children_tell_prompt(prompt):
    childrenParts = prompt.split('are children of')
    if len(childrenParts) == 2 and childrenParts[1][len(childrenParts[1]) - 1] == '.':
        parent_name = childrenParts[1][:len(childrenParts[1]) - 1].strip().lower()
        if not all_alpha(parent_name):
            return "",[]
        child_names = [name.strip() for name in childrenParts[0].split(",")]
        if len(child_names) == 1: # if two children only
            and_child_names = [name.strip().lower() for name in re.split(r'\s+', child_names[0])]
            if len(and_child_names) == 3:
                if all_alpha(and_child_names[0]) and and_child_names[1] == 'and' and all_alpha(and_child_names[2]):
                    and_child_names.pop(1)
                    return parent_name, and_child_names
            return "", []
        for index in range(len(child_names)):
            child_parts = child_names[index].split(' ')
            temp = child_names[index]
            if len(child_parts) == 1 and child_parts[0] == '':
                return "", []
            if len(child_parts) < 1 or len(child_parts) > 2:
                return "", []
            first_part = child_parts[0]
            if index == len(child_names) - 1 and len(child_names) != 2:
                if first_part == 'and' and len(child_parts) == 2:
                    child_names[index] = temp.replace('and', '')
                    temp = child_names[index]
                else:
                    return "", []
            child_names[index] = temp.strip().lower()
            if not all_alpha(child_names[index]):
                return "", []
        return parent_name, child_names
    return "", []

def children_ask_prompt(prompt):
    childrenParts = prompt.split('children of')
    if len(childrenParts) == 2 and childrenParts[0][:3] == 'are' and childrenParts[1][len(childrenParts[1]) - 1] == '?':
        parent_name = childrenParts[1][:len(childrenParts[1]) - 1].strip().lower()
        if not all_alpha(parent_name):
            return "",[]
        child_names = [name.strip() for name in childrenParts[0].split(",")]
        if len(child_names) == 1: # if two children only
            and_child_names = [name.strip().lower() for name in re.split(r'\s+', child_names[0])]
            if len(and_child_names) == 4:
                if and_child_names[0] == 'are' and all_alpha(and_child_names[1]) and and_child_names[2] == 'and' and all_alpha(and_child_names[3]): # are is lower case here from the list comprehension above
                    and_child_names.pop(0)
                    and_child_names.pop(2)
                    return parent_name, and_child_names
            return "", []
        for index in range(len(child_names)):
            child_parts = child_names[index].split(' ')
            temp = child_names[index]
            if len(child_parts) == 1 and child_parts[0] == '': # if extra empty string
                return "", []
            if len(child_parts) < 1 or len(child_parts) > 2: # wrong number left
                return "", []
            first_part = child_parts[0]
            if index == len(child_names) - 1 and len(child_names) != 2: # last child and not the second
                if first_part == 'and' and len(child_parts) == 2:
                    child_names[index] = temp.replace('and', '')
                    temp = child_names[index]
                else:
                    return "", []
            elif index == 0:
                if first_part == 'are' and len(child_parts) == 2:
                    child_names[index] = temp.replace('are', '')
                    temp = child_names[index] 
            child_names[index] = temp.strip().lower()
            if not all_alpha(child_names[index]):
                return "", []
        return parent_name, child_names
    return "", []
        
while (True):
    inputted = input("Prompt: ")
    prompt = inputted.lower()

    isMatch = re.match(r"^(\w+)\s+is\s+(?:the|a|an)\s+((?:father|mother|brother|sister|child|son|daughter|grandfather|grandmother|uncle|aunt))\s+of\s+(\w+)\.$", prompt)
    sibsMatch = re.match(r"^(\w+)\s+and\s+(\w+)\s+are\s+siblings\.$", prompt)
    parentsMatch = re.match(r"^(\w+)\s+and\s+(\w+)\s+are\s+the\s+parents\s+of\s+(\w+)\.$", prompt)

    isQuestion = re.match(r"^[Ii]s\s+(\w+)\s+(?:the|a|an)\s+((?:father|mother|brother|sister|child|son|daughter|grandfather|grandmother|uncle|aunt))\s+of\s+(\w+)\?$", prompt)
    areSibRel = re.match(r"^[Aa]re\s+(\w+)\s+and\s+(\w+)\s+((?:siblings|relatives))\?$", prompt)
    areParentsMatch = re.match(r"^[Aa]re\s+(\w+)\s+and\s+(\w+)\s+the\s+parents\s+of\s+(\w+)\?$", prompt)

    whoSibs = re.match(r"^[Ww]ho\s+are\s+the\s+siblings\s+of\s+(\w+)\?$", prompt)
    whoSis = re.match(r"^[Ww]ho\s+are\s+the\s+sisters\s+of\s+(\w+)\?$", prompt)
    whoBro = re.match(r"^[Ww]ho\s+are\s+the\s+brothers\s+of\s+(\w+)\?$", prompt)
    whoParents = re.match(r"^[Ww]ho\s+are\s+the\s+parents\s+of\s+(\w+)\?$", prompt)
    whoSons = re.match(r"^[Ww]ho\s+are\s+the\s+sons\s+of\s+(\w+)\?$", prompt)
    whoDaughters = re.match(r"^[Ww]ho\s+are\s+the\s+daughters\s+of\s+(\w+)\?$", prompt)
    whoChild = re.match(r"^[Ww]ho\s+are\s+the\s+children\s+of\s+(\w+)\?$", prompt)
    whoPaMa = re.match(r"^[Ww]ho\s+is\s+the\s+((?:father|mother))\s+of\s+(\w+)\?$", prompt)
    
    parent_tell, children_tell = children_tell_prompt(prompt)
    parent, children = children_ask_prompt(prompt)
    if whoPaMa: # this is first than isMatch because isMatch may overlap with this one
        relation, person = make_lower(whoPaMa.groups())
        show_relations(list(kb.query(f"{relation}(X, {person})")))
    elif isMatch: # simple is statement
        person1, relation, person2 = make_lower(isMatch.groups())
        check = f"{relation}({person1}, {person2})"
        tell(tell_response(kb, check, person1, relation, person2))
    elif sibsMatch:
        sib1, sib2 = make_lower(sibsMatch.groups())
        check = f"siblings({sib1}, {sib2})"
        tell(tell_response(kb, check, sib1, 'siblings', sib2))
    elif parentsMatch: # statements regarding parents
        parent1, parent2, child = make_lower(parentsMatch.groups())
        tell(compound_respond(kb, [parent1, parent2], 'parent', child))
    elif parent_tell and children_tell: # statements regarding children
        tell(compound_respond(kb, children_tell, 'child', parent_tell))
    elif isQuestion:
        person1, relation, person2 = make_lower(isQuestion.groups())
        ask_response(kb, person1, relation, person2)
    elif areSibRel:
        person1, person2, relation = make_lower(areSibRel.groups())
        ask_response(kb, person1, relation, person2)
    elif areParentsMatch:
        parent1, parent2, child = make_lower(areParentsMatch.groups())
        compound_ask(kb, [parent1, parent2], 'parent', child)
    elif parent and children: # questions about children.
        compound_ask(kb, children, 'child', parent)
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
    # need to type cast to list to execute the query
    # a query is needed to assess the condition because it won't be checked in Prolog automatically in any case
    list(kb.query("make_missing_children_parents(X, Y)")) 