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
    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_P = X_P * 2 * np.pi / np.max(X_P)'''
    '''
    X_P = X_P - np.pi

    X_Ph = -X_P
    Y_Ph = +Y_P

    X_P = np.concatenate((X_P, X_Ph))
    Y_P = np.concatenate((Y_P, Y_Ph))

    X_Pv = +X_P

    Y_Pv = -Y_P

    X_P = np.concatenate((X_P, X_Pv))
    Y_P = np.concatenate((Y_P, Y_Pv))

    X_P = X_P + np.pi
    
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_T_S_(Per_SinTheta).dat'
    X_PT, Y_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    #X_PT = X_PT * 2 * np.pi / np.max(X_P)
    
    X_PT = X_PT - np.pi

    X_PTh = -X_PT
    Y_PTh = +Y_PT

    X_PT = np.concatenate((X_PT, X_PTh))
    Y_PT = np.concatenate((Y_PT, Y_PTh))

    X_PTv = +X_PT

    Y_PTv = -Y_PT

    X_PT = np.concatenate((X_PT, X_PTv))
    Y_PT = np.concatenate((Y_PT, Y_PTv))

    X_PT = X_PT + np.pi

    '''
    FS=18
    # Plot
    plt.figure(figsize=(9, 6))
    plt.suptitle(f'{nome_arquivo} | Col. Exp. = {len(X_P)}')

    # Plot 3: Poincaré map data
    #plt.plot(X_PT, Y_PT, color='gray', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=6,alpha=0.75)#, markeredgecolor='black',alpha=0.5)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=12, markeredgecolor='black')
    # Rótulos dos eixos e ticks
    plt.xlabel(r'$\ell$', fontsize=FS)
    plt.ylabel(r'sin $\phi$', fontsize=FS)
    plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)
    plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS*4/5)

    # Limites dos eixos
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.ylim(-1.1, 1.1)

    # Configurações da grade
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray',alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Ajuste de layout e exibição do gráfico
    plt.tight_layout()
    plt.savefig('Gráficos/Poincaré/png' + str(nome_arquivo) + '_(Comp_Poincare_Solo).png', dpi=600)
    plt.savefig('Gráficos/Poincaré/pdf' + str(nome_arquivo) + '_(Comp_Poincare_Solo).pdf', dpi=600)
    plt.savefig('Gráficos/Poincaré/svg' + str(nome_arquivo) + '_(Comp_Poincare_Solo).svg', dpi=600)
    #plt.show()
