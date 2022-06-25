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

L_a = 6
L_b = 8
L_c = 6

EI = 100e3


ks_a = ks_flex(L_a, EI)
ks_b = ks_flex(L_b, EI)
ks_c = ks_flex(L_c, EI)

ks_def = pd.read_excel("ks_matrix.xlsx", header = None)
af = pd.read_excel("af_matrix.xlsx", header = None)
af_t = np.transpose(af)

kf = np.linalg.multi_dot((af_t,ks_def, af))
af_p0 = pd.read_excel("af_p0.xlsx", header = None)
Q0 = pd.read_excel("Qo_vec.xlsx", header = None)

af_p0_t = np.transpose(af_p0)
po = np.dot(af_p0_t,Q0)

pf = pd.read_excel("pf_vec.xlsx", header = None)

kf_inv = np.linalg.inv(kf)

pf_po = pf - po

uf = np.dot(kf_inv,pf_po)

#####################
#####################
#####################

v = np.dot(af,uf)

va = v[0:2]
vb = v[2:4]
vc = v[4:6]

q0_a = np.zeros((2,1))
qa = np.dot(ks_a, va)
qa = qa + q0_a

q0_b = np.zeros((2,1))
q0_b = Q0
qb = np.dot(ks_b, vb)
qb = qb + q0_b

q0_c = np.zeros((2,1))
qc = np.dot(ks_c, vc)
qc = qc + q0_c