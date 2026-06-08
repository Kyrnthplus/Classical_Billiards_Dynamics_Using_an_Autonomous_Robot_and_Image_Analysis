import numpy as np
import matplotlib.pyplot as plt
import datetime

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import sys
from scipy.signal import butter, filtfilt
from scipy.optimize import curve_fit
import os
import random


def produto_vetorial(v1, v2):
    # Verifica se ambos os vetores têm duas componentes
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Os vetores devem ter duas componentes (x, y)")

    # Calcula o componente z do vetor resultante
    z = v1[0] * v2[1] - v1[1] * v2[0]

    return z
def calcular_modulo(vetor):
    # Use a função norm do numpy para calcular o módulo
    modulo = np.linalg.norm(vetor)
    return modulo
def calcular_versor(vetor):
    # Calcule o módulo do vetor
    modulo = np.linalg.norm(vetor)

    # Evite divisão por zero
    if modulo == 0:
        return np.array([0, 0])  # Se o módulo for zero, retornar vetor nulo

    # Calcule o versor dividindo o vetor pelo seu módulo
    versor = vetor / modulo

    return versor
def calcular_angulo(Vdir, Pdir):
    # Calcule o produto escalar
    dot_product = np.dot(Vdir, Pdir)

    # Calcule as normas dos vetores
    norm_Vdir = np.linalg.norm(Vdir)
    norm_Pdir = np.linalg.norm(Pdir)

    # Evite divisão por zero
    if norm_Vdir == 0 or norm_Pdir == 0:
        return 0, 0

    # Calcule o cosseno do ângulo entre os vetores
    cos_theta = dot_product / (norm_Vdir * norm_Pdir)

    # Certifique-se de que o cosseno está dentro do intervalo [-1, 1]
    #cos_theta = np.clip(cos_theta, -1, 1)

    # Calcule o ângulo em radianos
    angle_radians = np.arccos(cos_theta)

    # Converta o ângulo para graus
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees, angle_radians
L0= 2*np.pi
gamma = 0.5624
Rg = L0 / (4 * np.arcsin(np.sqrt(1 - (gamma**2))))
Ag= Rg*gamma
# Tamanho do quadrado
L = Rg

# Posição inicial aleatória dentro do quadrado
x0 = np.random.uniform(-0.1, 0.1)
y0 = np.random.uniform(-0.5, 0.5)

# Velocidade inicial aleatória
vx0 = np.random.uniform(-1,1)
vy0 = np.random.uniform(-1,1)

# Tempo total de simulação e tamanho do passo de tempo
dt = 0.01

# Número de passos de tempo
# Listas para armazenar posições ao longo do tempo
x_traj = [x0]
y_traj = [y0]
coli = [[x0],[y0]]  # Inicialize coli como uma lista de listas

# Loop de simulação usando o método de Euler
x, y = x0, y0
vx, vy = vx0, vy0
v = [vx0,vy0]






a = Ag
centro = [[0],[a,-a]]
ii = [1,0]
jj = [0,1]

while len(coli[0]) < 1000:
    # Calcular novas posições usando o método de Euler
    x += v[0] * dt
    y += v[1] * dt
    # Reflexão nas bordas do quadrado
    if y<=00:
        raio1 = np.sqrt((x-centro[0][0])**2 + (y-centro[1][0])**2)
        if raio1 > Rg:
            coli[0].append(x)  # Adicione x à lista de colisões
            coli[1].append(y)  # Adicione y à lista de colisões
            Tcoli = len(coli[0])
            Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
            Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][0]]
            Vvdir = calcular_versor(Vdir)
            Rvdir = calcular_versor(Rdir)
            phig, phir = calcular_angulo(Vdir, Rdir)

            print(v[0])

            thetar=np.pi - 2*phir

            vz=produto_vetorial(Rdir,Vdir)
            if vz >0:
                Fdir = np.array([Vvdir[0] * np.cos(thetar)-Vvdir[1]*np.sin(thetar), +Vvdir[0] * np.sin(thetar)+Vvdir[1]*np.cos(thetar)])  # Vetor resultante rotacionado
            else:
                Fdir = np.array([Vvdir[0] * np.cos(thetar)+Vvdir[1]*np.sin(thetar), -Vvdir[0] * np.sin(thetar)+Vvdir[1]*np.cos(thetar)])  # Vetor resultante rotacionado

            print(f'Fdir[0]{Fdir[0]}')
            v[0] = Fdir[0]
            v[1] = Fdir[1]
            for i in range(1000):
                    x_traj.append(x)
                    y_traj.append(y)
            x += v[0] * dt
            y += v[1] * dt

    else:
        raio2 = np.sqrt((x-centro[0][0])**2 + (y-centro[1][1])**2)
        if raio2 > Rg:
            coli[0].append(x)  # Adicione x à lista de colisões
            coli[1].append(y)  # Adicione y à lista de colisões
            Tcoli = len(coli[0])
            Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
            Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][1]]
            Vvdir = calcular_versor(Vdir)
            Rvdir = calcular_versor(Rdir)
            phig, phir = calcular_angulo(Vdir, Rdir)

            print(v[0])

            thetar=np.pi - 2*phir

            vz=produto_vetorial(Rdir,Vdir)
            if vz >0:
                Fdir = np.array([Vvdir[0] * np.cos(thetar)-Vvdir[1]*np.sin(thetar), +Vvdir[0] * np.sin(thetar)+Vvdir[1]*np.cos(thetar)])  # Vetor resultante rotacionado
            else:
                Fdir = np.array([Vvdir[0] * np.cos(thetar)+Vvdir[1]*np.sin(thetar), -Vvdir[0] * np.sin(thetar)+Vvdir[1]*np.cos(thetar)])  # Vetor resultante rotacionado

            print(f'Fdir[0]{Fdir[0]}')
            v[0] = Fdir[0]
            v[1] = Fdir[1]
            for i in range(1000):
                    x_traj.append(x)
                    y_traj.append(y)
            x += v[0] * dt
            y += v[1] * dt
    # Armazenar novas posições''
    x_traj.append(x)
    y_traj.append(y)

    # Obter data e hora atual
agora = datetime.datetime.now()

# Formatar data e hora para incluir no nome do arquivo
data_hora_formatada = agora.strftime("%Y-%m-%d_%H-%M-%S")

# Nome do arquivo com data e hora
nome_arquivo = f'Trajetória_Simulada_{data_hora_formatada}.txt'
print(len(x_traj))  # Verifica o tamanho de x_traj
print(len(y_traj))  # Verifica o tamanho de y_traj

# Abrir arquivo para escrita
with open('DadosCrus/'+'Muito_'+str(nome_arquivo), 'w') as data:
    # Escreve cabeçalho


    # Loop sobre os dados da trajetória
    for i in range(len(y_traj)):
        # Escreve os dados transformados no arquivo
        data.write('%f %f %f %f\n' % (float(x_traj[i]), float(y_traj[i]), float(x_traj[i]), float(y_traj[i])))

# Plotar a trajetória da partícula dentro do quadrado
plt.figure(figsize=(6, 6))
plt.plot(x_traj, y_traj, color = 'black', linestyle='none', drawstyle='default', linewidth=0.1, marker='.', markersize=1, markeredgecolor='black')
plt.scatter(coli[0], coli[1], color='red')  # Adicione as colisões ao gráfico
circle = plt.Circle((0, a), L, color='black', fill=False)
circle1 = plt.Circle((0, -a), L, color='black', fill=False)
plt.gca().add_patch(circle)
plt.gca().add_patch(circle1)
plt.xlim(-5,5)
plt.ylim(-5,5)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Trajetória da Partícula dentro do Quadrado')
plt.grid(True)
plt.show()

