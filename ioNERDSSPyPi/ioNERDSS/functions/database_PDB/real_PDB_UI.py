import math
import numpy as np
import sys
import copy
from .gen.real_PDB_angles import real_PDB_angles
from .gen.real_PDB_norm_check import real_PDB_norm_check
from .gen.real_PDB_norm_input import real_PDB_norm_input
from .gen.real_PDB_mag import real_PDB_mag
from .PDB_object import ProteinComplex

def real_PDB_UI():
    """A user friendly UI to allow for open, minupulating, and then outputting .pdb files.

    Functions:
    
    Open .pdb files:
     - When run, the first thing that will be asked is "Enter pdb file name: []". You must enter the relative / absolute path to the file.
     - Ex: Enter pdb file name: "ioNERDSSPyPi\TestingFunctions\\1si4.pdb" (Note: I have to '\' before 1, so python does not see it as a weird charecter)
    Chaning distance between interaction sites:
     - After the .pdb file in initilized, it will ask "Would you like to chang...", and ask for you to write 'yes' or 'no'
     - If you write yes, keep reading, if you write no, it will just go to the next section
     - Than it will ask 'which distance' you want to change, and ask for an integer between 0-X. 
        - 0: means all distances will be set to the same number you input
        - 1+: That distance will be set to the number inputted. You can find which 'distance' each number refers to by reading and counting down the 
        list of Interaction Sites (which is directly above). 1 = the furthest up.
     - Then enter the new distance.
     - Then the initial message will come up again, and repeats this whol process.
    'Normalizing':
     - It will then ask if you want to see the 'default norm vector to (0,0,1)'. Write 'yes' or 'no' if you do or don't
     - It will then ask if you want each molecule's center of mass to be 0,0,0
     - The UI will then spit out the necessary .mol and .inp files to setup a NERDSS simulation

    If you want to make graphs / new .pdb files, you will need to use the 'seperate' commands instead of the UI.
    """
    # naming explanation:
    # variables with word 'total' in the front indicate that it's a list of data for the whole protein
    # variables with word 'split' in the front indicate that it's a list containing n sub-lists and each sub-list contains
    # data for different chains. (n is the number of chains)

    file_name = input("Enter pdb file name: ")
    UI_PDB = ProteinComplex(file_name)
    

    # user can choose to change the interaction site
    while True:
        answer = input(
            "Would you like to change the distance between interaction site (Type 'yes' or 'no'): ")
        if answer == "no":
            print("Calculation is completed.")
            break
        if answer == "yes":
            while True:
                n = int(input("Which distance would you like to change (please enter an integer no greater than %.0f or enter 0 to set all distance to a specific number): " % (
                    len(UI_PDB.int_site_distance)))) - 1
                if n in range(-1, len(UI_PDB.int_site_distance)):
                    while True:
                        new_distance = float(
                            input("Please enter new distance: "))
                        # decreasing distance & increasing distance
                        if new_distance >= 0:
                            if n == -1:
                                SiteList = range(0, len(UI_PDB.reaction_chain))
                                NewSigma = []
                                for na in range(0, len(UI_PDB.reaction_chain)):
                                    NewSigma.append(new_distance)
                                UI_PDB.change_sigma(ChangeSigma=True, SiteList = SiteList, NewSigma = NewSigma)
                                break
                            if n >= 0:
                                UI_PDB.change_sigma(ChangeSigma=True, SiteList = [n], NewSigma = [new_distance])
                                break
                        else:
                            print('Invalid number, please try again.')
                            break
                    break
                else:
                    print("Invalid answer, please try again.")
                    break
        else:
            print("Invalid answer, please try again.")

    # ditermine sigma
    # calculating angles
    angle = []
    normal_point_lst1 = []
    normal_point_lst2 = []

    while True:
        answer_norm = str(
            input("Would you like to use the default norm vector (0,0,1)? (Type 'yes' or 'no'): "))
        if answer_norm == 'yes' or answer_norm == 'no':
            break

    # type in norm
    if answer_norm == 'no':
        value = True 
        while value:
            answer_norm_2 = input("What do you want the norm vector to be? Please insert with a , between each number and no spaces. (ex: 1,1,3)")
            answer_norm_2 = answer_norm_2.split(',')
            answer_norm_2 = [float(ele) for ele in answer_norm_2]
            value = not UI_PDB.calc_angle(answer_norm_2,False)

    # generate norm
    if answer_norm == 'yes':
        UI_PDB.calc_angle()

    # asking whether to center the COM of every chain to origin.
    while True:
        answer2 = input(
            "Do you want each chain to be centered at center of mass? (Type 'yes' or 'no'): ")
        if answer2 == "yes":
            for i in range(len(unique_chain)):
                for k in range(len(reaction_chain)):
                    for j in range(2):
                        if unique_chain[i] == reaction_chain[k][j]:
                            for l in range(3):
                                new_int_site[k][j][l] = new_int_site[k][j][l] - COM[i][l]
                                # angle[k][j+6][l] = angle[k][j+6][l] - COM[i][l]
                for m in range(3):
                    COM[i][m] = 0.0
            break
        if answer2 == "no":
            break
        else:
            print("Invalid answer, please try again.")

    # writing parameters into a file

    f = open("parm.inp", "w")
    f.write(" # Input file\n\n")
    f.write("start parameters\n")
    f.write("    nItr = 1000000\n")
    f.write("    timestep = 0.1\n\n\n")
    f.write("    timeWrite = 500\n")
    f.write("    trajWrite = 500\n")
    f.write("    pdbWrite = 500\n")
    f.write("    restartWrite = 50000\n")
    f.write("    fromRestart = false\n")
    f.write("end parameters\n\n")
    f.write("start boundaries\n")
    f.write("    WaterBox = [494,494,494] #nm\n")
    f.write("    implicitLipid = false\n")
    f.write("    xBCtype = reflect\n")
    f.write("    yBCtype = reflect\n")
    f.write("    zBCtype = reflect\n")
    f.write("end boundaries\n\n")
    f.write("start molecules\n")
    for i in range(len(unique_chain)):
        f.write("     %s:100\n" % (unique_chain[i]))
    f.write("end molecules\n\n")
    f.write("start reactions\n")
    for i in range(len(reaction_chain)):
        molecule1_lower = reaction_chain[i][0].lower()
        molecule2_lower = reaction_chain[i][1].lower()
        f.write("    #### %s - %s ####\n" %
                (reaction_chain[i][0], reaction_chain[i][1]))
        f.write("    %s(%s) + %s(%s) <-> %s(%s!1).%s(%s!1)\n" % (reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower,
                                                                 reaction_chain[i][0], molecule2_lower,
                                                                 reaction_chain[i][1], molecule1_lower))
        f.write("    onRate3Dka = 10\n")
        f.write("    offRatekb = 1\n")
        f.write("    sigma = %f\n" % angle[i][5])
        f.write("    norm1 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst1[i][0], normal_point_lst1[i][1], normal_point_lst1[i][2]))
        f.write("    norm2 = [%.6f,%.6f,%.6f]\n" % (
            normal_point_lst2[i][0], normal_point_lst2[i][1], normal_point_lst2[i][2]))
        if reaction_chain[i][0] in one_site_chain:
            angle[i][2] = 'nan'
        if reaction_chain[i][1] in one_site_chain:
            angle[i][3] = 'nan'
        f.write("    assocAngles = [" + str(angle[i][0]) + "," + str(angle[i][1]) + "," + str(
            angle[i][2]) + "," + str(angle[i][3]) + "," + str(angle[i][4]) + "\n\n")
    f.write("end reactions")
    f.close()

    for i in range(len(unique_chain)):
        mol_file = str(unique_chain[i]) + '.mol'
        f = open(mol_file, "w")
        f.write("##\n# %s molecule information file\n##\n\n" % unique_chain[i])
        f.write("Name    = %s\n" % unique_chain[i])
        f.write("checkOverlap = true\n\n")
        f.write("# translational diffusion constants\n")
        f.write("D       = [12.0,12.0,12.0]\n\n")
        f.write("# rotational diffusion constants\n")
        f.write("Dr      = [0.5,0.5,0.5]\n\n")
        f.write("# Coordinates, with states below, or\n")
        f.write("COM     %.4f    %.4f    %.4f\n" %
                (COM[i][0], COM[i][1], COM[i][2]))
        reaction_chain_merged = []
        chain_string = []
        bond_counter = 0
        for a in range(len(reaction_chain)):
            for b in range(2):
                reaction_chain_merged.append(reaction_chain[a][b])
        if unique_chain[i] not in reaction_chain_merged:
            break
        if unique_chain[i] in reaction_chain_merged:
            bond_counter = 0
            for m in range(len(reaction_chain)):
                if unique_chain[i] == reaction_chain[m][0]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][1])
                    chain_string.append(chain_name.lower())
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][0][0], new_int_site[m][0][1], new_int_site[m][0][2]))
                elif unique_chain[i] == reaction_chain[m][1]:
                    bond_counter += 1
                    chain_name = str(reaction_chain[m][0])
                    f.write("%s       %.4f    %.4f    %.4f\n" % (chain_name.lower(
                    ), new_int_site[m][1][0], new_int_site[m][1][1], new_int_site[m][1][2]))
                    chain_string.append(chain_name)
        f.write("\nbonds = %d\n" % bond_counter)
        for j in range(bond_counter):
            f.write("COM %s\n" % chain_string[j])
    return 0

# --------------------------------------Seperated functions (same as above)----------------------------------------


