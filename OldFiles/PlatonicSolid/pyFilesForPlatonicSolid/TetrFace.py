import math
import numpy as np


def tetr_face_coord(radius):
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


def tetr_face_distance(a, b):
    n = 15
    return round(((a[0] - b[0])**2 + (a[1] - b[1])**2 + (a[2] - b[2])**2)**0.5, n)


def tetr_face_mid_pt(a, b):
    n = 15
    return [round((a[0]+b[0])/2, n), round((a[1]+b[1])/2, n), round((a[2]+b[2])/2, n)]


def tetr_face_COM_coord(a, b, c):
    n = 10
    mid_a = tetr_face_mid_pt(b, c)
    mid_b = tetr_face_mid_pt(a, c)
    mid_c = tetr_face_mid_pt(a, b)
    COM_a = []
    COM_b = []
    COM_c = []
    for i in range(0, 3):
        COM_a.append(round(a[i] + (mid_a[i] - a[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_b.append(round(b[i] + (mid_b[i] - b[i]) /
                     (1+math.sin(30/180*math.pi)), 12))
        COM_c.append(round(c[i] + (mid_c[i] - c[i]) /
                     (1+math.sin(30/180*math.pi)), 12))

    if COM_a == COM_b and COM_b == COM_c:
        return COM_a
    else:
        return COM_a


def tetr_face_COM_list_gen(radius):
    coord = tetr_face_coord(radius)
    COM_list = []
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[2]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[2], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[0], coord[1], coord[3]))
    COM_list.append(tetr_face_COM_coord(coord[1], coord[2], coord[3]))
    return COM_list


def tetr_face_COM_leg_coord(a, b, c):
    COM_leg = []
    COM_leg.append(tetr_face_COM_coord(a, b, c))
    COM_leg.append(tetr_face_mid_pt(a, b))
    COM_leg.append(tetr_face_mid_pt(b, c))
    COM_leg.append(tetr_face_mid_pt(c, a))
    return COM_leg


def tetr_face_COM_leg_list_gen(radius):
    coord = tetr_face_coord(radius)
    COM_leg_list = []
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[2]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[2], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[0], coord[1], coord[3]))
    COM_leg_list.append(tetr_face_COM_leg_coord(coord[1], coord[2], coord[3]))
    return COM_leg_list


def tetr_face_leg_reduce(COM, leg, sigma):
    n = 12
    angle = math.acos(1/3)
    red_len = sigma/(2*math.sin(angle/2))
    ratio = 1 - red_len/tetr_face_distance(COM, leg)
    leg_red = []
    for i in range(0, 3):
        leg_red.append(round((leg[i] - COM[i])*ratio + COM[i], n))
    return leg_red


def tetr_face_leg_reduce_coord_gen(radius, sigma):
    COM_leg_list = tetr_face_COM_leg_list_gen(radius)
    COM_leg_red_list = []
    for elements in COM_leg_list:
        temp_list = []
        temp_list.append(elements[0])
        i = 1
        while i <= 3:
            temp_list.append(tetr_face_leg_reduce(
                elements[0], elements[i], sigma))
            i += 1
        COM_leg_red_list.append(temp_list)
    return COM_leg_red_list


def tetr_face_angle_cal(COM1, leg1, COM2, leg2):
    n = 8
    c1 = np.array(COM1)
    p1 = np.array(leg1)
    c2 = np.array(COM2)
    p2 = np.array(leg2)
    v1 = p1 - c1
    v2 = p2 - c2
    sig1 = p1 - p2
    sig2 = -sig1
    theta1 = round(math.acos(np.dot(v1, sig1) /
                   (np.linalg.norm(v1)*np.linalg.norm(sig1))), n)
    theta2 = round(math.acos(np.dot(v2, sig2) /
                   (np.linalg.norm(v2)*np.linalg.norm(sig2))), n)
    t1 = np.cross(v1, sig1)
    t2 = np.cross(v1, c1)  # n1 = c1 here
    t1_hat = t1/np.linalg.norm(t1)
    t2_hat = t2/np.linalg.norm(t2)
    phi1 = round(math.acos(np.around(np.dot(t1_hat, t2_hat), n)), n)
    t3 = np.cross(v2, sig2)
    t4 = np.cross(v2, c2)  # n2 = c2 here
    t3_hat = t3/np.linalg.norm(t3)
    t4_hat = t4/np.linalg.norm(t4)
    phi2 = round(math.acos(np.around(np.dot(t3_hat, t4_hat), n)), n)
    t1_ = np.cross(sig1, v1)
    t2_ = np.cross(sig1, v2)
    t1__hat = t1_/np.linalg.norm(t1_)
    t2__hat = t2_/np.linalg.norm(t2_)
    omega = round(math.acos(np.around(np.dot(t1__hat, t2__hat), n)), n)
    return theta1, theta2, phi1, phi2, omega


def tetr_face_input_coord(radius, sigma):
    coor = tetr_face_leg_reduce_coord_gen(radius, sigma)
    coor_ = np.array(coor[0])
    COM = coor_[0] - coor_[0]
    lg1 = coor_[1] - coor_[0]
    lg2 = coor_[2] - coor_[0]
    lg3 = coor_[3] - coor_[0]
    n = -coor_[0]
    return [COM, lg1, lg2, lg3, n]


def tetr_face(radius, sigma):
    COM, lg1, lg2, lg3, n = tetr_face_input_coord(radius, sigma)
    coord = tetr_face_leg_reduce_coord_gen(radius, sigma)
    theta1, theta2, phi1, phi2, omega = tetr_face_angle_cal(
        coord[0][0], coord[0][1], coord[2][0], coord[2][1])

    f = open('parm.inp', 'w')
    f.write(' # Input file (tetrahedron face-centered)\n\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
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
    f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
            ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
    f.write('    observeLabel = leg\n')
    f.write('    bindRadSameCom = 5.0\n')
    f.write('\n')
    f.write('end reactions\n')

    f = open('tetr.mol', 'w')
    f.write('##\n')
    f.write('# Tetrahedron (face-centered) information file.\n')
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
