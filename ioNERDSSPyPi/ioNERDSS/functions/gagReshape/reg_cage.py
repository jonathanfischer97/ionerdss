import numpy as np
import pandas as pd
from .calculate_rmsd import *
from .calculate_gradient import *
from .determine_gagTemplate_structure import *
from .translate_gags_on_sphere import *
from .xyz_to_sphere_coordinates import *
from .restart_pdb_to_df import *
from .gag_write_PDB import *
from ..database_PDB.dtb_PDB_separate_read import *
from ..database_PDB.dtb_PDB_write_PDB import *
from .plot_3D_sites import *


def reg_cage(PathName: str):
    positions = fake_PDB_pdb_to_df(PathName)
    positions = positions[["Protein_Name","Cite_Name","x_coord", "y_coord", "z_coord"]]

    # convert coordinate unit from angstrom to nm
    positions["x_coord"] = positions["x_coord"]/10.0
    positions["y_coord"] = positions["y_coord"]/10.0
    positions["z_coord"] = positions["z_coord"]/10.0

    # get the number of monomers
    monomer_count = 0
    for i in range(len(positions)):
        if(positions.iloc[i]["Cite_Name"] == "COM"):
            monomer_count += 1
    
    # get count of interfaces for each monomer
    interfaces_count = []
    count = 0
    for i in range(len(positions)):
        count += 1
        if(positions.iloc[i]["Cite_Name"] == "COM"):
            count = 0
        if(i+1 == len(positions) or positions.iloc[i+1]["Cite_Name"] == "COM"):
            interfaces_count.append(count)
    interfaces_count = np.array(interfaces_count)

    # get the index of the COM
    COM_index = []
    curr_index = 0
    for i in range(len(interfaces_count)):
        COM_index.append(curr_index)
        curr_index += (interfaces_count[i]+1)
    #plot_3D_sites(positionsVec, COM_index)

    # sort the sites in the order of increasing distance from the COM of each monomer.
    distances = []
    for i in range(monomer_count):
        COM_coord = [positions.iloc[COM_index[i]]["x_coord"], positions.iloc[COM_index[i]]["y_coord"], positions.iloc[COM_index[i]]["z_coord"]]
        distances.append(0)
        for j in range(interfaces_count[i]):
            interface_coord = [positions.iloc[COM_index[i]+j+1]["x_coord"], positions.iloc[COM_index[i]+j+1]["y_coord"], positions.iloc[COM_index[i]+j+1]["z_coord"]]
            distances.append(np.linalg.norm(np.array(COM_coord)-np.array(interface_coord)))
    positions["Distance"] = distances

    for i in range(monomer_count):
        for j in range(COM_index[i], COM_index[i+1] if i+1 < len(COM_index) else len(positions)):
            for k in range(j, COM_index[i+1] if i+1 < len(COM_index) else len(positions)):
                if(positions.iloc[j]["Distance"] > positions.iloc[k]["Distance"]):
                    temp = positions.iloc[j]
                    positions.iloc[j] = positions.iloc[k]
                    positions.iloc[k] = temp
    
    # record the positions of the COM and interfaces of each monomer in a np array
    positionsVec = np.zeros([len(positions),3])
    for i in range(len(positions)):
        positionsVec[i,:] = [positions.iloc[i]["x_coord"], positions.iloc[i]["y_coord"], positions.iloc[i]["z_coord"]]

    # get the coordinates of the COM
    centersVec = np.zeros([monomer_count,3])
    for i in range(len(COM_index)):
        centersVec[i] = positionsVec[COM_index[i]]
    
    ##############################################
    # find the sphere radius and the sphere center
    ##############################################
    sphereXYZR = [0,0,0,70] # initial trial values for sphere x, y, z, and R respectively 
    rmsdOld = calculate_rmsd(centersVec,sphereXYZR)
    isForceSmallEnough = False
    while isForceSmallEnough == False :
        force = calculate_gradient(centersVec,sphereXYZR)
        stepSize = 1.0
        tempXYZR = sphereXYZR - force * stepSize
        rmsdNew = calculate_rmsd(centersVec,tempXYZR)
        while rmsdNew > rmsdOld :
            stepSize = stepSize * 0.8
            tempXYZR = sphereXYZR - force * stepSize
            rmsdNew = calculate_rmsd(centersVec,tempXYZR)
        sphereXYZR = tempXYZR
        rmsdOld = calculate_rmsd(centersVec,sphereXYZR)
        if ( np.linalg.norm(force) < 0.01 ):
            isForceSmallEnough = True

    print('Sphere center position [x,y,z] and radius [R] are, respectively: \n',sphereXYZR) 
    x0 = sphereXYZR[0] 
    y0 = sphereXYZR[1] 
    z0 = sphereXYZR[2] 
    r0 = sphereXYZR[3] 

    ##############################################
    # Second, move the center of the sphere to the axis origin, equivalently move the monomers 
    positionsVec[:,0] = positionsVec[:,0] - x0
    positionsVec[:,1] = positionsVec[:,1] - y0
    positionsVec[:,2] = positionsVec[:,2] - z0
    centersVec[:,0] = centersVec[:,0] - x0
    centersVec[:,1] = centersVec[:,1] - y0
    centersVec[:,2] = centersVec[:,2] - z0

    ##############################################
    # Third, move the centers of monomers to the sphere surface
    for i in range (0,monomer_count):
        center = centersVec[i,:]
        move = center/np.linalg.norm(center) * r0 - center
        centersVec[i,:] = centersVec[i,:] + move
        for j in range (0,interfaces_count[i]):
            positionsVec[COM_index[i] + j + 1,:] = positionsVec[COM_index[i] + j + 1,:] + move

    plot_3D_sites(positionsVec, COM_index)
    
    for i in range(len(positions)):
        positions.at[i,"x_coord"] = positionsVec[i,0]
        positions.at[i,"y_coord"] = positionsVec[i,1]
        positions.at[i,"z_coord"] = positionsVec[i,2]
    

    ##############################################
    # Determine the regulation coefficients and apply the regulation to the monomers
    ##############################################
    # find the "full monomers"
    # monomers that have all interfaces recorded in the PDB file are considered as full monomers
    full_monomer_COM_index = []
    full_interfaces_count = np.max(interfaces_count)
    for i in range(monomer_count):
        if(interfaces_count[i] == full_interfaces_count):
            full_monomer_COM_index.append(COM_index[i])
    full_monomer_count = len(full_monomer_COM_index)

    # generate a np array to record the coordinates of the COM and interfaces of the full monomers
    full_monomer_positionsVec = np.zeros([full_monomer_count*(full_interfaces_count+1),3])
    for i in range(full_monomer_count):
        for j in range(full_interfaces_count+1):
            full_monomer_positionsVec[i*(full_interfaces_count+1)+j] = positionsVec[full_monomer_COM_index[i]+j,:]
    

    full_monomer_COM_index_graph = []
    for i in range(full_monomer_count):
        full_monomer_COM_index_graph.append(i*(full_interfaces_count+1))
    

    plot_3D_sites(full_monomer_positionsVec, full_monomer_COM_index_graph)

    # Determine the regularized coefficients. All monomers will be reshaped according to this template
    # monomerTemplate is the positions of the gag center and five interfaces
    # monomerTemplateInterCoeffs is the coefficients of the gag 5 interfaces in the internal basis system
    numSites = full_interfaces_count + 1
    monomerCoeff = determine_gagTemplate_structure(full_monomer_count, numSites, full_monomer_positionsVec, returnCoeff = True)
    print(monomerCoeff)    

    # set up the internal coordinate system of the first monomer: 3 basis vecs: interBaseVec0, interBaseVec1, interBaseVec2
    regularized_positionsVec = np.zeros([full_monomer_count*(numSites),3])
    for i in range(0,full_monomer_count):
        center = full_monomer_positionsVec[numSites*i,:]                                            # center of the monomer
        interBaseVec0 = center / np.linalg.norm(center)                   # along the radius direction
        interBaseVec1 = full_monomer_positionsVec[i*numSites+1,:] - center          # in the direction of the first interface
        interBaseVec2 = np.cross(interBaseVec0,interBaseVec1)               # orthogonal to the first two basis vecs
        interBaseVec2 = interBaseVec2 / np.linalg.norm(interBaseVec2) 
        interBaseVec1 = np.cross(interBaseVec2,interBaseVec0)
        interBaseVec1 = interBaseVec1 / np.linalg.norm(interBaseVec1)
        regularized_positionsVec[numSites*i,:] = center
        for j in range (0,numSites-1) :
            regularized_positionsVec[numSites*i+j+1,:] = center + interBaseVec0 * monomerCoeff[j,0] + interBaseVec1 * monomerCoeff[j,1] + interBaseVec2 * monomerCoeff[j,2]

    plot_3D_sites(regularized_positionsVec, full_monomer_COM_index_graph)

    # update the coordinates of the full monomers
    for i in range(full_monomer_count):
        for j in range(full_interfaces_count+1):
            positionsVec[full_monomer_COM_index[i]+j,:] = regularized_positionsVec[i*(full_interfaces_count+1)+j,:]
    
    plot_3D_sites(positionsVec, COM_index)
    return positionsVec
