def dodecahedron_coord(radius):
    
    print('radius = ', radius)
    
    # Setup coordinates of 20 verticies when scaler = 1
    scaler = radius/(3**0.5)
    m = (1+5**(0.5))/2
    V0 = [0, m, 1/m]
    V1 = [0, m, -1/m]
    V2 = [0, -m, 1/m]
    V3 = [0, -m, -1/m]
    V4 = [1/m, 0, m]
    V5 = [1/m, 0, -m]
    V6 = [-1/m, 0, m]
    V7 = [-1/m, 0, -m]
    V8 = [m, 1/m, 0]
    V9 = [m, -1/m, 0]
    V10 = [-m, 1/m, 0]
    V11 = [-m, -1/m, 0]
    V12 = [1, 1, 1]
    V13 = [1, 1, -1]
    V14 = [1, -1, 1]
    V15 = [1, -1, -1]
    V16 = [-1, 1, 1]
    V17 = [-1, 1, -1]
    V18 = [-1, -1, 1]
    V19 = [-1, -1, -1]
    coord = [V0, V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19]
    
    # calculate coordinates according to the scaler as coord_ (list)
    coord_ = []
    for i in coord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        coord_.append(temp_list)
    return coord_


def distance(a, b):
    # a seperated function for calculating the distance between two coordinates
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)

def mid_pt(a, b):
    # this is a seperate function for calculating mid point of two coords
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]

from numpy import *

def COM_leg(COM, a, b, c):
    lega = mid_pt(COM, a)
    legb = mid_pt(COM, b)
    legc = mid_pt(COM, c)
    return [around(COM, 10), around(lega, 10), around(legb, 10), around(legc, 10)]

def COM_leg_gen(radius):
    coord = dodecahedron_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(COM_leg(coord[0], coord[1], coord[12], coord[16]))
    COM_leg_list.append(COM_leg(coord[1], coord[0], coord[13], coord[17]))
    COM_leg_list.append(COM_leg(coord[2], coord[3], coord[14], coord[18]))
    COM_leg_list.append(COM_leg(coord[3], coord[2], coord[15], coord[19]))
    COM_leg_list.append(COM_leg(coord[4], coord[6], coord[12], coord[14]))
    COM_leg_list.append(COM_leg(coord[5], coord[7], coord[13], coord[15]))
    COM_leg_list.append(COM_leg(coord[6], coord[4], coord[16], coord[18]))
    COM_leg_list.append(COM_leg(coord[7], coord[5], coord[17], coord[19]))
    COM_leg_list.append(COM_leg(coord[8], coord[9], coord[12], coord[13]))
    COM_leg_list.append(COM_leg(coord[9], coord[8], coord[14], coord[15]))
    COM_leg_list.append(COM_leg(coord[10], coord[11], coord[16], coord[17]))
    COM_leg_list.append(COM_leg(coord[11], coord[10], coord[18], coord[19]))
    COM_leg_list.append(COM_leg(coord[12], coord[0], coord[4], coord[8]))
    COM_leg_list.append(COM_leg(coord[13], coord[1], coord[5], coord[8]))
    COM_leg_list.append(COM_leg(coord[14], coord[2], coord[4], coord[9]))
    COM_leg_list.append(COM_leg(coord[15], coord[3], coord[5], coord[9]))
    COM_leg_list.append(COM_leg(coord[16], coord[0], coord[6], coord[10]))
    COM_leg_list.append(COM_leg(coord[17], coord[1], coord[7], coord[10]))
    COM_leg_list.append(COM_leg(coord[18], coord[2], coord[6], coord[11]))
    COM_leg_list.append(COM_leg(coord[19], coord[3], coord[7], coord[11]))
    return COM_leg_list

def COM_leg_valid(radius):
    COM_leg_list = COM_leg_gen(radius)
    leg_pool = []
    count = 0
    for i in COM_leg_list:
        for j in range(len(i)):
            if j != 0:
                if list(i[j]) not in leg_pool:
                    count += 1
                    leg_pool.append(list(i[j]))
    print('Number of leg = ', count, '(should be 30)')


def leg_reduce(COM, leg, sigma):   
    red_len = sigma/2
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red
                
def leg_reduce_valid(a, b, c, d, sigma):
    # validate the reduced length of legs is correct
    n = 8
    result_1 = leg_reduce(a, b, sigma)
    result_2 = leg_reduce(c, d, sigma)
    dis = distance(result_1, result_2)
    print('Actual distance: ', round(dis, 8))
    print('Assigned sigma: ', sigma)
    if round(dis, n) == sigma:
        print('Result match!\n')
    else:
        print('Result does not match!\n')

def leg_reduce_coor_gen(radius, sigma):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(leg_reduce(elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    print('Number of elements in list: ', len(COM_leg_red_list), '(should be 20)\n')
    return COM_leg_red_list

from mpl_toolkits.mplot3d import axes3d  
import matplotlib.pyplot as plt  
 
# visualize the model
def sig_vis(list, ax):
    for i in range(1, 4):
        figure = ax.plot([list[0][0], list[i][0]], [list[0][1], list[i][1]], [list[0][2], list[i][2]])

def vis(lst):
    fig = plt.figure(1)  
    ax = fig.gca(projection='3d')
    for element in lst:
        sig_vis(element, ax) 
    
    plt.show()

if __name__ == '__main__':
    lst = leg_reduce_coor_gen(radius = 10, sigma = 1)
    vis(lst)