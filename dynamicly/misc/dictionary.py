def quick_dict(some_iterable):
    quick_dict = {}
    for i, val in enumerate(some_iterable):
        quick_dict[str(i)] = val
    return quick_dict

def key_contains(dictionary, string, return_opposite=False):
    if isinstance(string, list):
        new = dictionary
        for phrase in string:
            new = {key: val for key, val in new.items() if phrase in key}
    else:
        new = {key: val for key, val in dictionary.items() if string in key}
    if return_opposite:
        opposite = {key:val for key,val in dictionary if key not in new.keys()}
        return new, opposite
    else:
        return new


def first(dictionnary):
    return dictionnary[list(dictionnary.keys())[0]]