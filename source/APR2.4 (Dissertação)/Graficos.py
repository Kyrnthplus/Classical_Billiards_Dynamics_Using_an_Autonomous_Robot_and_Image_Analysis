import os
import matplotlib.pyplot as plt
import numpy as np


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

    # Calculate the midpoint of X and Y and center the data
    ponto_medio_X = np.mean(X)
    ponto_medio_Y = np.mean(Y)
    X = X - np.mean(X)
    Y = Y - np.mean(Y)
    # Normalize the data
    max_X = np.max(X)
    min_X = np.min(X)
    Norm = max_X + abs(min_X)
    X = (X / Norm) * 2
    Y = (Y / Norm) * 2

    # Load collision data
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
    X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)

    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    X_P = X_P * 2 * np.pi / np.max(X_P)

    # Plot
    plt.figure(figsize=(20, 6))

    # Plot 1: Trajectory
    plt.subplot(1, 3, 1)
    plt.plot(X, Y, color='#ff972f', linestyle='solid', drawstyle='default', linewidth=1)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 2: Collision data
    plt.subplot(1, 3, 2)
    plt.plot(X_C, Y_C, color='#ff972f', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 3: Poincaré map data
    plt.subplot(1, 3, 3)
    plt.plot(X_P, Y_P, color='#ff972f', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel(r'$\rho$')
    plt.ylabel(r'sin $\phi$')
    plt.yticks([-1, 0, 1])
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('Gráficos/' + str(nome_arquivo) + '_(Per_SinTheta).png', dpi=350)
   # plt.show()
