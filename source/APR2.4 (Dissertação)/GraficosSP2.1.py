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
    print(nome_arquivo)
    # Load data from the specified file
    caminho_arquivo = 'DadosTratados/' + str(nome_arquivo) + '_(Traj).dat'
    X, Y, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
    AltY= np.max(Y)- np.min(Y)
    # Load collision data
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
    X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)
    AltC= np.max(Y_C)- np.min(Y_C)
    H=AltY/AltC
    X_C=X_C*H
    Y_C=Y_C*H

    FS=16
    # Plot
    plt.figure(figsize=(12, 6))
    plt.suptitle(f'{nome_arquivo} | Col. Exp. = {len(X_C)}')
    # Plot 1: Trajectory
    plt.subplot(1, 2, 1)


    plt.plot(X, Y, color=COR, linestyle='solid', drawstyle='default', linewidth=1)
    plt.xlabel('X',fontsize=FS)
    plt.ylabel('Y',fontsize=FS)
    plt.axis('square')
    plt.yticks(np.arange(-1, 1.01, 0.25))
    plt.xticks(np.arange(-1, 1.01, 0.25))
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.05, 1.06)

    #plt.xscale('log')
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)
    # Plot 2: Collision data
    plt.subplot(1, 2, 2)

    plt.plot(X_C, Y_C, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X',fontsize=FS)
    plt.ylabel('Y',fontsize=FS)
    plt.axis('square')
    plt.yticks(np.arange(-1, 1.01, 0.25))
    plt.xticks(np.arange(-1, 1.01, 0.25))
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.05, 1.06)
    plt.grid(True)


    plt.ylabel('')
    plt.xlabel('X',fontsize=FS)
    #plt.xscale('log')
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)
    plt.savefig('Gráficos/' + str(nome_arquivo) + '.png', dpi=350)
    #plt.close('all')

    #plt.tight_layout()
    #plt.savefig('Gráficos/Apr/' + str(nome_arquivo) + '_(APR2).png', dpi=350)
    #plt.show()
