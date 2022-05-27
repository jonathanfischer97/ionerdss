import numpy as np
import math

def angles_new(COM1, COM2, leg1, leg2, n1, n2):
    n = 8
    c1 = np.array(COM1)
    p1 = np.array(leg1)
    c2 = np.array(COM2)
    p2 = np.array(leg2)
    n1 = np.array(n1)
    n2 = np.array(n2)
    v1 = p1 - c1
    v2 = p2 - c2
    sig1 = p1 - p2
    sig2 = -sig1
    theta1 = round(math.acos(np.dot(v1, sig1)/(np.linalg.norm(v1)*np.linalg.norm(sig1))), n)
    theta2 = round(math.acos(np.dot(v2, sig2)/(np.linalg.norm(v2)*np.linalg.norm(sig2))), n)

    t1 = np.cross(v1, sig1)
    t2 = np.cross(v1, n1)
    t1_hat = t1/np.linalg.norm(t1)
    t2_hat = t2/np.linalg.norm(t2)
    phi1 = round(math.acos(np.around(np.dot(t1_hat, t2_hat), n)), n)
    t3 = np.cross(v2, sig2)
    t4 = np.cross(v2, n2)
    t3_hat = t3/np.linalg.norm(t3)
    t4_hat = t4/np.linalg.norm(t4)
    phi2 = round(math.acos(np.around(np.dot(t3_hat, t4_hat), n)), n)
    v1xt1 = np.cross(v1, t1)
    

    t1_ = np.cross(sig1, v1)
    t2_ = np.cross(sig1, v2)
    t1__hat = t1_/np.linalg.norm(t1_)
    t2__hat = t2_/np.linalg.norm(t2_)
    print(np.dot(t1__hat, t2__hat))
    omega = round(math.acos(np.around(np.dot(t1__hat, t2__hat), n)), n)
    
    return theta1, theta2, phi1, phi2, omega