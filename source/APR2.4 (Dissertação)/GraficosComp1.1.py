import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np

pi_value = np.pi
COR='#ff972f'
CORT='gray'
arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
print(arquivos)
for Nome in arquivos:
    # Extrair o nome do arquivo sem a extensão
    Nome_sem_extensao = os.path.splitext(Nome)[0]
    nome_arquivo = Nome_sem_extensao
    # Load data from the specified file
    caminho_arquivo = 'DadosCrus/' + str(nome_arquivo) + '.txt'
    X, Y, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
    AltY=np.max(Y)-abs(np.min(Y))

    # Calculate the midpoint of X and Y and center the data
    ponto_medio_X = np.mean(X)
    ponto_medio_Y = np.mean(Y)
    X = X - np.mean(X)
    Y = Y - np.mean(Y)#- np.max(Y)+AltY
    # Normalize the data
    max_X = np.max(X)
    min_X = np.min(X)
    Norm = max_X + abs(min_X)
    X = (X / Norm) * 2
    Y = (Y / Norm) * 2
    caminho_arquivo = 'DadosCrus/DadosSimulados/' + str(nome_arquivo) + '_T_S.txt'
    XT, YT = np.loadtxt(caminho_arquivo, unpack=True)
    #XT, YT, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
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
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
    X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)
    LgX=abs(np.min(X_C))+np.max(X_C)
    X_C=2*X_C/LgX
    Y_C=2*Y_C/LgX
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_T_S_Colisao(X-Y).dat'
    X_CT, Y_CT = np.loadtxt(caminho_arquivo_Colisao, unpack=True)
    LgXT=abs(np.min(X_CT))+np.max(X_CT)
    X_CT=2*X_CT/LgXT
    Y_CT=2*Y_CT/LgXT
    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)

    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)


    Lx, Ly = np.loadtxt('Lyapunov/' + str(nome_arquivo) + '.dat', unpack=True)
    LxT,LyT= np.loadtxt('Lyapunov/' + str(nome_arquivo) + '_T_S.dat', unpack=True)

    FS=12
    # Plot
    plt.figure(figsize=(10, 10))
    plt.suptitle(f'{nome_arquivo} | L.E. Simu. = {LyT[-1]:.5f} | L.E. Exp. = {Ly[-1]:.5f} | Col. Sim. = {len(X_PT)} | Col. Exp. = {len(X_P)}')
    # Plot 1: Trajectory
    plt.subplot(2, 2, 1)
    plt.plot(XT[:len(X)], YT[:len(X)], color=CORT, linestyle='solid', drawstyle='default', linewidth=1,alpha=0.5)

    plt.plot(X, Y, color=COR, linestyle='solid', drawstyle='default', linewidth=1)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 2: Collision data
    plt.subplot(2, 2, 2)
    plt.plot(X_CT[:len(X_C)], Y_CT[:len(Y_C)], color=CORT, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black',alpha=0.5)

    plt.plot(X_C, Y_C, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 3: Poincaré map data
    plt.subplot(2, 2, 3)
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

    plt.subplot(2, 2, 4)
    plt.axhline(Ly[-1], color='black', linestyle='dotted', linewidth=1, alpha=1, label=f'LE ({Ly[-1]:.5f})')

    plt.plot(LxT[:len(Lx)], LyT[:len(Ly)], color=CORT,alpha=0.5)
    plt.plot(Lx, Ly, color=COR)
    plt.minorticks_on()
    #plt.legend(loc='lower right')
    plt.ylim(Ly[-1]-0.50, Ly[-1]+ 0.50)
    #plt.yticks([-0.5,-0.25, 0,0.25,0.5])
    plt.yticks(np.arange( Ly[-1]-0.50,Ly[-1]+ 0.50 , 0.10))
    plt.gca().yaxis.set_major_formatter(FormatStrFormatter('%.2f'))


    #plt.ylim(-0.55, 0.55)

    plt.ylabel(r'$\gamma$',fontsize=FS)
    plt.xlabel('t',fontsize=FS)
    #plt.xscale('log')
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)

    #plt.savefig('Gráficos/' + str(nome_arquivo) + '.png', dpi=350)
    #plt.close('all')

    plt.tight_layout()
    plt.savefig('Gráficos/' + str(nome_arquivo) + '_(Comparação).png', dpi=350)
    #plt.show()
