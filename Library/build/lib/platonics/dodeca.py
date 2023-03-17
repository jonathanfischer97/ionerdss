#!/usr/bin/env python
# coding: utf-8

# In[17]:


def dodecahedron_coord(radius):
    
    # Set the edge length of the cube inside the orthodecahedron
    print('radius = ', radius)
    
    # Setup coordinates of 20 verticies when scaler = 1
    scaler = radius/(3**0.5)
    m = (1+5**(0.5))/2
    V1 = [0, m, 1/m]
    V2 = [0, m, -1/m]
    V3 = [0, -m, 1/m]
    V4 = [0, -m, -1/m]
    V5 = [1/m, 0, m]
    V6 = [1/m, 0, -m]
    V7 = [-1/m, 0, m]
    V8 = [-1/m, 0, -m]
    V9 = [m, 1/m, 0]
    V10 = [m, -1/m, 0]
    V11 = [-m, 1/m, 0]
    V12 = [-m, -1/m, 0]
    V13 = [1, 1, 1]
    V14 = [1, 1, -1]
    V15 = [1, -1, 1]
    V16 = [1, -1, -1]
    V17 = [-1, 1, 1]
    V18 = [-1, 1, -1]
    V19 = [-1, -1, 1]
    V20 = [-1, -1, -1]
    coord = [V1, V2, V3, V4, V5, V6, V7, V8, V9, V10, V11, V12, V13, V14, V15, V16, V17, V18, V19, V20]
    
    # calculate coordinates according to the scaler as coord_ (list)
    coord_ = []
    for i in coord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        coord_.append(temp_list)
    return coord_

if __name__ == '__main__':
    print(dodecahedron_coord(radius = 10))


# In[18]:


import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot(radius):
    # Visualize the dodecahedron model
    coord = dodecahedron_coord(radius)
    X = []
    Y = []
    Z = []
    for i in coord:
        X.append(i[0])
        Y.append(i[1])
        Z.append(i[2])
    fig = plt.figure()
    ax = plt.subplot(projection='3d')
    ax.scatter(X, Y, Z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()
    
if __name__ == '__main__':
    plot(radius = 10)


# In[19]:


def distance(a, b):
    # a seperated function for calculating the distance between two coordinates
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)

if __name__ == '__main__':
    print(distance([0, 0, 0], [1, 1, 1]))


# In[20]:


def comp_len(radius):
    # this function is for validate the correctness of dode. model
    coord = dodecahedron_coord(radius)
    n = 12
    # calculate the length of all 30 edges
    len_E = []
    len_E.append(round(distance(coord[0], coord[1]),14))
    len_E.append(round(distance(coord[0], coord[12]),14))
    len_E.append(round(distance(coord[0], coord[16]),14))
    len_E.append(round(distance(coord[1], coord[13]),14))
    len_E.append(round(distance(coord[1], coord[17]),14))
    len_E.append(round(distance(coord[2], coord[3]),14))
    len_E.append(round(distance(coord[2], coord[14]),14))
    len_E.append(round(distance(coord[2], coord[18]),14))
    len_E.append(round(distance(coord[3], coord[15]),14))
    len_E.append(round(distance(coord[3], coord[19]),14))
    len_E.append(round(distance(coord[4], coord[6]),14))
    len_E.append(round(distance(coord[4], coord[12]),14))
    len_E.append(round(distance(coord[4], coord[14]),14))
    len_E.append(round(distance(coord[5], coord[7]),14))
    len_E.append(round(distance(coord[5], coord[13]),14))
    len_E.append(round(distance(coord[5], coord[15]),14))
    len_E.append(round(distance(coord[6], coord[16]),14))
    len_E.append(round(distance(coord[6], coord[18]),14))
    len_E.append(round(distance(coord[7], coord[17]),14))
    len_E.append(round(distance(coord[7], coord[19]),14))
    len_E.append(round(distance(coord[8], coord[9]),14))
    len_E.append(round(distance(coord[8], coord[12]),14))
    len_E.append(round(distance(coord[8], coord[13]),14))
    len_E.append(round(distance(coord[9], coord[14]),14))
    len_E.append(round(distance(coord[9], coord[15]),14))
    len_E.append(round(distance(coord[10], coord[11]),14))
    len_E.append(round(distance(coord[10], coord[16]),14))
    len_E.append(round(distance(coord[10], coord[17]),14))
    len_E.append(round(distance(coord[11], coord[18]),14))
    len_E.append(round(distance(coord[11], coord[19]),14))
    
    # validate total number of edges
    print('All elements in list:')
    for i in len_E:
        print(i)
    print('Length: ', len_E[0])
    print('Count: ', len(len_E))
    print('E = 30 for dodecahedron')
    
    # check if all lengths are identical
    status = 1
    for i in range(0, len(len_E)):
        for j in range(i, len(len_E)):
            if round(len_E[i], n) != round(len_E[j], n):
                status = 0
                break
    if status == 1:
        print('Lengths match!')
        return len_E[0]
    else:
        print('Lengths do not match!')
        return 0
          
    
