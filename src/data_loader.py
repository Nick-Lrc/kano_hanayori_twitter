import pickle
import os

WORKING_DIR = os.path.join('..', 'data')
RAW_DIR = os.path.join(WORKING_DIR, 'raw')

def load_user():
    return load_pickle(os.path.join(RAW_DIR, 'user.pickle'))

def load_tweets():
    return load_pickle(os.path.join(RAW_DIR, 'tweets.pickle'))

def load_pickle(path):
    with open(path, 'rb') as file:
        return pickle.load(file)
