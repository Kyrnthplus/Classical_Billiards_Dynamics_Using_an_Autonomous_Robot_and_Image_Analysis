import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np
PAD=10
pi_value = np.pi
Norm=5.01/(2*pi_value)
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
    X=X*Norm
    Y=Y*Norm
    #AltY= np.max(Y)- np.min(Y)
    # Load collision data
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
    X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)
    #AltC= np.max(Y_C)- np.min(Y_C)
    #H=AltY/AltC
    X_C=X_C*Norm
    Y_C=Y_C*Norm

    FS=16
    # Plot
    fig, ax = plt.subplots(figsize=(7, 6))

    # Adicionando o título da figura
    fig.suptitle(f'{nome_arquivo} | Col. Exp. = {len(X_C)}', fontsize=FS)

    # Plotando a trajetória e as colisões
    ax.plot(X, Y, color=COR, linestyle='solid', drawstyle='default', linewidth=1, label='Trajetória')
    ax.plot(X_C, Y_C, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black', label='Colisões')

    # Configurando a legenda
    legend = ax.legend(loc='upper right', fontsize=FS*4/5)
    legend.get_frame().set_alpha(0.5)  # Define a transparência da caixa de legenda

    # Definindo o aspecto dos eixos
    ratio = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(ratio * (6 / 8))
    #ax.set_aspect(8/6)

    # Rótulos dos eixos
    ax.set_xlabel(r'$ X $', fontsize=FS)
    ax.set_ylabel(r'$ Y $', fontsize=FS)

    # Definindo o formato dos eixos (square)
    #ax.set_aspect('equal')

    # Configurando os ticks
    ax.set_yticks(np.arange(-1, 1.01, 0.5))
    ax.set_xticks(np.arange(-1, 1.01, 0.5))
    ax.tick_params(axis='y', labelsize=FS*4/5)
    ax.tick_params(axis='x', labelsize=FS*4/5)
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)

    # Configurando os ticks maiores e menores
    ax.tick_params(axis='both', which='major', pad=PAD)
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
    ax.minorticks_on()

    # Configurando a grade
    ax.grid(which='minor', linestyle=':', linewidth='0.1', color='gray', alpha=0.25)
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)

    # Ajustando o layout
    fig.tight_layout()

    # Exibindo o gráfico com a grade
    ax.grid(True)
    '''
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
    '''
    plt.savefig('Gráficos/SP/' + str(nome_arquivo) + '.SP.png', dpi=350)
    #plt.close('all')

    #plt.tight_layout()
    #plt.savefig('Gráficos/Apr/' + str(nome_arquivo) + '_(APR2).png', dpi=350)
    #plt.show()
