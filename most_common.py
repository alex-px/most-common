import ast
import collections
import os

from nltk import pos_tag


def flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    pos_info = pos_tag([word])
    return pos_info[0][1] == 'VB'


def find_py_files_in_path(root):
    py_files = []
    for current_dir, sub_dirs, files in os.walk(root):
        for current_file in files:
            if not current_file.endswith('.py'):
                continue
            py_files.append(os.path.join(current_dir, current_file))
    return py_files


def resolve_file_into_tree(file_path):
    with open(file_path, 'r', encoding='utf-8') as attempt_handler:
        main_file_content = attempt_handler.read()
    try:
        return ast.parse(main_file_content)
    except SyntaxError as e:
        print(e)


def fetch_trees_from_path(_path):
    trees = []
    py_files = find_py_files_in_path(_path)
    print('total %s py files found' % len(py_files))

    for py_file in py_files:
        tree = resolve_file_into_tree(py_file)
        if not tree:
            continue
        trees.append(tree)
    print('trees generated')
    return trees


def find_all_names_in_tree(tree):
    return [node.id for node in ast.walk(tree) if isinstance(node, ast.Name)]


def find_function_names_in_tree(tree):
    return [node.name.lower()
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)]


def extract_verbs_from_snake_case(name):
    return [word for word
            in split_snake_case_to_words(name)
            if is_verb(word)]


def split_snake_case_to_words(name):
    return [word for word in name.split('_') if word]


def is_magic_name(name):
    return name.startswith('__') and name.endswith('__')


def receive_names_in_path(_path):
    all_names = []
    for tree in fetch_trees_from_path(_path):
        all_names.extend(find_all_names_in_tree(tree))

    return flat([split_snake_case_to_words(name)
                 for name in all_names
                 if not is_magic_name(name)])


def receive_function_names_in_path(_path):
    function_names = []
    for tree in fetch_trees_from_path(_path):
        function_names.extend(find_function_names_in_tree(tree))
    return [f_name for f_name in function_names if not is_magic_name(f_name)]


def receive_function_verbs_in_path(_path):
    return flat([extract_verbs_from_snake_case(function_name)
                 for function_name
                 in receive_function_names_in_path(_path)])


def get_top_words_in_path(_path, top_size=10):
    all_words = receive_names_in_path(_path)
    return collections.Counter(all_words).most_common(top_size)


def get_top_verbs_in_path(_path, top_size=10):
    all_verbs = receive_function_verbs_in_path(_path)
    return collections.Counter(all_verbs).most_common(top_size)


def get_top_functions_names_in_path(_path, top_size=10):
    all_function_names = receive_function_names_in_path(_path)
    return collections.Counter(all_function_names).most_common(top_size)


if __name__ == '__main__':
    from pprint import pprint
    from sys import argv

    pprint(get_top_words_in_path(argv[1], top_size=7))
    pprint(get_top_verbs_in_path(argv[1], top_size=5))
    pprint(get_top_functions_names_in_path(argv[1]))
