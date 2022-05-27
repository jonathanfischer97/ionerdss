from angles import angles
import math

def mag(x):
    return math.sqrt(sum(i ** 2 for i in x))

COMA = [0,0,0]
COMB = [1.5,0,0]
# COMC = [-1.0606601717798214, -1.0606601717798214, 0]
# COMD = [-1.180952329051192, -2.311488291065657, 64.948151424630822]
# COMP = [-1.411331416087540,  2.178478863149561, 64.948151424630822]
# COMQ = [-5.834918472780235,  4.687465335031046, 64.567649757048542]
NormA = [0, 0, 1]
NormB = [1.5, 0, -1]
# NormC = [-1.0606601717798214, -1.0606601717798214, 1]
# NormD = [-1.199120826421210, -2.347049649389744, 65.947353754240524]
# NormP = [-1.433044207104272,  2.211993922582631, 65.947353754240524]
# NormQ = [-5.924686449284547,  4.759580186339216, 65.560998214849292]
IntAB = [0.5,0,0]
# IntAC = [-0.3535533905932738,-0.3535533905932738,0]
# IntAD = [-1.622017519986264, -0.899795971751000, 63.362161937168622]
# IntAP = [-1.760158787197043,  0.104638070326292, 63.337164137167093]
# IntAQ = [-3.393284769446724,  0.994305260709424, 65.743079033037361]
IntB = [1,0,0]
# IntC = [-0.7071067811865476,-0.7071067811865476,0]
# IntD = [-0.970698620704074, -1.472023189243900, 63.337164137167093]
# IntP = [-1.590254929752403,  0.954810391816039, 63.362161937168622]
# IntQ = [-5.462014723187736,  3.302488815006827, 65.485298434909637]
# IntmBinding = NormA
# IntrBinding = [-2.552402456751983, -0.130963129025081, 63.948949095021121]
inner_angle = angles(COMA,COMB,IntAB,IntB,NormA,NormB)
sigma = mag([IntAB[0] - IntB[0],IntAB[1] - IntB[1],IntAB[2] - IntB[2]])
print("Normal point for A is %.6f %.6f %.6f" %(NormA[0] - COMA[0], NormA[1] - COMA[1],NormA[2] - COMA[2]))
print("Normal point for B is %.6f %.6f %.6f" %(NormB[0] - COMB[0], NormB[1] - COMB[1],NormB[2] - COMB[2]))
print("Angles for dimers:")
print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4],sigma))
# inner_angle = angles(COMA,COMC,IntAC,IntC,NormA,NormC)
# sigma = mag([IntAC[0] - IntC[0],IntAC[1] - IntC[1],IntAC[2] - IntC[2]])
# print("Normal point for A is %.6f %.6f %.6f" %(NormA[0] - COMA[0], NormA[1] - COMA[1],NormA[2] - COMA[2]))
# print("Normal point for C is %.6f %.6f %.6f" %(NormC[0] - COMC[0], NormC[1] - COMC[1],NormC[2] - COMC[2]))
# print("Angles for trimer AC:")
# print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4],sigma))
# inner_angle = angles(COMA,COMD,IntAD,IntD,NormA,NormD)
# sigma = mag([IntAD[0] - IntD[0],IntAD[1] - IntD[1],IntAD[2] - IntD[2]])
# print("Normal point for A is %.6f %.6f %.6f" %(NormA[0] - COMA[0], NormA[1] - COMA[1],NormA[2] - COMA[2]))
# print("Normal point for D is %.6f %.6f %.6f" %(NormD[0] - COMD[0], NormD[1] - COMD[1],NormD[2] - COMD[2]))
# print("Angles for hexamer AD:")
# print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4],sigma))
# inner_angle = angles(COMA,COMP,IntAP,IntP,NormA,NormP)
# sigma = mag([IntAP[0] - IntP[0],IntAP[1] - IntP[1],IntAP[2] - IntP[2]])
# print("Normal point for A is %.6f %.6f %.6f" %(NormA[0] - COMA[0], NormA[1] - COMA[1],NormA[2] - COMA[2]))
# print("Normal point for P is %.6f %.6f %.6f" %(NormP[0] - COMP[0], NormP[1] - COMP[1],NormP[2] - COMP[2]))
# print("Angles for hexamer AP:")
# print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4],sigma))
# inner_angle = angles(COMA,COMQ,IntAQ,IntQ,NormA,NormQ)
# sigma = mag([IntAQ[0] - IntQ[0],IntAQ[1] - IntQ[1],IntAQ[2] - IntQ[2]])
# print("Normal point for A is %.6f %.6f %.6f" %(NormA[0] - COMA[0], NormA[1] - COMA[1],NormA[2] - COMA[2]))
# print("Normal point for Q is %.6f %.6f %.6f" %(NormQ[0] - COMQ[0], NormQ[1] - COMQ[1],NormQ[2] - COMQ[2]))
# print("Angles for trimer AQ:")
# print("%.6f, %.6f, %.6f, %.6f, %.6f, %.6f" % (inner_angle[0], inner_angle[1], inner_angle[2], inner_angle[3], inner_angle[4],sigma))
# c_IntAB = [IntAB[0] - COMA[0],IntAB[1] - COMA[1],IntAB[2] - COMA[2]]
# c_IntAC = [IntAC[0] - COMA[0],IntAC[1] - COMA[1],IntAC[2] - COMA[2]]
# c_IntAD = [IntAD[0] - COMA[0],IntAD[1] - COMA[1],IntAD[2] - COMA[2]]
# c_IntAP = [IntAP[0] - COMA[0],IntAP[1] - COMA[1],IntAP[2] - COMA[2]]
# c_IntAQ = [IntAQ[0] - COMA[0],IntAQ[1] - COMA[1],IntAQ[2] - COMA[2]]
# c_IntmBinding = [IntmBinding[0] - COMA[0],IntmBinding[1] - COMA[1],IntmBinding[2] - COMA[2]]
# c_IntrBinding = [IntrBinding[0] - COMA[0],IntrBinding[1] - COMA[1],IntrBinding[2] - COMA[2]]
# print("COM %.6f, %.6f, %.6f" %(0.000000, 0.000000, 0.000000))
# print("b %.6f %.6f %.6f" %(c_IntAB[0], c_IntAB[1],c_IntAB[2]))
# print("c %.6f %.6f %.6f" %(c_IntAC[0], c_IntAC[1],c_IntAC[2]))
# print("d %.6f %.6f %.6f" %(c_IntAD[0], c_IntAD[1],c_IntAD[2]))
# print("p %.6f %.6f %.6f" %(c_IntAP[0], c_IntAP[1],c_IntAP[2]))
# print("q %.6f %.6f %.6f" %(c_IntAQ[0], c_IntAQ[1],c_IntAQ[2]))
# print("m %.6f %.6f %.6f" %(c_IntmBinding[0], c_IntmBinding[1],c_IntmBinding[2]))
# print("r %.6f %.6f %.6f" %(c_IntrBinding[0], c_IntrBinding[1],c_IntrBinding[2]))




