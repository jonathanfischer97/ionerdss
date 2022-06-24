import math
import numpy as np


def icos_vert_coord(radius):
    scaler = radius/(2*math.sin(2*math.pi/5))
    m = (1+5**0.5)/2
    v0 = [0, 1, m]
    v1 = [0, 1, -m]
    v2 = [0, -1, m]
    v3 = [0, -1, -m]
    v4 = [1, m, 0]
    v5 = [1, -m, 0]
    v6 = [-1, m, 0]
    v7 = [-1, -m, 0]
    v8 = [m, 0, 1]
    v9 = [m, 0, -1]
    v10 = [-m, 0, 1]
    v11 = [-m, 0, -1]
    VertCoord = [v0, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
    VertCoord_ = []
    for i in VertCoord:
        temp_list = []
        for j in i:
            temp = j*scaler
            temp_list.append(temp)
        VertCoord_.append(temp_list)
    return VertCoord_


def icos_vert_distance(a, b):
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)


def icos_vert_mid_pt(a, b):
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]


def icos_vert_COM_leg(COM, a, b, c, d, e):
    lega = icos_vert_mid_pt(COM, a)
    legb = icos_vert_mid_pt(COM, b)
    legc = icos_vert_mid_pt(COM, c)
    legd = icos_vert_mid_pt(COM, d)
    lege = icos_vert_mid_pt(COM, e)
    result = [np.around(COM, 10), np.around(lega, 10), np.around(
        legb, 10), np. around(legc, 10), np.around(legd, 10), np.around(lege, 10)]
    return result


def icos_vert_COM_leg_gen(radius):
    coord = icos_vert_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(icos_vert_COM_leg(
        coord[0], coord[2], coord[8], coord[4], coord[6], coord[10]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[1], coord[4], coord[6], coord[11], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[2], coord[0], coord[10], coord[7], coord[5], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[3], coord[1], coord[11], coord[7], coord[5], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[4], coord[0], coord[6], coord[1], coord[9], coord[8]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[5], coord[2], coord[8], coord[7], coord[3], coord[9]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[6], coord[0], coord[10], coord[11], coord[1], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[7], coord[3], coord[11], coord[10], coord[2], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[8], coord[0], coord[2], coord[5], coord[9], coord[4]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[9], coord[8], coord[4], coord[1], coord[3], coord[5]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[10], coord[0], coord[2], coord[7], coord[11], coord[6]))
    COM_leg_list.append(icos_vert_COM_leg(
        coord[11], coord[10], coord[7], coord[3], coord[1], coord[6]))
    return COM_leg_list


def icos_vert_leg_reduce(COM, leg, sigma):
    red_len = sigma/2
    ratio = 1 - red_len/icos_vert_distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], 8))
    return leg_red


def icos_vert_leg_reduce_coor_gen(radius, sigma):
    COM_leg_list = icos_vert_COM_leg_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 5:
            temp_list.append(icos_vert_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def icos_vert_input_coord(radius, sigma):
    coor = icos_vert_leg_reduce_coor_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = np.around(coor_[0] - coor_[0], 12)
    lg1 = np.around(coor_[1] - coor_[0], 12)
    lg2 = np.around(coor_[2] - coor_[0], 12)
    lg3 = np.around(coor_[3] - coor_[0], 12)
    lg4 = np.around(coor_[4] - coor_[0], 12)
    lg5 = np.around(coor_[5] - coor_[0], 12)
    n = np.around(coor_[0]/np.linalg.norm(coor_[0]), 12)
    return COM, lg1, lg2, lg3, lg4, lg5, n


def icos_vert_center_coor(a, b, c, d, e):
    n = 8
    mid_a = icos_vert_mid_pt(c, d)
    mid_b = icos_vert_mid_pt(d, e)
    mid_c = icos_vert_mid_pt(a, e)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(0.3*math.pi)), 14))
    if round(COM_a[0], n) == round(COM_b[0], n) and round(COM_b[0], n) == round(COM_c[0], n) and \
        round(COM_a[1], n) == round(COM_b[1], n) and round(COM_b[1], n) == round(COM_c[1], n) and \
            round(COM_a[2], n) == round(COM_b[2], n) and round(COM_b[2], n) == round(COM_c[2], n):
        return COM_a
    else:
        return COM_a


