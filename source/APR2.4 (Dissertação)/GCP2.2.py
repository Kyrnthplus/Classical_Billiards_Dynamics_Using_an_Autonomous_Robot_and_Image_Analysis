import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np

pi_value = np.pi
FS = 24
PAD=10

plt.rcParams['font.family']= 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'	
plt.rcParams['mathtext.fontset'] = 'stix'

COR='#2f97ff'
CORT='gray'
arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
print(arquivos)
for Nome in arquivos:
    # Extrair o nome do arquivo sem a extensão
    Nome_sem_extensao = os.path.splitext(Nome)[0]
    nome_arquivo = Nome_sem_extensao
    print(nome_arquivo)
    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)
    
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)
    # Plot
    # Criar a figura e os eixos com o tamanho especificado
    fig, ax = plt.subplots(figsize=(9, 6))

    # Plotar os dados de Poincaré map (Numérico e Experimental)
    ax.plot(X_PT, Y_PT, color='black', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=6, alpha=1, label='Numerical')
    #ax.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12, markeredgecolor='black', label='Experimental')

    # Configurar a legenda
    legend = ax.legend(loc='upper right', fontsize=FS*4/5)
    legend.get_frame().set_alpha(0.5)  # Define a transparência da caixa de legendas
    ratio = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])
    ax.set_aspect(ratio * (6 / 8))
    # Rótulos dos eixos
    ax.set_xlabel(r'$\ell$', fontsize=FS)
    ax.set_ylabel(r'sen $\phi$', fontsize=FS)

    # Definir os ticks do eixo x com notação de pi
    ax.set_xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value])
    ax.set_xticklabels(['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)

    # Definir os ticks do eixo y
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.tick_params(axis='y', which='major', labelsize=FS*4/5, pad=PAD)
    ax.tick_params(axis='x', which='major', labelsize=FS*4/5, pad=PAD)

    # Definir os limites dos eixos
    ax.set_xlim(-0.1, 2 * np.pi + 0.1)
    ax.set_ylim(-1.05, 1.05)

    # Configurar a grade e ticks menores
    ax.minorticks_on()
    ax.grid(which='minor', linestyle=':', linewidth='0.1', color='gray', alpha=0.25)
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)

    # Configurar os ticks em todas as direções
    ax.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Ajustar o layout para evitar sobreposição
    fig.tight_layout()

    # Salvar o gráfico
    #plt.savefig('Gráficos/SP/Poincaré/' + str(nome_arquivo) + '_(Comp_Poincaré).png', dpi=600)

    #plt.savefig('Gráficos/Quirino/Poincaré/Comp/png/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).png', dpi=600)
    plt.savefig('Gráficos/Quirino/Poincaré/Comp/pdf/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).pdf', dpi=600)
    #plt.savefig('Gráficos/Quirino/Poincaré/Comp/svg/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).svg', dpi=600)
    #plt.show()
