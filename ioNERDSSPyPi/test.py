from ioNERDSS.__init__ import *

acf.acf_coord("../unimportant/TestingFunctions/testing_PDBs", ["A"], sim_num = 2, time_step = 0.1)

# f = open("/home/yufengdu/Clathrin/Full/1/PDB/5000000.pdb")
# line = f.readline()
# count = 0
# while line:
#     line = f.readline()
#     if len(line) == 0:
#                 continue
#     if line[0] == 'A': 
#         siteName = line[12:15]
#         molName = line[17:20]
#         molIndex = int(line[20:26]) + 1
#         molName = molName.strip()
#         if siteName == 'COM' and molName == "cla":
#             count += 1

# f.close()
# print(count)