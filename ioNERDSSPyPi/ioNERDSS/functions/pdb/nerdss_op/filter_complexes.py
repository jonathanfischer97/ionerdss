def filter_complexes(complex_lst,num_name_dict,num_dict):
    """Generates a list of every protein in a complex of the correct size

    Args:
        complex_lst (List[List[str]]): a list of complexes, where each complex is represented as a list of protein names
        num_name_dict (dictionary): a dictionary that holds the protein type for each protein number
        num_dict (dictionary): a dictionary that holds the wanted amount of each protein type in the complex.

    Returns:
        list: a list of each protein number that is in a complex of the correct size
    """

    complex_filtered = []
    #run through every protein complex
    for complex in complex_lst:
        temp_complex_num = {}
        for value in set(list(num_name_dict.values())):
            temp_complex_num[value] = 0
        #for each protein
        for protein in complex:
            temp_complex_num[num_name_dict[str(protein)]] = temp_complex_num[num_name_dict[str(protein)]] + 1

        
        if temp_complex_num == num_dict:
            for protein in complex:
                complex_filtered.append(protein)


    return complex_filtered

   