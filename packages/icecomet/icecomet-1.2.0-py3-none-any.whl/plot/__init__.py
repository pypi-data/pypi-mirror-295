def info_plot():
    print('\033[92m'+"scatter_1list(x)   scatter_2list(x,y)")


# modul Main
################################################################################################
import matplotlib.pyplot as plt

# # สมมติว่าคุณมีลิสต์ของตัวเลข
# data = [1, 3, 2, 5, 7, 8, 5, 6, 7, 3, 5, 6, 4, 7]

# # สร้างตัวเลขลำดับสำหรับแกน X
# x_values = range(len(data))

# # สร้างกราฟการกระจาย
# plt.scatter(x_values, data)

# # เพิ่มชื่อแกน X และ Y
# plt.xlabel('x')
# plt.ylabel('y')

# # เพิ่มชื่อกราฟ
# plt.title('Scatter Plot of Data List')

# # แสดงกราฟ
# plt.show()

def scatter_1list(x,xlabel='x',ylabel='y'):
    y_values = [1]*len(x)
    plt.scatter(x, y_values)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def scatter_2list(x,y,xlabel='x',ylabel='y'):
    if  len(x) != len(y):
        print('x != y')
        return None
    plt.scatter(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def histogram(ls,range=1, alpha=0.7, color='blue',xlabel='x',ylabel='y'):
    list(ls)
    plt.hist(ls,bins=range, alpha=alpha, color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
def s():
    plt.show()
################################################################################################





