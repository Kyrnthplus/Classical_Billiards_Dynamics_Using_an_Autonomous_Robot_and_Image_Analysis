import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter

import numpy as np
FS=30
PAD=10
pi_value = np.pi
Norm=5.01/(2*pi_value)
COR='#ff972f'
CORT='gray'
arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
print(arquivos)

def format_func(value, tick_number):
    if value == int(value):
        return f'{int(value)}'  # Sem casas decimais se for inteiro
    elif value * 10 == int(value * 10):
        return f'{value:.1f}'   # Uma casa decimal se for .0
    else:
        return f'{value:.2f}'   # Duas casas decimais para os outros
        
plt.rcParams['font.family']= 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'	
plt.rcParams['mathtext.fontset'] = 'stix'

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

    
    # Plot
    NX=9
    NY=6
    N=NX/NY
    plt.figure(figsize=(NX,NY))
    #plt.suptitle(f'{nome_arquivo} | Col. Exp. = {len(X_C)}')
    # Plot 1: Trajectory
    #plt.subplot(1, 2, 1)


    plt.plot(X, Y, color=COR, linestyle='none', drawstyle='default', linewidth=1,marker='.', markersize=1.5, label='Trajectory')
    plt.plot(X_C, Y_C, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black', label='Collisions')
    #plt.legend(loc='upper left', fontsize=FS*4/5)
    legend = plt.legend(loc='upper right', fontsize=FS*3/5)
    legend.get_frame().set_alpha(0.5)  # Define a transparência da caixa de legenda
    #plt.gca().set_aspect(8/6)
    plt.xlabel(r'$ X $',fontsize=FS)
    plt.ylabel(r'$ Y $',fontsize=FS)
    #plt.axis('square')
    plt.gca().xaxis.set_major_formatter(FuncFormatter(format_func))
    plt.yticks(np.arange(-1, 1.01, 0.5),fontsize=FS*4/5)
    plt.xticks(np.arange(-1.5, 1.51, 0.75),fontsize=FS*4/5)
    #plt.xticks(np.linspace(-1.5,1.5,5),fontsize=FS*4/5)
    plt.ylim(-1.05, 1.05)
    plt.xlim(-1.55, 1.55) #-(1.55+1.55*0.05)*N, +(1.55+1.55*0.05)*N)
    plt.tick_params(axis='y', which='major', pad=PAD)
    plt.tick_params(axis='x', which='major', pad=PAD)
    #plt.xscale('log')
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray',alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Ajuste de layout e exibição do gráfico
    #plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.2)

    plt.grid(True)

    plt.savefig('Gráficos/SP/' + str(nome_arquivo) + '.SP.png', dpi=350)
    plt.savefig('Gráficos/SP/svg_' + str(nome_arquivo) + '.SP.svg')
    #plt.close('all')

    #plt.tight_layout()
    #plt.savefig('Gráficos/Apr/' + str(nome_arquivo) + '_(APR2).png', dpi=350)
    #plt.show()
