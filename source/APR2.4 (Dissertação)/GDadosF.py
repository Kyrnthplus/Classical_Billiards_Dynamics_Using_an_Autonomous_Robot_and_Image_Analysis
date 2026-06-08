#Esse programa extrai as colisões e a trajetoria separadamente e exporta para png sem distorcer

import matplotlib.pyplot as plt
import numpy as np

# Solicitar o nome do arquivo sem extensão
Nome = str(input("Nome do arquivo sem extensão: "))

# Carregar os dados
Traj = np.loadtxt(f"DadosTratados/{Nome}_(Traj).dat")
Coli = np.loadtxt(f"DadosTratados/{Nome}_Colisao(X-Y).dat")

# Definir os dados
x, y = Traj.T[0], Traj.T[1]
X, Y = Coli.T[0], Coli.T[1]

# Definir constantes
FS = 18
COR = '#ff972f'

# Plotar a trajetória (gráfico 0) usando scatter
plt.figure()
#plt.scatter(x, y, color='black', s=0.25, label='Trajectory',alpha=0.5)
plt.scatter(x, y, color='red', s=0.25, label='Trajectory',alpha=0.5)
# Manter a escala dos eixos X e Y igual
plt.gca().set_aspect('equal', adjustable='box')

# Remover ticks e bordas do gráfico
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Salvar o gráfico 0
plt.savefig('grafico0.png', transparent=True, dpi=900)

# Criar nova figura para as colisões (gráfico 1)
plt.figure()
#plt.plot(X, Y, color=COR, linestyle='none', marker='.', markersize=10, markeredgecolor='black', label='Collisions')
plt.plot(X, Y, color='red', linestyle='none', marker='.', markersize=5, markeredgecolor='red', label='Collisions')

# Manter a escala dos eixos X e Y igual
plt.gca().set_aspect('equal', adjustable='box')

# Remover ticks e bordas do gráfico
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)

# Salvar o gráfico 1
plt.savefig('grafico1.png', transparent=True, dpi=900)

