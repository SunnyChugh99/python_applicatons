import pickle

with open('scoring_func', 'r') as file:
    score_code = file.read()

with open('score.pkl', 'wb') as pickle_file:
    pickle.dump(score_code, pickle_file)
