import os


if __name__ == "__main__":

    #get names of files in current directory
    dir = "ioNERDSSPyPi\ioNERDSS\\functions\platonic_solids\gen_platonic"
    dir_list = os.listdir(dir)
        


    #get the data in each file, add chatgpt starter, and create list
    textList = []
    for file in dir_list:
        if file.endswith('.py'):
            with open(f"{dir}\{file}",mode='r') as file_open:
                text = file_open.read()
                textList.append("Write a python docstring in the google style for this function: " + text) 



    #write into a new file
    with open('output.txt',mode='w') as op_file:
        op_file.write('')
    with open('output.txt',mode='a') as op_file:
        for text in textList:
            op_file.write(f"{text}\n\n=================================================================\n\n")
