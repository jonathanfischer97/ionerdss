# This function will calculate five necessary angles: theta_one, theta_two, phi_one, phi_two and omega
# Input variables: four coordinates indicating COM and interaction site of two chains
# First created by Yian Qian
# Modified by Mankun Sang on 04/13/2022 
#   1) unit of zero vector and length-one vector
#   2) error messages when v // n
#   3) test scripts
# Modified by Yian Qian & Mankun Sang on 04/16/2022
#   0) correct omega calculation when n // sigma
#   1) generalize the sign determination of phi and omega
#   2) created a function for phi cacluation


import numpy as np
import math

eps = 10**-6
norm = np.linalg.norm

def unit(x:np.ndarray) -> np.ndarray:
    '''Get the unit vector of x\n
    Return 0 if ||x||=0\n
    Return itself if ||x||=1'''
    x_norm = norm(x)
    if abs(x_norm-1) < eps:
        return x
    elif x_norm < eps:
        return np.zeros(3)
    else:
        return x/x_norm


def triangle_correction(x: float) -> float:
    '''make x in range of [-1, 1], correct precision'''
    if x < -1 and abs(x+1) < eps:
        return -1
    elif x > 1 and abs(x-1) < eps:
        return 1
    elif -1 <= x <= 1:
        return x
    else:
        raise ValueError(f'{x} is out of the range of sin/cos')

def calculate_phi(v:np.ndarray, n:np.ndarray, sigma:np.ndarray) -> float:

    # calculate phi
    t1 = unit(np.cross(v, sigma))
    t2 = unit(np.cross(v, n))
    phi = math.acos(triangle_correction(np.dot(t1, t2)))

    # determine the sign of phi (+/-)
    v_uni = unit(v)
    n_proj = n - v_uni * np.dot(v_uni, n)
    sigma_proj = sigma - v_uni * np.dot(v_uni, sigma)
    phi_dir = unit(np.cross(sigma_proj, n_proj))

    if np.dot(v_uni, phi_dir) > 0:
        phi = -phi
    else:
        phi = phi
    
    return phi


def angles(COM1, COM2, int_site1, int_site2, normal_point1, normal_point2):
    '''Calculate the angles for binding'''

    # Convert sequences into arrays for convinience
    COM1 = np.array(COM1)
    COM2 = np.array(COM2)
    int_site1 = np.array(int_site1)
    int_site2 = np.array(int_site2)
    normal_point1 = np.array(normal_point1)
    normal_point2 = np.array(normal_point2)

    # Get Vectors
    v1 = int_site1 - COM1 # from COM to interface (particle 1)
    v2 = int_site2 - COM2  # from COM to interface (particle 2)
    sigma1 = int_site1 - int_site2 # sigma, from p2 to p1
    sigma2 = int_site2 - int_site1  # sigma, from p1 to p2
    n1 = unit(normal_point1 - COM1) # normal vector for p1
    n2 = unit(normal_point2 - COM2) # normal vector for p2

    # Calculate the magnititude of sigma
    sigma_magnitude = norm(sigma1)

    # Calculate theta1 and theta2
    costheta1 = np.dot(v1, sigma1) / norm(v1) / norm(sigma1)
    costheta2 = np.dot(v2, sigma2) / norm(v2) / norm(sigma2)
    theta1 = math.acos(triangle_correction(costheta1))
    theta2 = math.acos(triangle_correction(costheta2))

    # check geometry
    errormsg = ''
    iferror = False # determine if v // n
    if norm(np.cross(n1, v1)) < eps:
        iferror = True
        errormsg += '\n\tn1 and v1 parallel, phi1 not available'
    if norm(np.cross(n2, v2)) < eps:
        iferror = True
        errormsg += '\n\tn2 and v2 parallel, phi2 not available'
    if iferror:
        raise ValueError(errormsg)

    # determine if phi1 exists (v1 // sigma1 ?)
    if norm(np.cross(sigma1, v1)) < eps:
        phi1 = float('nan')
        # omega_parallel = True
        omega_t1 = unit(np.cross(sigma1, n1))
    else:
        phi1 = calculate_phi(v1, n1, sigma1)
        omega_t1 = unit(np.cross(sigma1, v1))

    # determine if phi2 exists (v2 // sigma2 ?)
    if norm(np.cross(sigma2, v2)) < eps:
        phi2 = float('nan')
        # omega_parallel = True
        omega_t2 = unit(np.cross(sigma1, n2))
    else:
        phi2 = calculate_phi(v2, n2, sigma2)
        omega_t2 = unit(np.cross(sigma1, v2))

    # calculate omega (both cases are same)
    omega = math.acos(triangle_correction(np.dot(omega_t1, omega_t2)))
    # determine the sign of omega (+/-)
    sigma1_uni = unit(sigma1)
    sigma1xomega_t1 = np.cross(sigma1, omega_t1)
    sigma1xomega_t2 = np.cross(sigma1, omega_t2)
    omega_dir = unit(np.cross(sigma1xomega_t1, sigma1xomega_t2))
    if np.dot(sigma1_uni, omega_dir) > 0:
        omega = -omega
    else:
        omega = omega

    return theta1, theta2, phi1, phi2, omega, sigma_magnitude

if __name__ == '__main__':

    sq3 = np.sqrt(3)

    COM1 = np.array([3, 3*sq3, 0])
    # int_site1 = np.array([11/2, 13/sq3/2, 0])
    int_site1 = np.array([0.5, 3*sq3, 0])
    normal_point1 = np.array([3, 3*sq3, 1])
    
    # COM2 = np.array([6,0,0])
    # int_site2 = np.array([6, 5/sq3, 0])
    # normal_point2 = np.array([6, 0, -1])
    COM2 = np.array([-3,3*sq3,0])
    int_site2 = np.array([-0.5, 3*sq3, 0])
    normal_point2 = np.array([-3, 3*sq3, -1])

    print(int_site1 - COM1, normal_point1 - COM1)
    print(int_site2 - COM2, normal_point2 - COM2)

    inner_angle = angles(COM1, COM2, int_site1, int_site2, normal_point1, normal_point2)
    print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % inner_angle)
