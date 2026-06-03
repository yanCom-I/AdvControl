from scipy.optimize import minimize
import numpy as np

# ============================================================
# CLASSE MPC MIMO (STATE-SPACE REPRESENTATION)
# ============================================================
class CSTR_MPC:
    def __init__(self, dt, P=30, M=3):
        self.dt = 20000*dt
        self.P = P        # Horizonte de Predição 
        self.M = M        # Horizonte de Controle
        
        # Matrices de Sintonia (Q = Erro de Output, R = Esforço de Controle)
        self.Q = np.diag([20.0, 5.0]) 
        self.R = np.diag([1.0, 2.0])

        # --- LIMITES FÍSICOS ---
        # Saturação absoluta: 0% a 100% para ambas as válvulas
        self.limits = [(0, 100), (0, 100)] 
        
        # Limite de velocidade (Rate of Change): Máximo de 5% por passo de tempo
        self.du_max = np.array([5.0, 5.0])
        
        self.limits = [(0, 100), (0, 100)]
        self.last_u = np.array([50.0, 50.0]) 

        # --- CORREÇÃO: ESTADO INTERNO INICIAL (5 Estados) ---
        self.x_state = np.zeros(5)
        
        # A Matrix (State Dynamics): [Level_k, Temp_k]
        self.A = np.array([[1.0006, -0.0002, 0.0000, 0.0000, 0.0000],
                           [0.0021, 0.9992, 0.0001, 0.0001, -0.0000], 
                           [-0.0018, -0.0002, 0.9998, 0.0010, -0.0009], 
                           [-0.0011, -0.0023, -0.0013, 0.9957, -0.0025],
                           [0.0013, 0.0049, 0.0017, 0.0076, 0.9964]]).T
        
        # B Matrix (Input matrix): [Valve_OP, Heater_OP]
        self.B = np.array([[0.0000, -0.0000, -0.0005, -0.0012, 0.0003], 
                           [0.0000,-0.0000,-0.0002,-0.0005,-0.0027]]).T
        
        # C Matrix (Output Matrix): Assumes we measure exactly what we model
        self.C = np.array([[-12.2083, 1.1211, -0.0001, 0.0001, -0.0000],
                           [-62.1608, 493.0750, 0.0456, 0.0254, -0.0002]])

    def predict(self, x0, u_seq_flat):
        u_seq = u_seq_flat.reshape((self.M, 2))
        y_pred = np.zeros((self.P, 2))
        
        x = np.array(x0) # Deve ser um vetor de dimensão 5
        u = self.last_u
        
        for k in range(self.P):
            if k < self.M:
                u = u_seq[k]
            
            # 1.(5x5) @ (5,1) + (5x2) @ (2,1)
            x = self.A @ x + self.B @ u
            
            # 2. Saída medida: (2x5) @ (5,1) -> Vetor com 2 elementos [Nível, Temp]
            y_pred[k] = self.C @ x
            
        return y_pred

    def cost_function(self, u_seq_flat, x0, sp):
        y_pred = self.predict(x0, u_seq_flat)
        u_seq = u_seq_flat.reshape((self.M, 2))
        sp_arr = np.array(sp)
        
        cost = 0.0
        for k in range(self.P):
            e = y_pred[k] - sp_arr
            cost += e.T @ self.Q @ e
            
        u_prev = self.last_u
        for k in range(self.M):
            du = u_seq[k] - u_prev
            cost += du.T @ self.R @ du
            u_prev = u_seq[k]
            
        return cost
    
    def update(self, pv, sp):
        """
        pv: Array contendo apenas as saídas medidas do processo [Nível, Temp]
        sp: Setpoints desejados [Nível, Temp]
        """
        u0 = np.tile(self.last_u, self.M)
        bnds = [limit for _ in range(self.M) for limit in self.limits]
        
        # Evolução natural do estado apenas com a dinâmica do modelo
        self.x_state = self.A @ self.x_state + self.B @ self.last_u

        C_pseudo_inv = np.linalg.pinv(self.C)
        measured_x_error = C_pseudo_inv @ (np.array(pv) - self.C @ self.x_state)
        self.x_state += 0.25 * measured_x_error # Filtro leve para suavizar ruídos 
        
        def rate_constraints(u_seq_flat):
            u_seq = u_seq_flat.reshape((self.M, 2))
            du = np.zeros_like(u_seq)
            du[0] = u_seq[0] - self.last_u
            for k in range(1, self.M):
                du[k] = u_seq[k] - u_seq[k-1]
                
            upper_bound = self.du_max - du
            lower_bound = self.du_max + du
            return np.concatenate([upper_bound.flatten(), lower_bound.flatten()])
            
        cons = {'type': 'ineq', 'fun': rate_constraints}
            
        # Passa o 'self.x_state' (Tamanho 5) em vez do 'pv' (Tamanho 2)
        res = minimize(self.cost_function, u0, args=(self.x_state, sp), 
                    bounds=bnds, constraints=cons, method='SLSQP')
        
        u_opt = res.x.reshape((self.M, 2))[0]
        self.last_u = u_opt
        
        return u_opt[0], u_opt[1]