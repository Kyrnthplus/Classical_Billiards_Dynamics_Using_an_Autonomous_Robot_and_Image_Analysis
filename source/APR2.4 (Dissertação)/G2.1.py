import matplotlib.pyplot as plt
import numpy as np

pi_value = np.pi
FS = 30
PAD=10



plt.rcParams['font.family']= 'serif'
plt.rcParams['font.serif'] = 'FreeSerif'	
plt.rcParams['mathtext.fontset'] = 'stix'

# Título da figura
plt.suptitle('Mapa de Poincaré')
# Criando uma figura vazia
plt.figure(figsize=(9, 6))
# Rótulos dos eixos e ticks
plt.xlabel(r'$\ell$', fontsize=FS)
plt.ylabel(r'sin $\phi$', fontsize=FS)
plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)
plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS*4/5)

plt.tick_params(axis='y', which='major', pad=PAD)
plt.tick_params(axis='x', which='major', pad=PAD)

# Limites dos eixos
plt.xlim(-0.1, 2 * np.pi + 0.1)
plt.ylim(-1.05, 1.05)

# Configurações da grade
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray',alpha=0.25)
plt.grid(which='major', linestyle='-', linewidth='0.5', color='gray', alpha=0.25)
plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

# Ajuste de layout e exibição do gráfico
plt.tight_layout()
plt.show()

