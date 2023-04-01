import pickle


def load(fp):
    with open(fp, 'rb') as f:
        return pickle.load(f)


def dump(data, fp):
    with open(fp, 'wb') as f:
        return pickle.dump(data, f)
