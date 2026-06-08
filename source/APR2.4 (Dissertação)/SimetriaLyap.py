import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np

pi_value = np.pi
COR='#ff972f'
CORT='gray'
arquivos = [arq for arq in os.listdir('DadosComparar') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
print(arquivos)
for Nome in arquivos:
    # Extrair o nome do arquivo sem a extensão
    Nome_sem_extensao = os.path.splitext(Nome)[0]
    nome_arquivo = Nome_sem_extensao
    # Load data from the specified file
    caminho_arquivo = 'DadosComparar/' + str(nome_arquivo) + '.txt'
    X, Y, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
    AltY=np.max(Y)-abs(np.min(Y))

    # Calculate the midpoint of X and Y and center the data

    caminho_arquivo = 'DadosComparar/DadosSimulados/' + str(nome_arquivo) + '_T_S.txt'
    XT, YT, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
    AltYT=np.max(YT)+np.min(YT)
    # Calculate the midpoint of X and Y and center the data
    ponto_medio_X = np.mean(XT)
    ponto_medio_Y = np.mean(YT)
    XT = XT - np.mean(XT)
    YT = YT #- np.max(YT)#+AltYT
    # Normalize the data
    max_X = np.max(XT)
    min_X = np.min(XT)
    Norm = max_X + abs(min_X)
    XT = (XT / Norm) * 2
    YT = (YT / Norm) * 2

    # Load collision data

    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)
    for i in range(len(X_P)):
        if X_P[i]>np.pi:
            X_P[i]=X_P[i]-np.pi
    for j in range(len(Y_P)):
        if Y_P[j]<0:
            Y_P[j]=abs(Y_P[j])
            X_P[j]=abs(X_P[j]-np.pi)

    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)
    for i in range(len(X_PT)):
        if X_PT[i]>np.pi:
            X_PT[i]=X_PT[i]-np.pi
    for j in range(len(Y_PT)):
        if Y_PT[j]<0:
            Y_PT[j]=abs(Y_PT[j])
            X_PT[j]=abs(X_PT[j]-np.pi)

    Lx, Ly = np.loadtxt('Lyapunov/' + str(nome_arquivo) + '.dat', unpack=True)
    LxT,LyT= np.loadtxt('Lyapunov/' + str(nome_arquivo) + '_T_S.dat', unpack=True)

    FS=12
    # Plot
    plt.figure(figsize=(15,15/2))
    plt.suptitle(f'Simetria no mapa de Poincaré | {nome_arquivo} |\nL.E. Sim. = {LyT[-1]:.5f} | L.E. Exp. = {Ly[-1]:.5f} | Col. Sim. = {len(X_PT)} | Col. Exp. = {len(X_P)}')




    # Plot 3: Poincaré map data
    plt.subplot(1, 2, 1)
    plt.plot(X_PT, Y_PT, color='gray', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12,alpha=0.6)#, markeredgecolor='black',alpha=0.5)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12, markeredgecolor='black')
    plt.xlabel(r'$\rho$')
    x_ticks_positions = [0, 0.5 * pi_value, pi_value]
    x_ticks_labels = ['0', r'$\frac{\pi}{2}$', r'$\pi$' ]
    plt.xticks(x_ticks_positions, x_ticks_labels)
    plt.xlabel(r'$\rho$', fontsize=FS)
    plt.ylabel(r'sin $\phi$')
    #plt.yticks([-1,-0.5, 0,0.5, 1])
    #plt.locator_params(axis='y', nbins=9)
    plt.yticks()
    #plt.axis('equal')
    #plt.axis('tight')  # Ajusta os limites dos eixos para que todos os dados sejam mostrados

    plt.ylim(0, 1)
    plt.xlim(-0.1, np.pi +0.1)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)

    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)

    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)
    # Plot 3: Poincaré map data
    plt.subplot(1, 2, 2)
    plt.plot(X_PT, Y_PT, color='gray', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12,alpha=0.6)#, markeredgecolor='black',alpha=0.5)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel(r'$\rho$')
    x_ticks_positions = [0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value]
    x_ticks_labels = ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    plt.xticks(x_ticks_positions, x_ticks_labels)
    plt.xlabel(r'$\rho$', fontsize=FS)
    plt.ylabel(r'sin $\phi$')
    plt.yticks([-1, 0, 1])
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)
    plt.savefig('Gráficos/Simetria/' + str(nome_arquivo) + '_(Simetria).png', dpi=400)
