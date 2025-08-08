import random


def print_list(
    list_to_print: list,
    title: str = None,
    bullet_point: str = "•",
    max_items: int = None,
    randomize: bool = False,
    indent_level: int = 0,
) -> None:
    """
    Prints a list nicely. Handles sublists. Tupples will be displayed as items: ('e1', 'e2', ...).
    Author: Valérien BRAYE (@brayevalerien on github)
    Args:
        list_to_print (list): the list to be printed
        title (str, optional): title of the list. Defaults to None.
        bullet_point (str, optional): character to used for the bullet points. Defaults to "•".
        max_items (int, optional): maximum number of items to print, longer list will be elapsed with "...". Defaults to None.
        randomize (bool, optional): randomize the order of the items or not. Defaults to False.
        indent_level (int, optional): indentation level for sub-lists. Defaults to 0.
    """
    if title:
        print(f"{indent_level * '  '}{title}:")
        indent_level += 1
    final_list_to_print = list_to_print.copy()
    if randomize:
        random.shuffle(final_list_to_print)
    if max_items:
        final_list_to_print = list_to_print[:max_items]
    for item in final_list_to_print:
        if isinstance(item, list):
            print_list(item, bullet_point=bullet_point, indent_level=indent_level + 1)
        elif isinstance(item, tuple):
            print(f"{indent_level * '  '}{bullet_point} {str(item)}")
        else:
            print(f"{indent_level * '  '}{bullet_point} {item}")
    if len(final_list_to_print) != len(list_to_print):
        print(f"{indent_level * '  '}...")


def print_dict(
    dict_to_print: dict,
    title: str = None,
    bullet_point: str = "•",
    max_items: int = None,
    randomize: bool = False,
    indent_level: int = 0,
) -> None:
    """
    Prints a dictionary nicely. Handles subdicts. List will be printed nicely aswell. Tupples will be displayed as items: ('e1', 'e2', ...).
    Author: Valérien BRAYE (@brayevalerien on github)
    Args:
        dict_to_print (dict): the dict to be printed
        title (str, optional): title of the dict. Defaults to None.
        bullet_point (str, optional): character to used for the bullet points. Defaults to "•".
        max_items (int, optional): maximum number of items to print, longer dict will be elapsed with "...". Defaults to None.
        randomize (bool, optional): randomize the order of the items or not. Defaults to False.
        indent_level (int, optional): indentation level for sub-dicts. Defaults to 0.
    """
    if max_items is None:
        max_items = len(dict_to_print)
    if title:
        print(f"{indent_level * '  '}{title}:")
        indent_level += 1
    final_dict_to_print = dict_to_print.copy()
    dict_keys = list(final_dict_to_print.keys())
    if randomize:
        random.shuffle(dict_keys)
    final_dict_to_print = {key: final_dict_to_print[key] for key in dict_keys[:max_items]}
    for key in final_dict_to_print.keys():
        item = dict_to_print[key]
        if isinstance(item, dict):
            print_dict(item, bullet_point=bullet_point, indent_level=indent_level + 1)
        elif isinstance(item, tuple):
            print(f"{indent_level * '  '}{bullet_point} {key}: {str(item)}")
        elif isinstance(item, list):
            print(f"{indent_level * '  '}{bullet_point} {key}:")
            print_list(item, bullet_point=bullet_point, indent_level=indent_level + 1)
        else:
            print(f"{indent_level * '  '}{bullet_point} {key}: {item}")
    if len(final_dict_to_print) != len(dict_to_print):
        print(f"{indent_level * '  '}...")
