import matplotlib.pyplot as plt
import numpy as np

pi_value = np.pi
FS = 18

# Criando uma figura vazia
plt.figure(figsize=(9, 6))

# Título da figura
plt.suptitle('Mapa de Poincaré')

# Rótulos dos eixos e ticks
plt.xlabel(r'$\rho$', fontsize=FS)
plt.ylabel(r'sin $\phi$', fontsize=FS)
plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value], ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'], fontsize=FS*4/5)
plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS*4/5)

# Limites dos eixos
plt.xlim(-0.2, 2 * np.pi + 0.2)
plt.ylim(-1.1, 1.1)

# Configurações da grade
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
plt.grid(True)

# Ajuste de layout e exibição do gráfico
plt.tight_layout()
plt.show()

