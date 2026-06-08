import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np
import matplotlib.font_manager

pi_value = np.pi
FS = 30
PAD=10

plt.rcParams['font.family']= 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'	
plt.rcParams['mathtext.fontset'] = 'stix'

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
    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)
    
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)
    # Plot
    NX=9
    NY=6
    plt.figure(figsize=(NX,NY))
    #plt.suptitle(f'{nome_arquivo} | Col. Sim. = {len(X_PT)} | Col. Exp. = {len(X_P)}')

    # Plot 3: Poincaré map data
    plt.plot(X_PT, Y_PT, color='gray', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=6,alpha=0.75, label='Numerical')#, markeredgecolor='black',alpha=0.5)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12, markeredgecolor='black', label='Experimental')
    legend = plt.legend(loc='upper right', fontsize=FS*3/5)
    legend.get_frame().set_alpha(0.5)  # Define a transparência da caixa de legendas
    # Rótulos dos eixos e ticks
    plt.xlabel(r'$\ell$', fontsize=FS)
    plt.ylabel(r'sin $\phi$', fontsize=FS)
    plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)
    plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS*4/5)

    plt.tick_params(axis='y', which='major', pad=PAD)
    plt.tick_params(axis='x', which='major', pad=PAD)

    # Limites dos eixos
    plt.xlim(-(2 * np.pi*0.015), 2 * np.pi + 2 * np.pi*0.015)
    plt.ylim(-1.05, 1.05)

    # Configurações da grade
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray',alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Ajuste de layout e exibição do gráfico
    #plt.tight_layout()
    plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.2)

    plt.savefig('Gráficos/SP/' + str(nome_arquivo) + '_(Comp_Poincaré).png', dpi=350)
    plt.savefig('Gráficos/SP/svg' + str(nome_arquivo) + '_(Comp_Poincaré).svg')
    #plt.savefig('Gráficos/Quirino/Poincaré/Comp/png/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).png', dpi=600)
    #plt.savefig('Gráficos/Quirino/Poincaré/Comp/pdf/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).pdf', dpi=600)
    #plt.savefig('Gráficos/Quirino/Poincaré/Comp/svg/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).svg', dpi=600)
    #plt.show()