if __name__ == '__main__':
    comp_len(radius = 10)


# In[21]:


def mid_pt(a, b):
    # this is a seperate function for calculating mid point of two coords
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]

if __name__ == '__main__':
    print(mid_pt([1, 2, 3], [4, 5, 6]))


# In[22]:


import math

def COM_coor(a, b, c, d, e):
    # calculate the center of mass(COM) according to 5 coords on the same face
    n = 10
    mid_a = mid_pt(c, d)
    mid_b = mid_pt(d, e)
    mid_c = mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    # calculate 3 COM here and check if they are overlapped
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i])/(1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i])/(1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i])/(1+math.sin(0.3*math.pi)), 14))
        
    # checking overlap
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        print('COM coordinates match!')
        return COM_a
    else:
        print('COM coordinates do not match!')
        print(COM_a)
        print(COM_b)
        print(COM_c)
        return COM_a
    
if __name__ == '__main__':
    coord = dodecahedron_coord(radius = 10)
    print(COM_coor(coord[3], coord[15], coord[9], coord[14], coord[2]))
    


# In[23]:


def COM_list_gen(radius):
    # generate the list of COM of all 12 faces
    coord = dodecahedron_coord(radius)
    COM_list = []
    COM_list.append(COM_coor(coord[6], coord[18], coord[2], coord[14], coord[4]))
    COM_list.append(COM_coor(coord[6], coord[4], coord[12], coord[0], coord[16]))
    COM_list.append(COM_coor(coord[4], coord[14], coord[9], coord[8], coord[12]))
    COM_list.append(COM_coor(coord[6], coord[18], coord[11], coord[10], coord[16]))
    COM_list.append(COM_coor(coord[14], coord[2], coord[3], coord[15], coord[9]))
    COM_list.append(COM_coor(coord[18], coord[11], coord[19], coord[3], coord[2]))
    COM_list.append(COM_coor(coord[16], coord[10], coord[17], coord[1], coord[0]))
    COM_list.append(COM_coor(coord[12], coord[0], coord[1], coord[13], coord[8]))
    COM_list.append(COM_coor(coord[7], coord[17], coord[10], coord[11], coord[19]))
    COM_list.append(COM_coor(coord[5], coord[13], coord[8], coord[9], coord[15]))
    COM_list.append(COM_coor(coord[3], coord[19], coord[7], coord[5], coord[15]))
    COM_list.append(COM_coor(coord[1], coord[17], coord[7], coord[5], coord[13]))
    return COM_list

if __name__ == '__main__':
    result = COM_list_gen(radius = 10)
    print(result)


# In[24]:


def COM_leg_coor(a, b, c, d, e):
    # calculate COM and 5 legs of one protein, 6 coords in total [COM, lg1, lg2, lg3, lg4, lg5]
    COM_leg = []
    COM_leg.append(COM_coor(a, b, c, d, e))
    COM_leg.append(mid_pt(a, b))
    COM_leg.append(mid_pt(b, c))
    COM_leg.append(mid_pt(c, d))
    COM_leg.append(mid_pt(d, e))
    COM_leg.append(mid_pt(e, a))
    return COM_leg

