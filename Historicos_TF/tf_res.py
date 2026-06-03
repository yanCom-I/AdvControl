import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def analyze_fopdt(df, time_col, pv_col, op_col):
    """
    Analisa a resposta de um Step para um processo Autorregulatório 
    e retorna Paramêtros de uma FOPDT.
    """
    print(f"\n--- FOPDT: {pv_col} ---")
    
    # 1. Encontra o Step
    step_index = df[op_col].diff().abs().idxmax()
    step_time = df[time_col].iloc[step_index]
    
    # 2. Filtra os Dados do Step
    df_filtered = df.iloc[step_index:].reset_index(drop=True)
    
    # 3. Calcula os Deltas
    OP_initial = df[op_col].iloc[step_index - 1]
    OP_final = df_filtered[op_col].iloc[-1]
    delta_OP = OP_final - OP_initial
    
    PV_initial = df_filtered[pv_col].iloc[0]
    PV_final = df_filtered[pv_col].iloc[-10:].mean() # Average last 10 points for stability
    delta_PV = PV_final - PV_initial
    
    # 4. Calcula K, Tau, Theta
    K = delta_PV / delta_OP
    PV_63 = PV_initial + (0.632 * delta_PV)
    
    time_63_index = (df_filtered[pv_col] - PV_63).abs().idxmin()
    time_63 = df_filtered[time_col].iloc[time_63_index]
    
    # Estima Tempo Morto (limiar de movimento de 1%)
    PV_deadtime_threshold = PV_initial + (0.01 * delta_PV)
    if delta_PV > 0:
        condition = df_filtered[pv_col] > PV_deadtime_threshold
    else:
        condition = df_filtered[pv_col] < PV_deadtime_threshold
        
    dead_time_indices = np.where(condition)[0]
    dead_time_index = dead_time_indices[0] if len(dead_time_indices) > 0 else 0
    dead_time_absolute = df_filtered[time_col].iloc[dead_time_index]
    
    theta = max(0, dead_time_absolute - step_time)
    tau = max(0, (time_63 - step_time) - theta)
    
    print(f"Ganho de Processo (K): {K:.4f}")
    print(f"Tempo Morto (Theta): {theta:.2f} s")
    print(f"Constante de Tempo (Tau): {tau:.2f} s")
    print(f"FT: G(s) = ({K:.4f} / ({tau:.2f}s + 1) * e^(-{theta:.2f}s)")
    
    return K, tau, theta, step_time

def analyze_integrating(df, time_col, pv_col, op_col):
    """
    Analisa a resposta de um Step para um processo Integrador  
    e retorna Velocidade de Ganho e Tempo Morto Efetivo.
    """
    print(f"\n--- INTEGRATING ANALYSIS: {pv_col} ---")
    
    # 1. Encontra o Step
    step_index = df[op_col].diff().abs().idxmax()
    step_time = df[time_col].iloc[step_index]
    
    # 2. Calcula o Delta (OP)
    OP_initial = df[op_col].iloc[step_index - 1]
    OP_final = df[op_col].iloc[step_index + 10]
    delta_OP = OP_final - OP_initial
    
    # 3. Calcula inclinação inicial (antes do step)
    df_before = df[df[time_col] < (step_time - 5)]
    slope_before, int_before, _, _, _ = linregress(df_before[time_col], df_before[pv_col])
    
    # 4.  Calcula inclinação final (depois do tempo morto, assumindo rampa estável)
    df_after = df[df[time_col] > (step_time + 20)]
    slope_after, int_after, _, _, _ = linregress(df_after[time_col], df_after[pv_col])
    
    # 5. Calcula Kv e Theta
    delta_slope = slope_after - slope_before
    Kv = delta_slope / delta_OP
    
    # Intersecção entre as duas linhas de inclinação
    t_intersect = (int_after - int_before) / (slope_before - slope_after)
    theta = max(0, t_intersect - step_time)
    
    print(f"Ganho de Velocidade (Kv): {Kv:.6f}")
    print(f"Tempo Morto Efetivo (Theta): {theta:.2f} s")
    print(f"FT: G(s) = ({Kv:.6f} / s) * e^(-{theta:.2f}s)")
    
    return Kv, theta, slope_before, int_before, slope_after, int_after, step_time

def plot_system(df, time_col, pv_col, op_col, step_time, title):
    """Plot de PV e OP nos Eixos X compatilhados."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    ax1.plot(df[time_col], df[pv_col], color='red' if 'Temp' in pv_col else 'green')
    ax1.axvline(x=step_time, color='black', linestyle='--', label='Step')
    ax1.set_ylabel(pv_col)
    ax1.set_title(title)
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(df[time_col], df[op_col], color='blue')
    ax2.axvline(x=step_time, color='black', linestyle='--', label='Step')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel(op_col)
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

# ==========================================
# Execução
# ==========================================


df_temp = pd.read_csv('historico_T.csv')

K_t, tau_t, theta_t, step_t = analyze_fopdt(
    df_temp, time_col='Time_s', pv_col='Temp_PV_C', op_col='Temp_OP_pct')
plot_system(df_temp, 'Time_s', 'Temp_PV_C', 'Temp_OP_pct', step_t, 'Temperature System (FOPDT)')



df_level = pd.read_csv('historico_L.csv')

Kv_l, theta_l, sb, ib, sa, ia, step_l = analyze_integrating(
    df_level, time_col='Time_s', pv_col='Level_PV_m', op_col='Level_OP_pct')
plot_system(df_level, 'Time_s', 'Level_PV_m', 'Level_OP_pct', step_l, 'Level System (Integrating)')
