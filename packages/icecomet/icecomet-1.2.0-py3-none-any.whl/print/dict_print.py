from iprint import *

def dict_print(dict={},number_in_line=5,space_index=1,space_value=10):
    k = list(dict.keys())
    l = list(dict.values())
    a=space_index
    b=space_value
    for k,i in enumerate(k):
        k+=1
        ij(ct.green+f'{i:>{a}} --> {dict[i]:<{b}}',end='')
        if k%number_in_line == 0:
            print()
    print()
