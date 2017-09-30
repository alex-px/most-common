from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def split_snake_case_to_words(name):
    return [word for word in name.split('_') if word]


def is_magic_name(name):
    return name.startswith('__') and name.endswith('__')