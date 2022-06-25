import numpy as np
import pandas as pd

def ks_flex (L, EI):
    ks = np.zeros((2,2))
    ks[0,0] = 4*EI/L
    ks[0,1] = 2*EI/L
    ks[1,0] = 2*EI/L
    ks[1,1] = 4*EI/L
    
    return ks

def ks_axial (L, EA):
    ks = np.zeros((1,1))
    ks[0,0] = EA/L
   
    return ks

def ks_flex_rot (L,EI):
    ks = np.zeros((1,1))
    ks[0,0] = 3*EI/L
    
    return ks

def ks_flex_ax (L,EA):
    ks = np.zeros((1,1))
    ks[0,0] = EA/L
    
    return ks

L_a = 8
L_b = 10
L_c = 6
L_d = 10
EA = 10e3
EA_2 = 20e3


ks_a = ks_axial(L_a, EA)
ks_b = ks_axial(L_b, EA)
ks_c = ks_axial(L_c, EA_2)
ks_d = ks_axial(L_d, EA_2)

ks_def = pd.read_excel("ks_matrix.xlsx", header = None)
af = pd.read_excel("af_matrix.xlsx", header = None)
af_t = np.transpose(af)

kf = np.linalg.multi_dot((af_t,ks_def, af))

po = pd.read_excel("po_vec.xlsx", header = None)
pf = pd.read_excel("pf_vec.xlsx", header = None)

kf_inv = np.linalg.inv(kf)

pf_po = pf - po

uf = np.dot(kf_inv,pf_po)


#####################
#####################
#####################

v = np.dot(af,uf)

va = v[0:1]
vb = v[1:2]
vc = v[2:3]
vd = v[3:4]

q0_a = np.zeros((1,1))
qa = np.dot(ks_a, va)
qa = qa + q0_a

q0_b = np.zeros((1,1))
qb = np.dot(ks_b, vb)
qb = qb + q0_b

q0_c = np.zeros((1,1))
qc = np.dot(ks_c, vc)
qc = qc + q0_c

q0_d = np.zeros((1,1))
qd = np.dot(ks_d, vd)
qd = qd + q0_d