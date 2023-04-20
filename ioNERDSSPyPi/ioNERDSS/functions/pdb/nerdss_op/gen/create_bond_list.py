import pandas as pd
from .determine_bind import determine_bind


def create_bond_list(site_array,site_dict,binding_array,binding_dict,BufferRatio):
    """Generates a distance dataframe for protein-protein interactions based on given information.

    Args:
        site_array (list of lists): holds information about each bonding site on every protein
        site_dict (dictionary): turns column name (from df) into list index for site_array
        binding_array (list of lists): holds information about each iteraction
        binding_dict (dictionary): turns column name (from df) into list index for binding_array

    Returns:
        pd.DataFrame: the generated distance dataframe containing calculated distances between protein pairs

    Example:
        >>> df = pd.read_csv('protein_data.csv')
        >>> info = pd.read_csv('interaction_info.csv')
        >>> dis_df = PDB_dis_df_gen(df, info)
        >>> dis_df.head()
        Protein_Num_1 Protein_Name_1 Cite_Name_1 Protein_Num_2 Protein_Name_2 Cite_Name_2 sigma       dis
        0             1          Protein_A       Cite_A             2          Protein_B       Cite_B  2.75  5.196152
        1             1          Protein_A       Cite_A             3          Protein_C       Cite_C  1.25  3.162278
        ...
    """
    index = 0
    count = 1

    #bonds_array = []
    #bonds_dict = {"Protein_Num_1":0,"Protein_Name_1":1,"Site_Name_1":2,"Protein_Num_2":3,"Protein_Name_2":4,"Site_Name_2":5,"sigma":6,"distance":7}
    bond_lst = []

    #input(binding_array)

    for bind_type in binding_array:
        
        #create a list of each possible interaction site for this interaction
        protein_1_sites = [] #list of first interaction site
        protein_2_sites = [] #list of second interaction site

        for site in site_array: #for every site, check if it can be included in 1 of the lists
            if site[site_dict['Protein_Name']] == bind_type[binding_dict['Protein_Name_1']]:
                if site[site_dict['Site_Name']] == bind_type[binding_dict['Site_Name_1']]:
                    protein_1_sites.append(site)
            if site[site_dict['Protein_Name']] == bind_type[binding_dict['Protein_Name_2']]:
                if site[site_dict['Site_Name']] == bind_type[binding_dict['Site_Name_2']]:
                    protein_2_sites.append(site)


        print('Calculating distance for reaction #', count, '...')
        count += 1
        
        #create list of each interaction
        for site_1 in protein_1_sites:
            for site_2 in protein_2_sites:
                storeBoolean,distance = determine_bind(site_1,site_2,BufferRatio,site_dict,bind_type[binding_dict["sigma"]])
                if storeBoolean:

                    temp_bond_lst = [site_1[site_dict["Protein_Num"]],site_2[site_dict["Protein_Num"]]]
                    if temp_bond_lst not in bond_lst:
                        bond_lst.append(temp_bond_lst)
                    
                    for bond in bond_lst:
                        bond.sort()
    
                    index += 1

    return bond_lst


