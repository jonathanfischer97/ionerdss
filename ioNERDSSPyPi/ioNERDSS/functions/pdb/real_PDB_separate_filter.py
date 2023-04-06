def real_PDB_separate_filter(Result: tuple, ChainList: list):
    """
    This function will filter the desired chain according to the input list of chain and exclude all the 
    unnecessary coordinate information for future analysis. 

    Args:
        Result (tuple): The output result of function ‘real_PDB_separate_read (FileName)’. 
        ChainList (list): The desired name of chains that users intend to examine. 

    Returns:
        A tuple that includes:
         - coms_dict: Dictionary of the COMs of each unique chain
         - dist_dict: Dictionary of the binding information between each pair of chains (including whether two chains are binded and the coordinates of each binding interface)
    """

    reaction_chain, int_site, int_site_distance, unique_chain, COM = Result
    int_index = []
    for i in range(len(reaction_chain)):
        if reaction_chain[i][0] in ChainList and reaction_chain[i][1] in ChainList:
            int_index.append(i)
    reaction_chain_ = []
    int_site_ = []
    int_site_distance_ = []
    for i in range(len(int_index)):
        reaction_chain_.append(reaction_chain[i])
        int_site_.append(int_site[i])
        int_site_distance_.append(int_site_distance[i])
    chain_index = []
    for i in range(len(unique_chain)):
        if unique_chain[i] in ChainList:
            chain_index.append(i)
    unique_chain_ = []
    COM_ = []
    for i in range(len(chain_index)):
        unique_chain_.append(unique_chain[i])
        COM_.append(COM[i])
    print('After filter with', ChainList, ':')
    print(str(len(unique_chain_)) + ' chain(s) in total: ' + str(unique_chain_))
    for i in range(len(COM_)):
        print("Center of mass of  " + unique_chain_[i] + " is: " +
              "[%.3f, %.3f, %.3f]" % (COM_[i][0], COM_[i][1], COM_[i][2]))
    for i in range(len(int_site_)):
        print("Interaction site of " + reaction_chain_[i][0] + " & " + reaction_chain_[i][1] + " is: "
              + "[%.3f, %.3f, %.3f]" % (int_site_[i][0][0],
                                        int_site_[i][0][1], int_site_[i][0][2]) + " and "
              + "[%.3f, %.3f, %.3f]" % (int_site_[i][1][0],
                                        int_site_[i][1][1], int_site_[i][1][2])
              + " distance between interaction sites is: %.3f nm" % (int_site_distance_[i]))

    return reaction_chain_, int_site_, int_site_distance_, unique_chain_, COM_


