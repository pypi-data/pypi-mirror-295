
def ij(a,mode=None,c='\033[92m'):
    if mode is None or mode =='':
        print(f'{c}ค่า : {a}\033[0m')
        return a
    else :
        for i in mode:
            if i == 'l':
                print(f'{c}จำนวน : {len(a)}\033[0m')
            elif i == 't':
                print(f'{c}ประเภท : {type(a)}\033[0m')
            elif i == 'i':
                print(f'{c}ค่า : {a}\033[0m')
        return a