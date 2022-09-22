import ioNERDSS as io

FileName = '1si4.pdb'
# FileName = '1utc.pdb'

result1 = io.real_PDB_separate_read(FileName)

io.real_PDB_3D(Result=result1)