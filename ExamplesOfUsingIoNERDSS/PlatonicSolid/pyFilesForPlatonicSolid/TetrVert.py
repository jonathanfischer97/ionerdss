import numpy as np


def tetr_vert_coord(radius):
    scaler = radius/(3/8)**0.5/2
    v0 = [1, 0, -1/2**0.5]
    v1 = [-1, 0, -1/2**0.5]
    v2 = [0, 1, 1/2**0.5]
    v3 = [0, -1, 1/2**0.5]
    VertCoord = [v0, v1, v2, v3]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def tetr_vert_distance(a, b):
    # a seperated function for calculating the distance between two coordinates
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)


def tetr_vert_mid_pt(a, b):
    # this is a seperate function for calculating mid point of two coords
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]


def tetr_vert_COM_leg(COM, a, b, c):
    lega = tetr_vert_mid_pt(COM, a)
    legb = tetr_vert_mid_pt(COM, b)
    legc = tetr_vert_mid_pt(COM, c)
    return [np.around(COM, 10), np.around(lega, 10), np.around(legb, 10), np.around(legc, 10)]


def tetr_vert_COM_leg_gen(radius):
    coord = tetr_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[0], coord[1], coord[2], coord[3]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[1], coord[2], coord[3], coord[0]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[2], coord[3], coord[0], coord[1]))
    COM_leg_list.append(tetr_vert_COM_leg(
        coord[3], coord[0], coord[1], coord[2]))
    return COM_leg_list


def tetr_vert_leg_reduce(COM, leg, sigma):
    red_len = sigma/2
    ratio = 1 - red_len/tetr_vert_distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def tetr_vert_leg_reduce_coor_gen(radius, sigma):
    # Generating all the coords of COM and legs when sigma exists
    COM_leg_list = tetr_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def tetr_vert_input_coord(radius, sigma):
    coor = tetr_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 8)
    lg1 = np.around(coor_[1] - coor_[0], 8)
    lg2 = np.around(coor_[2] - coor_[0], 8)
    lg3 = np.around(coor_[3] - coor_[0], 8)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 8)
    return COM, lg1, lg2, lg3, n


def tetr_vert_norm_input(radius, sigma):
    COM, lg1, lg2, lg3, n = tetr_vert_input_coord(radius, sigma)
    length = tetr_vert_distance(lg1, lg2)
    dis1 = ((-length/2)**2+(-((length/2)*(3**0.5))/3)**2)**0.5
    dis2 = tetr_vert_distance(COM, lg1)
    height = (dis2**2-dis1**2)**0.5
    lg1_ = np.array([-length/2, -((length/2)*(3**0.5))/3, -height])
    lg2_ = np.array([length/2, -((length/2)*(3**0.5))/3, -height])
    lg3_ = np.array([0, ((length/2)*(3**0.5))/3*2, -height])
    COM_ = np.array([0, 0, 0])
    n_ = np.array([0, 0, 1])
    return COM_, lg1_, lg2_, lg3_, n_


def tetr_vert(radius, sigma):
    COM, lg1, lg2, lg3, n = tetr_vert_norm_input(radius, sigma)

    f = open('parm.inp', 'w')
    f.write(' # Input file (tetrahedron vertex-centered)\n\n')
    f.write('start parameters\n')
    f.write('    nItr = 10000000 #iterations\n')
    f.write('    timeStep = 0.1\n')
    f.write('    timeWrite = 10000\n')
    f.write('    pdbWrite = 10000\n')
    f.write('    trajWrite = 10000\n')
    f.write('    restartWrite = 50000\n')
    f.write('    checkPoint = 1000000\n')
    f.write('    overlapSepLimit = 7.0\n')
    f.write('end parameters\n\n')
    f.write('start boundaries\n')
    f.write('    WaterBox = [500,500,500]\n')
    f.write('end boundaries\n\n')
    f.write('start molecules\n')
    f.write('    tetr : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    tetr(lg1) + tetr(lg1) <-> tetr(lg1!1).tetr(lg1!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg2) <-> tetr(lg2!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg3) + tetr(lg3) <-> tetr(lg3!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 2\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg2) <-> tetr(lg1!1).tetr(lg2!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg1) + tetr(lg3) <-> tetr(lg1!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('    tetr(lg2) + tetr(lg3) <-> tetr(lg2!1).tetr(lg3!1)\n')
    f.write('    onRate3Dka = 4\n')
    f.write('    offRatekb = 2\n')
    f.write('    norm1 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    norm2 = [' + str(n[0]) + ', ' +
            str(n[1]) + ', ' + str(n[2]) + ']\n')
    f.write('    sigma = ' + str(float(sigma)) + '\n')
    f.write('    assocAngles = [M_PI, M_PI, nan, nan, 0]\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('tetr.mol', 'w')
    f.write('##\n')
    f.write('# Tetrahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = tetr\n')
    f.write('checkOverlap = true\n\n')
    f.write('# translational diffusion constants\n')
    f.write('D = [13.0, 13.0, 13.0]\n\n')
    f.write('# rotational diffusion constants\n')
    f.write('Dr = [0.03, 0.03, 0.03]\n\n')
    f.write('# Coordinates\n')
    f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
            str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
    f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
            str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
    f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
            str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
    f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
            str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 3\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('\n')