def icos_vert_check_dis(cen, COM, lg1, lg2, lg3, lg4, lg5):
    dis1 = round(icos_vert_distance(cen, lg1), 8)
    dis2 = round(icos_vert_distance(cen, lg2), 8)
    dis3 = round(icos_vert_distance(cen, lg3), 8)
    dis4 = round(icos_vert_distance(cen, lg4), 8)
    dis5 = round(icos_vert_distance(cen, lg5), 8)
    dis_ = round(icos_vert_distance(COM, cen), 8)
    if dis1 == dis2 and dis1 == dis3 and dis1 == dis4 and dis1 == dis5:
        return dis1, dis_
    else:
        return dis1, dis_


def icos_vert_norm_input(scaler, dis_):
    c1 = math.cos(2*math.pi/5)
    c2 = math.cos(math.pi/5)
    s1 = math.sin(2*math.pi/5)
    s2 = math.sin(4*math.pi/5)
    v0 = scaler*np.array([0, 1])
    v1 = scaler*np.array([-s1, c1])
    v2 = scaler*np.array([-s2, -c2])
    v3 = scaler*np.array([s2, -c2])
    v4 = scaler*np.array([s1, c1])
    lg1 = np.array([v0[0], v0[1], -dis_])
    lg2 = np.array([v1[0], v1[1], -dis_])
    lg3 = np.array([v2[0], v2[1], -dis_])
    lg4 = np.array([v3[0], v3[1], -dis_])
    lg5 = np.array([v4[0], v4[1], -dis_])
    COM = np.array([0, 0, 0])
    n = np.array([0, 0, 1])
    return COM, lg1, lg2, lg3, lg4, lg5, n


def icos_vert(radius, sigma):
    COM_, lg1_, lg2_, lg3_, lg4_, lg5_, n_ = icos_vert_input_coord(
        radius, sigma)
    cen_ = icos_vert_center_coor(lg1_, lg2_, lg3_, lg4_, lg5_)
    scaler, dis_ = icos_vert_check_dis(
        cen_, COM_, lg1_, lg2_, lg3_, lg4_, lg5_)
    COM, lg1, lg2, lg3, lg4, lg5, n = icos_vert_norm_input(scaler, dis_)

    f = open('parm.inp', 'w')
    f.write(' # Input file (icosahedron vertex-centered)\n\n')
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
    f.write('    icos : 200\n')
    f.write('end molecules\n\n')
    f.write('start reactions\n')
    f.write('    icos(lg1) + icos(lg1) <-> icos(lg1!1).icos(lg1!1)\n')
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
    f.write('    icos(lg2) + icos(lg2) <-> icos(lg2!1).icos(lg2!1)\n')
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
    f.write('    icos(lg3) + icos(lg3) <-> icos(lg3!1).icos(lg3!1)\n')
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
    f.write('    icos(lg4) + icos(lg4) <-> icos(lg4!1).icos(lg4!1)\n')
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
    f.write('    icos(lg5) + icos(lg5) <-> icos(lg5!1).icos(lg5!1)\n')
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
    f.write('    icos(lg1) + icos(lg2) <-> icos(lg1!1).icos(lg2!1)\n')
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
    f.write('    icos(lg1) + icos(lg3) <-> icos(lg1!1).icos(lg3!1)\n')
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
    f.write('    icos(lg1) + icos(lg4) <-> icos(lg1!1).icos(lg4!1)\n')
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
    f.write('    icos(lg1) + icos(lg5) <-> icos(lg1!1).icos(lg5!1)\n')
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
    f.write('    icos(lg2) + icos(lg3) <-> icos(lg2!1).icos(lg3!1)\n')
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
    f.write('    icos(lg2) + icos(lg4) <-> icos(lg2!1).icos(lg4!1)\n')
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
    f.write('    icos(lg2) + icos(lg5) <-> icos(lg2!1).icos(lg5!1)\n')
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
    f.write('    icos(lg3) + icos(lg4) <-> icos(lg3!1).icos(lg4!1)\n')
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
    f.write('    icos(lg3) + icos(lg5) <-> icos(lg3!1).icos(lg5!1)\n')
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
    f.write('    icos(lg4) + icos(lg5) <-> icos(lg4!1).icos(lg5!1)\n')
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

    f = open('icos.mol', 'w')
    f.write('##\n')
    f.write('# Icosahedron (vertex-centered) information file.\n')
    f.write('##\n\n')
    f.write('Name = icos\n')
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
    f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
            str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
    f.write('lg5   ' + str(round(lg5[0], 8)) + '   ' +
            str(round(lg5[1], 8)) + '   ' + str(round(lg5[2], 8)) + '\n')
    f.write('\n')
    f.write('# bonds\n')
    f.write('bonds = 5\n')
    f.write('com lg1\n')
    f.write('com lg2\n')
    f.write('com lg3\n')
    f.write('com lg4\n')
    f.write('com lg5\n')
    f.write('\n')