if __name__ == '__main__':
    print(COM_leg_coor(coord[6], coord[18], coord[2], coord[14], coord[4]))


# In[25]:


def COM_leg_list_gen(radius):
    # generate all COM and leg coords of 12 faces as a large list
    coord = dodecahedron_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(COM_leg_coor(coord[6], coord[18], coord[2], coord[14], coord[4]))
    COM_leg_list.append(COM_leg_coor(coord[6], coord[4], coord[12], coord[0], coord[16]))
    COM_leg_list.append(COM_leg_coor(coord[4], coord[14], coord[9], coord[8], coord[12]))
    COM_leg_list.append(COM_leg_coor(coord[6], coord[18], coord[11], coord[10], coord[16]))
    COM_leg_list.append(COM_leg_coor(coord[14], coord[2], coord[3], coord[15], coord[9]))
    COM_leg_list.append(COM_leg_coor(coord[18], coord[11], coord[19], coord[3], coord[2]))
    COM_leg_list.append(COM_leg_coor(coord[16], coord[10], coord[17], coord[1], coord[0]))
    COM_leg_list.append(COM_leg_coor(coord[12], coord[0], coord[1], coord[13], coord[8]))
    COM_leg_list.append(COM_leg_coor(coord[7], coord[17], coord[10], coord[11], coord[19]))
    COM_leg_list.append(COM_leg_coor(coord[5], coord[13], coord[8], coord[9], coord[15]))
    COM_leg_list.append(COM_leg_coor(coord[3], coord[19], coord[7], coord[5], coord[15]))
    COM_leg_list.append(COM_leg_coor(coord[1], coord[17], coord[7], coord[5], coord[13]))
    return COM_leg_list

def COM_leg_list_valid(radius):
    # to validate if the coords of legs overlaps with each other
    result = COM_leg_list_gen(radius)
    count = 0
    pool = []
    for i in result:
        for j in range(1, 6):
            if i[j] not in pool:
                pool.append(i[j])
                count += 1
    print('Number of faces: ', len(COM_leg_list_gen(radius)))
    print('Total number of non-repetitive interfaces: ', count, '(should be 30)')

if __name__ == '__main__':
    COM_leg_list_valid(radius = 10)


# In[26]:


def leg_reduce(COM, leg, sigma):
    # calculate the recuced length when considering the sigma value
    n = 14
    m = (1+5**(0.5))/2
    angle = 2*math.atan(m)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red

def leg_reduce_valid(a, b, c, d, sigma):
    # validate the reduced length of legs is correct
    n = 10
    result_1 = leg_reduce(a, b, sigma)
    result_2 = leg_reduce(c, d, sigma)
    dis = distance(result_1, result_2)
    print('Actual distance: ', round(dis, n))
    print('Assigned sigma: ', sigma)
    if round(dis, n) == sigma:
        print('Result match!\n')
    else:
        print('Result does not match!\n')

if __name__ == '__main__':
    coord = COM_leg_list_gen(radius = 10)
    leg_reduce_valid(coord[0][0], coord[0][3], coord[4][0], coord[4][1], 0.1)
    leg_reduce_valid(coord[5][0], coord[5][2], coord[8][0], coord[8][4], 0.01)
    leg_reduce_valid(coord[1][0], coord[1][4], coord[6][0], coord[6][5], 0.04)


# In[27]:


