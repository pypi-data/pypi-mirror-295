
def info_print():
    print(ct.green+"ij(string,'lti')  cprint(string,ct.color)   ct:color")


# modul cprint :--> class color_text : ct.  cprint(string)
#############################################################################################

class color_text:
    def __init__(self) -> None:
        self.gray = '\033[90m'
        self.red = '\033[91m'
        self.green = '\033[92m'
        self.yello = '\033[93m'
        self.blue = '\033[94m'
        self.magenta = '\033[95m'
        self.sky = '\033[96m'
        self.white = '\033[97m'


        self.grayk = '\033[100m'
        self.redk = '\033[101m'
        self.greenk = '\033[102m'
        self.yellok = '\033[103m'
        self.bluek = '\033[104m'
        self.magentak = '\033[105m'
        self.skyk = '\033[106m'
        self.whitek = '\033[107m'

        self.set = '\033[0m'
        self.ijset = '\033[92m'
        self.jiset = '\033[93m'
    def show(self):
        print(f"{self.gray}gray {self.red}red {self.green}green {self.yello}yello {self.blue}blue {self.magenta}magenta {self.sky}sky {self.white}white {self.set}")
        print(f"{self.grayk}gray {self.redk}red {self.greenk}green {self.yellok}yello {self.bluek}blue {self.magentak}magenta {self.skyk}sky {self.whitek}white {self.set}")


ct = color_text()


def cprint(string='',color=ct.greenk):
    print(f'{color}{string}{ct.set}')





# modul II :--> debug :ij  ji  show_color()
#############################################################################################
ij_round = 0
ji_round = 0

def ij(a='',mode=None,c=ct.ijset,end='\n'):
    global ij_round
    if a=='':
        print(c+'Passed : '+str(ij_round)+ct.set,end=end)
        ij_round += 1
    elif mode is None or mode =='':
        print(f'{c}{a}'+ct.set,end=end)
        return a
    else :
        for i in mode:
            if i == 'l':
                print(f'{c}จำนวน : {len(a)}'+ct.set,end=end)
            elif i == 't':
                print(f'{c}ประเภท : {type(a)}'+ct.set,end=end)
            elif i == 'i':
                print(f'{c}{a}'+ct.set,end=end)
        return a
def ji(a='',c=ct.jiset,end='\n'):
    global ji_round
    print(c+f"Tag '{a}' Passed : "+str(ji_round)+ct.set,end=end)
    ji_round += 1

def show_color():
    for i in range(200):
        print(f'\033[{i}m{i}'+ct.set)
        if i %10 ==0:
            print('')
#############################################################################################



