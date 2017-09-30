from argparse import ArgumentParser
import ast
import collections
import os

from helpers import (is_verb,
                     flat,
                     split_snake_case_to_words,
                     is_magic_name)


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


def get_top_words_in_path(path, top=10):
    all_words = receive_names_in_path(path)
    return collections.Counter(all_words).most_common(top)


def get_top_verbs_in_path(path, top=10):
    all_verbs = receive_function_verbs_in_path(path)
    return collections.Counter(all_verbs).most_common(top)


def get_top_functions_names_in_path(path, top=10):
    all_function_names = receive_function_names_in_path(path)
    return collections.Counter(all_function_names).most_common(top)


def parse_args():
    parser = ArgumentParser(description='Calculate words occurrences in path')

    subparsers = parser.add_subparsers()

    parser_words = subparsers.add_parser(
        'words',
        help='- words occurrences')
    parser_words.add_argument('--path', help='path to parse', default='./')
    parser_words.add_argument('--top', help='top number to return', type=int)
    parser_words.set_defaults(func=get_top_words_in_path)

    parser_verbs = subparsers.add_parser(
        'verbs',
        help='- verbs occurrences')
    parser_verbs.add_argument('--path', help='path to parse', default='./')
    parser_verbs.add_argument('--top', help='top number to return', type=int)
    parser_verbs.set_defaults(func=get_top_verbs_in_path)

    parser_funcs = subparsers.add_parser(
        'functions',
        help='- function names occurrences')
    parser_funcs.add_argument('--path', help='path to parse', default='./')
    parser_funcs.add_argument('--top', help='top number to return', type=int)
    parser_funcs.set_defaults(func=get_top_functions_names_in_path)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    print(args.func(args.path, args.top))
