import numpy as np

def find_nearest_site(siteCoord, positionsVec, COM_index, interfaces_count):
    min_distance = 100000000
    nearest_site_index = -1 
    nearest_COM_index = -1
    for i in range(len(COM_index)):
        for j in range(interfaces_count[i]):
            distance = np.linalg.norm(siteCoord - positionsVec[COM_index[i]+j+1])
            if distance < 1e-9:
                continue
            if distance < min_distance:
                min_distance = distance
                nearest_site_index = COM_index[i]+j+1
                nearest_COM_index = COM_index[i]
    return positionsVec[nearest_COM_index], positionsVec[nearest_site_index]
    