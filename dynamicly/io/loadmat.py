from scipy.io import loadmat as lm
import scipy.io as spio
import pathlib


def loadmat(filename, single_key=True, contains=False):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    mat_tags = ['__header__', '__version__', '__globals__']
    if isinstance(filename, pathlib.Path) and filename.is_dir():
        accectable = f'*{contains}*' if contains else '*'
        data = {file.stem: lm(file, struct_as_record=False, squeeze_me=True)
                for file in filename.glob(f'{accectable}.mat')}
        dictionary = _check_keys(data)
        for key, val in dictionary.items():
            new_dict = _check_keys(val)
            new_dict = {key: val for key, val in new_dict.items() if
                        key not in mat_tags}
            data[key] = new_dict[list(new_dict.keys())[0]]

    else:
        data = lm(filename, struct_as_record=False, squeeze_me=True)
        # if isinstance()
        dictionary = _check_keys(data)
        data = {key: val for key, val in dictionary.items() if
                key not in mat_tags}

        if single_key and len(data) == 1:
            data = data[list(data.keys())[0]]
    return data


# OLD LOAD MAT THAT COULDNT HANDLE NESTED DICTIONARIES
# def loadmat(path, key = True):
#     dictionary = lm(path)
#     mat_tags = ['__header__', '__version__', '__globals__']
#     data = {key: val for key, val in dictionary.items() if key not in mat_tags}
#     if key and len(data) == 1:
#         data = data[list(data.keys())[0]]
#     return data


def loadmat_nested(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = lm(filename, struct_as_record=False, squeeze_me=True)
    dictionary = _check_keys(data)
    mat_tags = ['__header__', '__version__', '__globals__']
    data = {key: val for key, val in dictionary.items() if key not in mat_tags}
    return data


def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def path_to_filename(path):
    file_with_ext = path.split('\\')[-1]
    file = file_with_ext.split('.')[0]
    return file
