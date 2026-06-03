import pandas as pd
import numpy as np
from sippy import system_identification

# 1. Carrega os Datasets
df = pd.read_csv('historico_PRBS_mpc.csv')
# 2. Extrai Inputs (U) e Outputs (Y) como arrays
U = df[['Level_OP_pct', 'Temp_OP_pct']].values.T
Y = df[['Level_PV_m', 'Temp_PV_C', 'CA_PV_mol/m3']].values.T

# 3. N4SID
sys = system_identification(Y, U, id_method='N4SID', IC='AIC', tsamp=0.1)

# 4. Printar as Matrizes
print("Matrix A:\n", sys.A)
print("Matrix B:\n", sys.B)
print("Matrix C:\n", sys.C)
print("Matrix D:\n", sys.D)