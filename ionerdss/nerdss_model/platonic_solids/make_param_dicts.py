def _print_dict(dict):
    '''
    Nicely formats and prints the contents of a dictionary.

    This function iterates over each key-value pair in the input dictionary and prints it in the format:
    ['key'] = value

    Parameters:
    -----------
    dict : dict
        The dictionary whose contents are to be printed.

    Returns:
    --------
    None
        This function prints to standard output and does not return any value.

    '''

    for key, value in dict.items():
        key_str = f"'{key}'" if isinstance(key, str) else str(key)

        if isinstance(value, list):
            value_str = f"[{', '.join(map(str, value))}]"
        else:
            value_str = str(value)
        print(f'[{key_str}] = {value_str}')
    print("\n")

def pull_reaction_information(file: str):
    '''
    Extracts reaction information from a given input file and returns it as a dictionary.

    The function parses a file (e.g., "parms.inp") to extract details about reactions within a specific block 
    labeled by "start reactions" and "end reactions". For each reaction, the function captures relevant 
    information and organizes it into a dictionary, where each key corresponds to a reaction equation 
    (e.g., "A <-> B") and its associated parameters.

    Reaction details are stored as nested dictionaries, with the reaction equation as the outer key, 
    and each parameter as an inner key-value pair.

    Parameters:
    -----------
    file : str
        The path to the input file containing the reaction information.

    Returns:
    --------
    dict
        A dictionary where each key is a reaction equation (e.g., "A <-> B") and the value is another dictionary
        containing parameters and values associated with that reaction. The parameters may include things like 
        exclusion conditions and numerical values for reaction conditions.
    
    Example:
    --------
    Given an input file containing reaction data, the function will return a dictionary like:
    {
        "A <-> B": {
            "norm1": [1.0, 2.0, 3.0],
            "sigma": "1.20302012"
        },
        "C -> D": {
            "onRate": "0"
        }
    }
    
    Notes:
    ------
    - The function assumes the input file contains structured reaction information in blocks marked by "start reactions" and "end reactions".
    - Each reaction line may contain additional parameters, which are processed as key-value pairs.
    - Lines with "exclude" are treated specially, storing them in the dictionary under the respective reaction.
    '''

    rxn_dict = {}
    with open(file,"r") as f:
        lines = f.readlines()
        in_reactions: bool = False
        in_rxn_block: bool = False
        current_rxn: str = ""
        for line in lines:
            line = line.strip()
            if line.startswith("start reactions"):
                in_reactions = True
                continue
            if line.startswith("end reactions"):
                in_reactions = False
                continue
            if in_reactions == False:
                continue
            if "<->" in line or "<-" in line or "->" in line:
                in_rxn_block = True
                current_rxn = line
                rxn_dict[line] = {}
                continue
            if "exclude" in line and in_rxn_block == True:
                rxn_dict[current_rxn][line.split()[0]] = line.split()[-1]
                in_rxn_block = False
                continue
            if in_rxn_block == True and in_reactions == True:
                #generally the .split() outputs [condition, =, vals] so anything from 2 onward is our vals
                if len((line.split()[2:])) > 2:
                    rxn_dict[current_rxn][line.split()[0]] = [float(x) for x in line.replace("[","").replace(",", "").replace(']',"").split()[2:]]
                    continue
                print(line.split())
                if line.split() == []:
                    continue
                else:
                    rxn_dict[current_rxn][line.split()[0]] = line.split()[2]
        print("The following lines can be used to access your reaction information. Copy and Paste the reactions into your code you wish to modify. Be sure to include the dictionary name.")
        _print_dict(rxn_dict)
        return rxn_dict
        
def pull_parameter_file_information(file: str):
    '''
    Parses a simulation input file and extracts parameter, boundary, and molecule information into a dictionary.

    Parameters:
    -----------
    file : str
        Path to the input file containing the simulation parameters and configuration data.

    Returns:
    --------
    dict
        A dictionary containing key-value pairs from the parameters, boundaries, and molecules blocks.
        - Keys are parameter names (e.g., "dt", "runtime").
        - Values are strings, floats, or lists of floats depending on the format of the line in the file.

    Example:
    --------
    Given an input file, the function might return:
    {
        "nItr": "10000",
        "timeStep": "0.1",
        'WaterBox' = [100, 100, 100],
    }
    '''
     
    with open(file,"r") as f:
        lines = f.readlines()
        param_dict: dict = {}
        in_params: bool = False
        in_bounds: bool = False
        in_mol: bool = False
    for line in lines:
        line = line.strip()
        if line.startswith("start parameters"):
            in_params = True
            continue
        if line.startswith("end parameters"):
            in_params = False
            continue
        if in_params == True:
            if "#iterations" in line:
                param_dict[line.split()[0]] = line.split()[2]
            param_dict[line.split()[0]] = line.split()[2]
        line = line.strip()
        if line.startswith("start boundaries"):
            in_bounds = True
            continue
        if line.startswith("end boundaries"):
            in_bounds = False
            continue
        if line.startswith("start molecules"):
            in_mol = True
            continue
        if line.startswith("end molecules"):
            in_mol = False
        if in_bounds == True:
            if len((line.split()[2:])) > 2:
                    param_dict[line.split()[0]] = [float(x) for x in line.replace("[","").replace(",", "").replace(']',"").split()[2:]]
                    continue
            param_dict[line.split()[0]] = line.split()[2]
        if in_mol == True:
            param_dict[line.split()[0]] = line.split()[2]
    print("The following lines can be used to access your parameter information. Copy and Paste the parameters into your code you wish to modify. Be sure to include the dictionary name.")

    _print_dict(param_dict)

    return param_dict

def pull_mol_file_information(file: str):
    '''
    Extracts molecular configuration information from a .mol-style input file into a dictionary.

    Parameters:
    -----------
    file : str
        Path to the input .mol file containing molecular relationship and configuration information.

    Returns:
    --------
    dict
        A dictionary where keys are molecular attribute names (e.g., "mass", "COM", "D" for example) and 
        values are either strings or lists of floats depending on the format in the file.

    Example:
    --------
    Given a section of a .mol file, the output might look like:
    {
        "mass": "1.0",
        "COM": [0.0, 0.0, 1.0],
        "D" = [13.0, 13.0, 13.0]
    }
    '''
    with open(file,'r') as f:
        lines = f.readlines()
        mol: dict = {}
        in_rel = False
    for line in lines:
        line = line.strip()
        if line.startswith("Name"):
            in_rel = True
            continue
        if len(line.split()) == 0: #skip empty lines
            continue
        if line.startswith("COM"):
            in_rel = False
            continue
        if in_rel == True:
            if len((line.split()[2:])) > 2:
                    mol[line.split()[0]] = [float(x) for x in line.replace("[","").replace(",", "").replace(']',"").split()[2:]]
                    continue
            mol[line.split()[0]] = line.split()[2]
        
    print(("The following lines can be used to access your mol information. Copy and paste this output into your code to modify the .mol file"))
    _print_dict(mol)
    return mol
    
    



        
    


    return dict