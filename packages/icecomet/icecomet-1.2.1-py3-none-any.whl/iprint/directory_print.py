

def directory_print(example, indent='', last=True):
    for i, (key, value) in enumerate(example.items()):
        connector = '└── ' if last and i == len(example) - 1 else '├── '
        print(f"{indent}{connector}{key}/")

        new_indent = indent + ('    ' if last and i == len(example) - 1 else '│   ')

        if isinstance(value, dict):
            directory_print(value, new_indent, last=True)
        elif isinstance(value, list):
            for j, item in enumerate(value):
                sub_connector = '└── ' if j == len(value) - 1 else '├── '
                if isinstance(item, dict):
                    for k, (sub_key, sub_value) in enumerate(item.items()):
                        sub_connector = '└── ' if k == len(item) - 1 else '├── '
                        print(f"{new_indent}{sub_connector}{sub_key}/")
                        directory_print({sub_key: sub_value}, new_indent + '│   ', last=(k == len(item) - 1))
                else:
                    print(f"{new_indent}{sub_connector}{item}")



example = {
    'A': ['a', 'b'],
    'C': ['f', {'D':['ui','ai'],'E':['ui','ai']},'jio'],
    'B': ['c', 'd', 'e']
}


# directory_print(example)