def leg_reduce_coor_gen(radius, sigma):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(leg_reduce(elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    print('Number of elements in list: ', len(COM_leg_red_list), '(should be 12)\n')
    return COM_leg_red_list

if __name__ == '__main__':
    result = leg_reduce_coor_gen(radius = 10, sigma = 1)
    for i in result:
        print(i, '\n')


# In[28]:


from mpl_toolkits.mplot3d import axes3d  
import matplotlib.pyplot as plt  
 
# visualize the model
def sig_vis(list, ax):
    for i in range(1, 6):
        figure = ax.plot([list[0][0], list[i][0]], [list[0][1], list[i][1]], [list[0][2], list[i][2]])

def vis(list):
    fig = plt.figure(1)  
    ax = fig.gca(projection='3d')
    for element in list:
        sig_vis(element, ax) 
    plt.show()

if __name__ == '__main__':
    list = leg_reduce_coor_gen(radius = 10, sigma = 1)
    vis(list)


# In[29]:


import numpy as np

# matrix calculation test
a = [2, 3, 4]
b = [1, 0, 6]
a_ = np.array(a)
b_ = np.array(b)

print(a_, b_)

print(np.dot(a, b))

print(np.cross(a, b))

print(np.linalg.norm(a))


# In[30]:


# import sympy

# def solve_norm(a, b, c):
#     n = 14
#     a1 = b[0] - a[0]
#     a2 = b[1] - a[1]
#     a3 = b[2] - a[2]
#     b1 = c[0] - a[0]
#     b2 = c[1] - a[1]
#     b3 = c[2] - a[2]
#     x = sympy.symbols('x')
#     y = sympy.symbols('y')
#     z = sympy.symbols('z')
#     # n = [x, y, z]
#     result = sympy.solve([a1*x+a2*y+a3*z, b1*x+b2*y+b3*z, x**2+y**2+z**2-1], [x, y, z])
#     norm = []
#     for i in range (0, 2):
#         temp = []
#         for j in range (0, 3):
#             temp.append(round(result[i][j], n))
#         norm.append(temp)
            
#     return norm[0]

# if __name__ == '__main__':
#     coord = leg_reduce_coor_gen()
#     print(solve_norm(coord[0][0], coord[0][1], coord[0][2]))
#     print(solve_norm(coord[0][0], coord[0][2], coord[0][3]))
#     print(solve_norm(coord[0][0], coord[0][3], coord[0][4]))
#     print(solve_norm(coord[0][0], coord[0][4], coord[0][5]))
#     print(solve_norm(coord[0][0], coord[0][5], coord[0][1]))


# In[31]:


import numpy as np

# calculating the 5 angles according to the coords of legs and COM
# see SI of the NERDSS paper II part for detail
def angle_cal(COM1, leg1, COM2, leg2):
    n = 8
    c1 = np.array(COM1)
    p1 = np.array(leg1)
    c2 = np.array(COM2)
    p2 = np.array(leg2)
    v1 = p1 - c1
    v2 = p2 - c2
    sig1 = p1 - p2
    sig2 = -sig1
    theta1 = round(math.acos(np.dot(v1, sig1)/(np.linalg.norm(v1)*np.linalg.norm(sig1))), n)
    theta2 = round(math.acos(np.dot(v2, sig2)/(np.linalg.norm(v2)*np.linalg.norm(sig2))), n)
    print('-----------------------')
    print('theta1 = ', round(theta1/math.pi, n), 'pi')
    print('theta2 = ', round(theta2/math.pi, n), 'pi')

    t1 = np.cross(v1, sig1)
    t2 = np.cross(v1, c1) # n1 = c1 here
    t1_hat = t1/np.linalg.norm(t1)
    t2_hat = t2/np.linalg.norm(t2)
    phi1 = round(math.acos(np.around(np.dot(t1_hat, t2_hat), n)), n)
    t3 = np.cross(v2, sig2)
    t4 = np.cross(v2, c2) # n2 = c2 here
    t3_hat = t3/np.linalg.norm(t3)
    t4_hat = t4/np.linalg.norm(t4)
    phi2 = round(math.acos(np.around(np.dot(t3_hat, t4_hat), n)), n)
    print('phi1 = ', round(phi1/math.pi, n), 'pi')
    print('phi2 = ', round(phi2/math.pi, n), 'pi')

    t1_ = np.cross(sig1, v1)
    t2_ = np.cross(sig1, v2)
    t1__hat = t1/np.linalg.norm(t1)
    t2__hat = t2/np.linalg.norm(t2)
    omega = round(math.acos(np.around(np.dot(t1__hat, t2__hat), n)), n)
    print('omega = ', round(omega/math.pi, n), 'pi')
    
    print('COM1 = ', COM1)
    print('COM2 = ', COM2)
    print('leg1 = ', leg1)
    print('leg2 = ', leg2)
    print('c1 = ', c1)
    print('c2 = ', c2)
    
    return theta1, theta2, phi1, phi2, omega

if __name__ == '__main__':
    coord = leg_reduce_coor_gen(radius = 10, sigma = 1)
    print(angle_cal(coord[0][0], coord[0][3], coord[4][0], coord[4][1]))
#     print(angle_cal(coord[5][0], coord[5][2], coord[8][0], coord[8][4]))
#     print(angle_cal(coord[1][0], coord[1][4], coord[6][0], coord[6][5]))


# In[36]:


# calculate coordinates of normalized COM and legs
def input_coord(radius, sigma):

    coor = leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    lg4 = coor_[4] - coor_[0]
    lg5 = coor_[5] - coor_[0]
    n = -coor_[0]
    
    print('COM = ', COM)
    print('lg1 = ', lg1)
    print('lg2 = ', lg2)
    print('lg3 = ', lg3)
    print('lg4 = ', lg4)
    print('lg5 = ', lg5)
    print('n   = ', n)
    
    return COM, lg1, lg2, lg3, lg4, lg5, n

if __name__ == '__main__':
    input_coord(radius = 10, sigma = 1)


# In[37]:


def dode_face_main(radius, sigma):
    COM, lg1, lg2, lg3, lg4, lg5, n = input_coord(radius, sigma)
    theta1, theta2, phi1, phi2, omega = angle_cal(coord[0][0], coord[0][3], coord[4][0], coord[4][1])
    print('\n------------------------------------------')
    print('output:')
    print('COM = ', COM)
    print('lg1 = ', lg1)
    print('lg2 = ', lg2)
    print('lg3 = ', lg3)
    print('lg4 = ', lg4)
    print('lg5 = ', lg5)
    print('n = ', n)
    print('theta1 = ', theta1)
    print('theta2 = ', theta2)
    print('phi1 = ', phi1)
    print('phi2 = ', phi2)
    print('omega = ', omega)

if __name__ == '__main__':
    dode_face_main(radius = 10, sigma = 1)   


# In[39]:


dode_face_main(10, 1)


# In[38]:


# After simulation in nerdss, obtain coordinates by pymol from trajectory.xyz
f1 = [[-94.799629, -81.177841, -31.289844],
      [-92.815157, -84.259188, -31.343076],
      [-94.848075, -82.497384, -34.709218],
      [-96.814042, -78.912016, -33.349902],
      [-95.996159, -78.457942, -29.143655],
      [-93.524712, -81.762676, -27.903368]]
f2 = [[-91.765086, -81.372770, -37.855986],
      [-88.374444, -82.093512, -39.047515],
      [-90.845890, -78.788778, -40.287802],
      [-94.587634, -79.055033, -38.167402],
      [-94.428712, -82.524322, -35.616637],
      [-90.588749, -84.402205, -36.160576]]
f3 = [[-88.351237, -84.331342, -32.203273],
      [-88.793604, -84.076362, -28.573540],
      [-85.051860, -83.810107, -30.693940],
      [-85.869744, -84.264181, -34.900186],
      [-90.116967, -84.811070, -35.379391],
      [-91.924012, -84.694992, -31.469308]]
f4 = [[-95.066505, -75.351916, -35.573306],
      [-93.268102, -74.371349, -38.613026],
      [-93.977657, -71.874837, -35.173319],
      [-96.191962, -74.183530, -32.286381],
      [-96.850923, -78.106893, -33.941862],
      [-95.043878, -78.222972, -37.851944]]
f5 = [[-88.783051, -74.904797, -39.134061],
      [-90.433783, -77.894926, -40.464427],
      [-86.186560, -77.348037, -39.985223],
      [-85.527599, -73.424674, -38.329741],
      [-89.367562, -71.546791, -37.785802],
      [-92.399750, -74.309558, -39.105110]]
f6 = [[-84.632787, -80.454387, -37.051266],
      [-85.355866, -83.728399, -35.570162],
      [-82.323678, -80.965631, -34.250854],
      [-82.482600, -77.496342, -36.801619],
      [-85.613008, -78.114971, -39.697387],
      [-87.388784, -81.966594, -38.936305]]
f7 = [[-86.560747, -73.671014, -27.705098],
      [-83.738199, -75.988751, -27.393682],
      [-87.479943, -76.255007, -25.273283],
      [-89.951389, -72.950272, -26.513570],
      [-87.737084, -70.641579, -29.400508],
      [-83.897121, -72.519462, -29.944447]]
f8 = [[-83.526204, -73.865942, -34.271241],
      [-85.510675, -70.784595, -34.218009],
      [-84.801121, -73.281107, -37.657716],
      [-82.329674, -76.585842, -36.417430],
      [-81.511791, -76.131768, -32.211183],
      [-83.477758, -72.546400, -30.851866]]
f9 = [[-89.974596, -70.712441, -33.357811],
      [-88.208866, -70.232714, -30.181694],
      [-92.456089, -70.779603, -30.660898],
      [-93.273973, -71.233677, -34.867145],
      [-89.532229, -70.967421, -36.987544],
      [-86.401821, -70.348792, -34.091776]]
f10 = [[-83.259329, -79.691868, -29.987779],
       [-84.348177, -83.168948, -30.387766],
       [-85.057731, -80.672436, -26.948059],
       [-83.281955, -76.820813, -27.709141],
       [-81.474910, -76.936891, -31.619223],
       [-82.133871, -80.860254, -33.274704]]
f11 = [[-93.693046, -74.589396, -28.509819],
       [-95.843233, -77.547441, -28.759465],
       [-96.002155, -74.078152, -31.310231],
       [-92.969966, -71.315385, -29.990922],
       [-90.937049, -73.077190, -26.624779],
       [-92.712825, -76.928812, -25.863697]]
f12 = [[-89.542782, -80.138987, -26.427024],
       [-92.798234, -81.619110, -27.231344],
       [-92.139273, -77.695747, -25.575862],
       [-87.892050, -77.148858, -25.096658],
       [-85.926083, -80.734226, -26.455975],
       [-88.958272, -83.496993, -27.775283]]
void = [[-90, -76, -30], [-90, -76, -30], [-90, -76, -30], [-90, -76, -30], [-90, -76, -30], [-90, -76, -30]]

# find opposite faces by visualize them
coord_list = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]
# f1&f8
vis([f1, void, void, void, void, void, void, f8, void, void, void, void])
# f2&f7
vis([void, f2, void, void, void, void, f7, void, void, void, void, void])
# f3&f9
vis([void, void, f3, void, void, void, void, void, f9, void, void, void])
# f4&f10
vis([void, void, void, f4, void, void, void, void, void, f10, void, void])
# f5&f12
vis([void, void, void, void, f5, void, void, void, void, void, void, f12])
# f6&f11
vis([void, void, void, void, void, f6, void, void, void, void, f11, void])


# In[35]:


# f1&f8
# f2&f7
# f3&f9
# f4&f10
# f5&f12
# f6&f11

# validate original point (center of dodechehedron) overlap
print('coordinate of center')
print(mid_pt(f1[0], f8[0]))
print(mid_pt(f2[0], f7[0]))
print(mid_pt(f3[0], f9[0]))
print(mid_pt(f4[0], f10[0]))
print(mid_pt(f5[0], f12[0]))
print(mid_pt(f6[0], f11[0]))
print('--------------------')

# validate the distance between legs and original point is the same
print('distance from center to legs')
coord_list = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12]
count = 0
for face in coord_list:
    for i in range(1, 6):
        count += 1
        print(round(distance([-89.162917, -77.521892, -32.780543], face[i]), 6))
print('count = ', count, '(should be 12*5=60)')


# In[ ]:





# In[ ]:




