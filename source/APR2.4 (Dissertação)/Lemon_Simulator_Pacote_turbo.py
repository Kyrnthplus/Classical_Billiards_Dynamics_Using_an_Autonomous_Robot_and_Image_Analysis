import numpy as np
import matplotlib.pyplot as plt
import datetime
import multiprocessing as mp
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

def simular(k, COUNT, gamma):
    np.random.seed(k)
    L0 = 2*np.pi
    Gamma = gamma / 100000
    Rg = L0 / (4 * np.arcsin(np.sqrt(1 - (Gamma**2))))
    Ag = Rg * Gamma
    L = Rg
    Anda = 5
    Para = 50

    x0 = np.random.normal(0, 1)
    y0 = np.random.normal(0, 0.5)

    vx0 = np.random.normal(0, 1)
    vy0 = np.random.normal(0, 1)

    dt = 0.01

    ThetaList=[]
    PerList=[]
    x_traj = [x0]
    y_traj = [y0]
    coli = [[x0], [y0]]

    x, y = x0, y0
    vx, vy = vx0, vy0
    v = [vx0, vy0]
    v = calcular_versor(v) * 1
    vm = calcular_modulo(v)
    a = Ag
    centro = [[0], [a, -a]]

    while len(coli[0]) < COUNT:
        x += v[0] * dt
        y += v[1] * dt

        if y <= 0:
            raio1 = np.sqrt((x - centro[0][0])**2 + (y - centro[1][0])**2)
            if raio1 > Rg:
                dist = np.sqrt((x - coli[0][-1])**2 + (y - coli[1][-1])**2)
                if dist <= vm * 10:
                    x = x_traj[-1]
                    y = y_traj[-1]

                coli[0].append(x)
                coli[1].append(y)
                Tcoli = len(coli[0])
                Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][0]]
                phig, phir = calcular_angulo(Vdir, Rdir)

                thetar = np.pi - 2*phir

                vz = produto_vetorial(Rdir, Vdir)

                if vz > 0:
                    Fdir = np.array([v[0] * np.cos(thetar) - v[1] * np.sin(thetar),
                                     v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                else:
                    Fdir = np.array([v[0] * np.cos(thetar) + v[1] * np.sin(thetar),
                                     -v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                    thetar=-thetar
                ###
                ThetaList.append(np.sin(thetar))
                Per= np.arccos((x)/(np.sqrt(x**2+y**2)))
                PerList.append(Per)
                ###
                v[0] = Fdir[0]
                v[1] = Fdir[1]
                for i in range(Para):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * Anda * dt
                y += v[1] * Anda * dt

        else:
            raio2 = np.sqrt((x - centro[0][0])**2 + (y - centro[1][1])**2)
            if raio2 > Rg:
                dist = np.sqrt((x - coli[0][-1])**2 + (y - coli[1][-1])**2)
                if dist <= vm * 10:
                    x = x_traj[-1]
                    y = y_traj[-1]
                coli[0].append(x)
                coli[1].append(y)
                Tcoli = len(coli[0])
                Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][1]]
                phig, phir = calcular_angulo(Vdir, Rdir)

                thetar = np.pi - 2*phir

                vz = produto_vetorial(Rdir, Vdir)
                if vz > 0:
                    Fdir = np.array([v[0] * np.cos(thetar) - v[1] * np.sin(thetar),
                                     v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                else:
                    Fdir = np.array([v[0] * np.cos(thetar) + v[1] * np.sin(thetar),
                                     -v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                    thetar=-thetar

                ###
                ThetaList.append(np.sin(thetar))
                Per= np.arccos((x)/(np.sqrt(x**2+y**2)))+np.pi
                PerList.append(Per)
                ###
                v[0] = Fdir[0]
                v[1] = Fdir[1]
                for i in range(Para):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * Anda * dt
                y += v[1] * Anda * dt

        x_traj.append(x)
        y_traj.append(y)

    agora = datetime.datetime.now()
    data_hora_formatada = agora.strftime("%Y-%m-%d")
    N = k + 1
    nome_arquivo = f'{gamma}_N-{N:03d}_C-{COUNT}_T_S.txt'
    print(N)
    with open('DadosTratadosSimulados/' +  str(nome_arquivo) + '_(Per_SinTheta).txt', 'w') as data1:
    # Iterate over the data and write to the file
        for i in range(len(PerList)):
        # Write transformed data to the file
            data1.write('%f %f\n' % (float(PerList[i]), float(np.sin(ThetaList[i]))) ) # Change Theta to sin(Theta)

    with open('DadosCrus/' + str(nome_arquivo), 'w') as data:
        for i in range(len(y_traj)):
            data.write('%f %f %f %f\n' % (float(x_traj[i]), float(y_traj[i]), float(x_traj[i]), float(y_traj[i])))

def executar_simulacoes_em_paralelo(Simu, COUNT, gamma):
    num_cores = mp.cpu_count()
    sim_por_core = Simu // num_cores

    pool = mp.Pool(processes=num_cores)
    resultados = [pool.apply_async(simular, args=(i, COUNT, gamma)) for i in range(Simu)]

    for resultado in resultados:
        resultado.get()

    print("Simulações concluídas com sucesso!")

if __name__ == '__main__':
    Simu = int(input('Insira quantas Simulações: '))
    gamma = int(input('Insira o valor do Gamma(5 digitos): '))  # 0.5624
    COUNT = int(input('Insira a quantidade de colisões por simulação: '))

    executar_simulacoes_em_paralelo(Simu, COUNT, gamma)

    '''
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
    '''
