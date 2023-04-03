# Calculated COM Coordinates
a = [9.7488,50.1822,35.4530]
b = [42.1434,68.8598,20.1947]
p = [26.3527,53.0674,31.1525]
q = [25.5483,64.1859,22.2182]
# 
A = [469.319, 363.559, 361.285]
B = [474.44, 334.505, 333.704]
P = [473.159, 347.979, 354.576]
Q = [468.129, 348.817, 341.231]

def dis(x, y):
    return round(((y[0]-x[0])**2 + (y[1]-x[1])**2 + (y[2]-x[2])**2) ** 0.5, 3)

print('A&B')
print(dis(a, b))
print(dis(A, B))
print('A&P')
print(dis(a, p))
print(dis(A, P))
print('A&Q')
print(dis(a, q))
print(dis(A, Q))
print('B&P')
print(dis(b, p))
print(dis(B, P))
print('B&Q')
print(dis(b, q))
print(dis(B, Q))
print('P&Q')
print(dis(p, q))
print(dis(P, Q))