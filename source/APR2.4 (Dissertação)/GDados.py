import matplotlib.pyplot as plt
import numpy as np
Nome=str(input("nome do arquivo sem extensão:"))
Traj=np.loadtxt("DadosTratados/"+str(Nome)+"_(Traj).dat")
Coli=np.loadtxt("DadosTratados/"+str(Nome)+"_Colisao(X-Y).dat")
x=Traj.T[0]
y=Traj.T[1]
X=Coli.T[0]*1.0
Y=Coli.T[1]*1.0
#print(Traj)
#print(x)
#print(y)
pi_value = np.pi
FS = 18

# Criando uma figura vazia
plt.figure(figsize=(9, 9))

# Título da figura
#plt.suptitle('Mapa de Poincaré')

plt.scatter(X,Y,s=15,c="red")
# Rótulos dos eixos e ticks
#plt.xlabel(r'$\ell$', fontsize=FS)
#plt.ylabel(r'sin $\phi$', fontsize=FS)
#plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)
#plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS*4/5)

# Limites dos eixos
#plt.xlim(-0.2, 2 * np.pi + 0.2)
#plt.ylim(-1.1, 1.1)

# Configurações da grade
#plt.minorticks_on()
#plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray',alpha=0.25)
#plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)
#plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

# Ajuste de layout e exibição do gráfico
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.tight_layout()
plt.savefig('grafico0.png', transparent=True, dpi=900)
plt.figure(figsize=(9, 9))
plt.scatter(x,y,s=0.5,c="red",alpha=0.5)
plt.gca().set_xticks([])
plt.gca().set_yticks([])
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.tight_layout()
plt.savefig('grafico1.png', transparent=True, dpi=900)

