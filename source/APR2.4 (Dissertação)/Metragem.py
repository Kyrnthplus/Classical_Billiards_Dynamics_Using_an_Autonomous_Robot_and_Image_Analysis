import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import FuncFormatter
import os
import numpy as np
from math import sqrt
FS=30
PAD=10
pi_value = np.pi
Norm=5.01/(2*pi_value)
COR='#ff972f'
CORT='gray'
arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
#print(arquivos)

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
    #print(nome_arquivo)
    # Load data from the specified file
    caminho_arquivo = 'DadosTratados/' + str(nome_arquivo) + '_(Traj).dat'
    X, Y, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)
    Dist=0
    for i in range(1,len(X)):
        Dist += sqrt((X[i]-X[i-1])**2 + (Y[i]-Y[i-1])**2)
        #print(Dist)
    seg=len(X)/30
    min=seg/60
    
    #print(f'Velocidade = {Dist/seg} | Distancia total = {Dist} | Minuto = {min}')
    print(f'{nome_arquivo} {Dist/seg}m/s {Dist}m  {seg} s')
