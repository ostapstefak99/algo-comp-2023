import numpy as np
from typing import List, Tuple
import random

def preferences_satisfied(gender1, pref1, gender2, pref2):
    pref_to_gender = {
        'Men': ['Male', 'Nonbinary'],
        'Women': ['Female', 'Nonbinary'],
        'Bisexual': ['Male', 'Female', 'Nonbinary']
    }

    if gender2 in pref_to_gender[pref1] and gender1 in pref_to_gender[pref2]:
        return True
    else:
        return False

def truify_scores(scores, gender_id, gender_pref):
    """Make scores reflect gender preferences
    """
    N = len(scores)
    for i in range(N):
        for j in range(N):
            if i < j:
                gender1 = gender_id[i]
                gender2 = gender_id[j]
                pref1 = gender_pref[i]
                pref2 = gender_pref[j]

                if not preferences_satisfied(gender1, pref1, gender2, pref2):
                    scores[i][j] = 0
                    scores[j][i] = 0
        
    return scores

def construct_preferences_dict(props_initial, scores, prop):
    """
        Construct dictionary of prop preferences
    """
    preferences = scores[prop].copy()
    preferences_dict = dict()
    
    for i in range(len(scores)): # remove other props from preferences
        if i not in props_initial: # i can only have preference for acc
            preferences_dict[i] = preferences[i]
        
    return preferences_dict

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """
    g = truify_scores(scores, gender_id, gender_pref)
    
    N = len(scores) # total number of people we need to match

    # FOR DEBUGGING
    for i in range(N):
        print(i, g[i])

    people = list(range(len(scores)))
    props_initial = sorted(people, key=lambda _: random.random())[:int(N/2)] # set a random half of people to be proposers
    
    #accs = list(set(people) - set(props_initial)) # everyone else is an accepter #WE DON'T NEED THIS LINE
    
    # FOR DEBUGGING
    print(props_initial)

    matches = dict() # this will be a dict of acc: prop

    active_props = props_initial.copy()

    while active_props != list():

        # take the first proposer 'in line'
        prop = active_props[0]         

        preferences_dict = construct_preferences_dict(props_initial, scores, prop)

        matched = False

        while not matched:
            
            top_pref_acc = max(preferences_dict, key=preferences_dict.get)
            matched_acc = matches.keys()

            if top_pref_acc not in matched_acc:
                matches[top_pref_acc] = prop
                active_props.remove(prop)
                matched = True
            
            elif scores[top_pref_acc][prop] > scores[top_pref_acc][matches[top_pref_acc]]:
                old_prop = matches[top_pref_acc]
                active_props.append(old_prop)
                matches[top_pref_acc] = prop
                active_props.remove(prop)
                matched = True
            else:
                # remove acc from preferences. prop has been rejected :(((
                del preferences_dict[top_pref_acc]
    
    # for debugging
    print(matches)

    return matches

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
