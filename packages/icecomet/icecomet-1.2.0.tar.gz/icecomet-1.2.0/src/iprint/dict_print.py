from iprint import ij,ct

class dpN_confix():
    def __init__(self):
        self.number_in_line = 5
        self.space_index = 2
        self.space_value = 10

dp_confix = dpN_confix()

def dict_print(dict={}):
    global dp_confix
    k = list(dict.keys())
    l = list(dict.values())
    a=dp_confix.space_index
    b=dp_confix.space_value
    for k,i in enumerate(k):
        k+=1
        
        ij(ct.green+f'{i:>{a}} --> {dict[i]:<{b}}',end='')
        if k%dp_confix.number_in_line == 0:
            print()
    print()

    
