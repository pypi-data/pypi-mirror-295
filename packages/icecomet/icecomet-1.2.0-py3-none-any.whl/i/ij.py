def ij(a,mode=None):
    if mode is None or mode =='':
        print(f'\033[92mค่า : {a}\033[0m')
    elif mode == 'l':
        print(f'\033[92mจำนวน : {len(a)}\033[0m')
    elif mode == 't':
        print(f'\033[92mประเภท : {type(a)}\033[0m')
    elif mode == 'o':
        pass
    return a