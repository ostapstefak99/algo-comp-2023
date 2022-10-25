#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses

def compute_gender_compatibility(user1: User, user2: User) -> float:
    """
    Strict gender compatibility matching.
    If preferences are satisfied, return 1.
    Else, return 0.
    """

    if user2.gender in user1.preferences and user1.gender in user2.preferences:
        return True
    
    else: 
        return False


def compute_grad_year_compatibility(user1: User, user2: User) -> float:
    """
    Returns graduation year compatibility between two users. 
    Returned value ranges from 0 to 1
    """
    age_gap_fm_f_older = [.5, .25, .1, 0] # index = number of years F is older by
    age_gap_fm_m_older = [.5, 1, .5, 0] # index = number of years M is older by
    age_gap_same_sex = [1, .5, .25, .25] # index = age difference

    grad_diff = user1.grad_year - user2.grad_year

    if user1.gender == user2.gender:
        return age_gap_same_sex[abs(grad_diff)]

    elif user1.gender != user2.gender:
        if user1.gender == "M":
            if grad_diff > 0:
                return age_gap_fm_f_older[grad_diff]
            else:
                return age_gap_fm_m_older[-grad_diff]

        elif user1.gender == "F":
            if grad_diff > 0:
                return age_gap_fm_m_older[grad_diff]
            else:
                return age_gap_fm_f_older[-grad_diff]
    

def compute_response_distribution(users):
    """
    Computes response distribution for the set of questions.
    Returns a list of lists, where first index is the question number,
    and second index is the response. The value at response_distribution[i, j] 
    is the number of responses j for question i. 
    """
    
    response_distribution = [[0,0,0,0,0,0] for i in range(20)]

    for user in users:
        for question_num in range(len(user.responses)):
            user_response = user.responses[question_num]
            response_distribution[question_num][user_response] += 1

    return response_distribution
    
def resp_scale_factor(p1, p2):
    return 1/(1+(p1*p2)**(1/2))


def compute_response_compatibility(user1: User, user2: User, response_distribution):
    """
    Returns a value between 0 and 1. 
    """

    total_compatibility = 0

    num_users = len(users)
    
    for question_num in range(20):
        user1_resp = user1.responses[question_num]
        user2_resp = user2.responses[question_num]

        if user1_resp == user2_resp:
            p1 = response_distribution[question_num][user1_resp] / num_users
            p2 = response_distribution[question_num][user2_resp] / num_users
            
            resp_scale = resp_scale_factor(p1, p2)
            total_compatibility += 1/20 * resp_scale     

    return total_compatibility



# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    """
    Returns value between 0 and 1
    """

    factor_weights = { # weight on different types of similarity
        "grad": .1, # weight on graduation year
        "resp": .9 # weight on response similarity
    }

    genders_compatible = compute_gender_compatibility(user1=user1, user2=user2)

    if not genders_compatible:
        return 0

    else:
        grad_compatibility = compute_grad_year_compatibility(user1=user1, user2=user2)
        
        response_distribution = compute_response_distribution(users)
        resp_compatibility = compute_response_compatibility(user1=user1, user2=user2, response_distribution=response_distribution)

        return factor_weights["grad"] * grad_compatibility + factor_weights["resp"] * resp_compatibility



if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
