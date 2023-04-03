# function for checking format of data in readlines

def data_check(data):
    if len(data) != 12:
        if len(data[2]) > 4:
            return -1 # Amino acid name stick with info before
    else:
        if len(data[3]) == 3:
            return 1 # True data
        else: 
            return -2 # Wrong amino acid name