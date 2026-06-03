# Atividade Controle Avançado (período 26.1)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![tkinter](https://img.shields.io/badge/UI-tkinter-ff69b4)](https://docs.python.org/3/library/tkinter.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Repositório para disciplina Controle Avançado de Processos no Programa de Pós-Graduação em Engenharia Quimica
### Autores: Ian Ferreira e Maria Eduarda Cunha

## Cenário:
Controle de Nível e Temperatura de um CSTR com Atraso através de controladores PID e MPC

## Sumário

- [Reconhecimento de Sistema](#reconhecimento-de-sistema)
  - [Temperatura](#temperatura)
  - [Nível](#nível)
  - [PRBS](#prbs)
- [Função de Transferência](#função-de-transferência)
  - [Controle PID](#controle-pid)
  - [Controlador MPC](#controle-mpc)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Pré-requisitos](#pré-requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Funcionalidades](#funcionalidades)
- [Interpretação de Resultados](#interpretação-de-resultados)
- [Referências](#referências)
  
---
### Reconhecimento de Sistema:
Foi inicialmente causado pertubações no sistema em malha aberta para poder avaliar o comportamento que este assumia. Foram dados sinais do tipo "Step" nas variáveis manipuladas de interesse. Assim podendo fazer o reconhecimento e encontrar os parâmetros das [Funções de Transferêcia](#função-de-transferência). 
  
  ### Temperatura

  O gráfico abaixo apresenta a resposta da variável de processo após uma pertubação do tipo _Step_ na variável manipulada. Foi feito um processo de limpeza dos ruídos nos resultados, utilizando efetivamente a resposta após o _Step_ para reconhecimento do sistema. O reconhecimento do sistema foi feito através de metódos análitcos, como descritos por _Skogestad, 2003_

   
  ![Step Reponse Temp](Img_Imp/T_rep.png)

  
  ### Nível

  O gráfico abaixo apresenta a resposta da variável de processo após uma pertubação do tipo _Step_ na variável manipulada. Foi feito um processo de limpeza dos ruídos nos resultados, utilizando efetivamente a resposta após o _Step_ para reconhecimento do sistema. O reconhecimento do sistema foi feito através de sistemas de identificação built-in **IDENT**, parte do pacote MATLAB. 
  
  ![Step Response Lvl](Img_Imp/N_rep.png)

  ### PRBS

  Sinais aleatórios para cálculo e identificação dos sub-espaços do sistema (Que foram posteriormente usados na Aplicação do controlador MPC)

  ![PRBS1](Img_Imp/LvlPRBS.png)
  
  ![PRBS2](Img_Imp/TempPRBS.png)
  
  
---
### Função de Transferência: 

Função de Transferência de Nível, devido a resposta do sistema e através do declive apresentado, se assemelha com Comportamento de Processo Integrador: 

$$
G(s) = \frac{K}{s}
$$

Função de Transferência da Temperatura teve melhor encaixe com comportamento de Processo de Primeira Ordem com Tempo Morto: 

$$
G(s) = \frac{K}{{τ_i}s + 1}e^{-{τ_d}s}
$$

---

### Controle PID

Dois controladores PID operam as malhas de nível e temperatura:

- **LIC-101 (Nível)**: $K_p = -60$ (ação reversa: nível alto $\rightarrow$ saída diminui $\rightarrow$ válvula fecha)
- **TIC-101 (Temperatura)**: $K_p = 3.39$ (ação direta: temperatura alta $\rightarrow$ saída aumenta $\rightarrow$ resfria)

A equação do controlador na forma paralela:

$$u(t) = K_p \cdot e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$


com $e(t) = SP - PV$ (erro = setpoint $-$ processo).

Para encontrar os parâmetros foi utilizado o metódo de IMC como descrito por _Skogestad 2003_. 

$$
Kp = \frac{1}{k'}\frac{τ}{τ_c + θ}
$$

$$
τ_i = τ_i
$$

$$
τ_d = τ_d
$$

Neste caso, como o sistema se trata de processos do tipo Integrador e de 1ª ordem apenas, $τ_d = 0$.

### Resposta PID:

Através dos resultados é possível perceber uma resposta mais rápida do sistema a desvios bruscos, abrindo e fechando as válvulas, respeitando os limites físicos do sistema, no entanto, abrindo e fechando as válvulas de forma rápida para corrigir o desvio do Setpoint num passo muito rápido. Assim, no longo prazo, causando problemas com o sistema mecânico das válvulas, necessitando de mais lubrificação e manutenções mais constantes do equipamento. 

![INSERIR IMAGEM](#Img_Imp/res_PID.png)

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
