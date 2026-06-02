# Atividade Controle Avançado (período 26.1)
Repositório para disciplina Controle Avançado de Processos no Programa de Pós-Graduação em Engenharia Quimica
### Autores: Ian Ferreira e Maria Eduarda Cunha

## Resolução PID
Cenário: Controle de Temperatura de um CSTR com Atraso

## Sumário

- [Fundamentação Teórica](#fundamentação-teórica)
  - [Controle PID](#controle-pid)
  - [Controlador MPC](#controle-mpc)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Funcionalidades](#funcionalidades)
- [Guia de Uso](#guia-de-uso)
  - [Painel de Operação](#painel-de-operação)
  - [Parâmetros e Sintonia](#parâmetros-e-sintonia)
  - [Controles Gerais](#controles-gerais)
- [Interpretação de Resultados](#interpretação-de-resultados)
- [Extensões Possíveis](#extensões-possíveis)
- [Referências](#referências)

---

### Controle PID

Dois controladores PID operam as malhas de nível e temperatura:

- **LIC-101 (Nível)**: $K_p = -60$ (ação reversa: nível alto $\rightarrow$ saída diminui $\rightarrow$ válvula fecha)
- **TIC-101 (Temperatura)**: $K_p = +8$ (ação direta: temperatura alta $\rightarrow$ saída aumenta $\rightarrow$ resfria)

A equação do controlador na forma paralela:

$$u(t) = K_p \cdot e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$


com $e(t) = SP - PV$ (erro = setpoint $-$ processo).

---

$$
\frac{H(s)}{Q(s)} = \frac{K}{\tau s + 1}
$$  

 $$ 
 J = \sum_{i=1}^{N_p} |y_{k+i} - r_{k+i}|Q^2 + \sum_{j=0}^{N_c-1} |u_{k+j}|R^2 + \sum_{j=1}^{N_c-1} |\Delta u_{k+j}|_{R_u}^2 
 $$


---
 ## Referências

1. Fogler, H. S. (2016). *Elements of Chemical Reaction Engineering* (5th ed.). Prentice Hall.
2. Seborg, D. E., Edgar, T. F., Mellichamp, D. A., & Doyle, F. J. (2016). *Process Dynamics and Control* (4th ed.). Wiley.
3. Skogestad, Sigurd. *Simple Analytic Rules for Model Reduction and PID Controller Tuning. Journal of Process Control*, v. 13, n. 4, p. 291-309, 2003.
4. Smith, J. M., Van Ness, H. C., & Abbott, M. M. (2005). *Introduction to Chemical Engineering Thermodynamics* (7th ed.). McGraw-Hill.
5. Marlin, T. E. (2000). *Process Control: Designing Processes and Control Systems for Dynamic Performance* (2nd ed.). McGraw-Hill.
6. Luyben, W. L. (1990). *Process Modeling, Simulation, and Control for Chemical Engineers* (2nd ed.). McGraw-Hill.

---
