import os
import matplotlib.pyplot as plt
import numpy as np
import time
from multiprocessing import Pool
import subprocess

#ffmpeg -framerate 5 -i %04d.jpg -c:v libx264 -r 5  -pix_fmt yuv420p output.mp4

def processar_arquivo(nome_arquivo):
    nome_sem_extensao = os.path.splitext(nome_arquivo)[0]
    print(nome_sem_extensao)

    # Carregar dados de colisão
    caminho_arquivo_colisao = f'DadosTratados/{nome_sem_extensao}_Colisao(X-Y).dat'
    LINHAX, LINHAY = np.loadtxt(caminho_arquivo_colisao, unpack=True)
    if not nome_sem_extensao.endswith('T_S'):
        COR1='#ff972f'
        COR2='green'
    else:
        COR1='#812fff'
        COR2='green'
    for linha in range(2, len(LINHAX) + 1):
        caminho_arquivo_colisao = f'DadosTratados/{nome_sem_extensao}_Colisao(X-Y).dat'
        X_C, Y_C = np.loadtxt(caminho_arquivo_colisao, max_rows=linha, unpack=True)
        # Carregar dados do mapa de Poincaré
        caminho_arquivo_poincare = f'DadosTratados/{nome_sem_extensao}_(Per_SinTheta).dat'
        X_P, Y_P = np.loadtxt(caminho_arquivo_poincare, max_rows=linha, unpack=True)
        #X_P = X_P * 2 * np.pi / np.max(X_P)

        # Configurar o gráfico
        plt.figure(figsize=(5, 10))
        plt.suptitle(f'{nome_sem_extensao} |-|-| Coli = {linha}')

        # Gráfico 1: Dados de colisão
        plt.subplot(2, 1, 1)
        plt.plot(X_C[:-1], Y_C[:-1], color=COR1, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
        plt.plot(X_C[-1:], Y_C[-1:], color=COR2, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
        plt.xlabel('X', fontsize=12)
        plt.ylabel('Y', fontsize=12)
        plt.axis('square')
        plt.ylim(-1.51, 1.51)
        plt.xlim(-1.51, 1.51)
        plt.grid(True)

        # Gráfico 2: Dados do mapa de Poincaré
        plt.subplot(2, 1, 2)
        plt.plot(X_P[:-1], Y_P[:-1], color=COR1, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
        plt.plot(X_P[-1:], Y_P[-1:], color=COR2, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black') # Último ponto em vermelho
        pi_value = np.pi
        x_ticks_positions = [0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value]
        x_ticks_labels = ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
        plt.xticks(x_ticks_positions, x_ticks_labels)
        plt.xlabel(r'$\rho$', fontsize=12)
        plt.ylabel(r'sin $\phi$', fontsize=12)
        plt.yticks([-1, -0.5, 0, 0.5, 1])
        #plt.axis('square')

        plt.ylim(-1, 1)
        plt.xlim(-0.2, 2 * np.pi + 0.2)
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
        plt.grid(True)

        # Salvar o gráfico
        pasta_saida = f'Passo/{nome_sem_extensao}'
        if not os.path.exists(pasta_saida):
            os.makedirs(pasta_saida)
            print(f"A pasta '{nome_sem_extensao}' foi criada com sucesso.")
        plt.savefig(f'{pasta_saida}/{linha:04d}.jpg', dpi=350)
        plt.close()

inicio = time.time()

arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]

# Número de processos a serem utilizados
num_processos = os.cpu_count()

with Pool(num_processos) as p:
    p.map(processar_arquivo, arquivos)

fim = time.time()
tempo_decorrido = fim - inicio
print(f"O programa levou {tempo_decorrido:.2f} segundos para ser executado.")
#ffmpeg -framerate 5 -i %04d.jpg -c:v libx264 -r 5  -pix_fmt yuv420p output.mp4

