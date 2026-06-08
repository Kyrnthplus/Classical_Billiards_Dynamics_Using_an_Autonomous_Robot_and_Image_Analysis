##Esse programa Cria um grafico de Expoente de lyapunov em função do Gamma, comparando experimental com o numerico

import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

import numpy as np

pi_value = np.pi
FS = 30
PAD=10

plt.rcParams['font.family']= 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'	
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']  # Alternativa ao STIX e LaTeX
plt.rcParams['mathtext.fontset'] = 'stix'  # Fonte matemática STIX
plt.rcParams['text.usetex'] = True  # Usa LaTeX para renderizar o texto
COR ='#ff972f'
CORT='#2f97ff'
nome_arquivo="ExpLyap.txt"
nome_arquivo1="ExpLyapRR.txt"
nome_arquivo2="SF.txt"
nome_arquivo3="F.txt"
# Solicit user input for file name and width of the plot
#print(arquivos)

# Extrair o nome do arquivo sem a extensão
# Load Poincaré map data
caminho_arquivo_Poincare = 'DadosCrus/LG/' + str(nome_arquivo)
X_P, Xe_P, Y_P, Ye_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
#X_P = X_P * 2 * np.pi / np.max(X_P)

caminho_arquivo_Poincare = 'DadosCrus/LG/' + str(nome_arquivo1)
X_PT, Y_PT, Ye_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
#X_PT = X_PT * 2 * np.pi / np.max(X_P)
# Plot

caminho_arquivo_Poincare = 'DadosCrus/LG/' + str(nome_arquivo2)
Xsf_PT, Ysf_PT, Ysfe_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
#X_P = X_P * 2 * np.pi / np.max(X_P)

caminho_arquivo_Poincare = 'DadosCrus/LG/' + str(nome_arquivo3)
Xf_PT, Yf_PT, Yfe_PT = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
#X_P = X_P * 2 * np.pi / np.max(X_P)

NX=9
NY=6
plt.figure(figsize=(NX,NY))

# Plot 3: Poincaré map data
#plt.errorbar(X_PT, Y_PT, linestyle='--', yerr=Ye_PT, color='gray', ecolor="black", drawstyle='default', linewidth=1, marker='.', markersize=9, markeredgecolor='black', alpha=1, capsize=3, elinewidth=1, label='Numerical', zorder=1)


plt.plot(Xsf_PT, Ysf_PT, linestyle='--', color='gray', drawstyle='default', linewidth=1, marker='.', markersize=9*1.5, markeredgecolor='black', alpha=0.3, label='Numérico', zorder=2)

#plt.errorbar(Xsf_PT, Ysf_PT, linestyle='--', yerr=Ysfe_PT, color='blue', ecolor="blue", drawstyle='default', linewidth=1, marker='.', markersize=9, markeredgecolor='black', alpha=1, capsize=3, elinewidth=1, label='Numerical', zorder=1)
plt.errorbar(Xf_PT, Yf_PT, linestyle='--', yerr=Yfe_PT, color='black', ecolor='black', drawstyle='default', linewidth=1, marker='.', markersize=9*1.5, markeredgecolor='black', alpha=0.8, capsize=3, elinewidth=1, label='Numérico com Filtro', zorder=3)
#plt.errorbar(X_P, Y_P, xerr=Xe_P, yerr=Ye_P, color=COR, linestyle='none', drawstyle='default', linewidth=3, marker='.', markersize=18*1.25, markeredgecolor='black', capsize=5, elinewidth=3, label='Experimental', zorder=4)
plt.errorbar(X_P[:-1], Y_P[:-1], xerr=Xe_P[:-1], yerr=Ye_P[:-1], color=COR, linestyle='none', drawstyle='default', linewidth=3, marker='.', markersize=18*1.25, markeredgecolor='black', capsize=5, elinewidth=3, label='Experimental', zorder=4)
plt.errorbar(X_P[-1:], Y_P[-1:], xerr=Xe_P[-1:], yerr=Ye_P[-1:], color=CORT, linestyle='none', drawstyle='default', linewidth=3, marker='.', markersize=18*1.25, markeredgecolor='black', capsize=5, elinewidth=3, zorder=4)


# Legenda
#plt.legend(loc='upper left', fontsize=FS*3/5)
legend = plt.legend(loc='upper left', fontsize=FS*3/5)
legend.get_frame().set_alpha(0.5)  # Define a transparência da caixa de legendas
# Rótulos dos eixos
plt.xlabel(r'$\gamma_{\mathrm{eff}}$', fontsize=FS)
plt.ylabel(r'$\lambda$', fontsize=FS)

# Ticks e configurações
plt.xticks(fontsize=FS*4/5)
plt.yticks(fontsize=FS*4/5)
plt.tick_params(axis='y', which='major', pad=PAD)
plt.tick_params(axis='x', which='major', pad=PAD)

# Limites dos eixos
plt.xlim(-0.01, 1/2 + 0.015)
plt.ylim(-0.005, 1/4 + 0.005)

# Configurações da grade
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.15)
plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.15)
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

# Ajuste de layout e exibição do gráfico
#plt.tight_layout()
#plt.suptitle(f'{nome_arquivo} | Col. Sim. = {len(X_PT)} | Col. Exp. = {len(X_P)}')
plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.2)
#plt.show()
plt.savefig('Gráficos/LGLF.png', dpi=600)
plt.savefig('Gráficos/LGLF.pdf')
#plt.savefig('Gráficos/LyapGamma/' + str(nome_arquivo) + '.pdf')
#plt.savefig('Gráficos/Quirino/Poincaré/Comp/png/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).png', dpi=600)
#plt.savefig('Gráficos/Quirino/Poincaré/Comp/pdf/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).pdf', dpi=600)
#plt.savefig('Gráficos/Quirino/Poincaré/Comp/svg/' + str(nome_arquivo) + '_(Comp_Poincare_Comp).svg', dpi=600)
#plt.show()
