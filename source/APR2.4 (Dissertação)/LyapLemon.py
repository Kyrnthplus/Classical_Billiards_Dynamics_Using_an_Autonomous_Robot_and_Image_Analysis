import numpy as np
import random
import matplotlib.pyplot as plt

# Solicitar nome do arquivo de entrada (sem .dat)
Nome = input("Digite o nome do arquivo de entrada (sem .dat): ")

# Cálculo do expoente de Lyapunov
# Inicialização de um vetor delta com valores aleatórios entre 0 e 1
delta = [random.uniform(0, 1), random.uniform(0, 1)]
# Normalização do vetor delta para ter comprimento unitário
delta /= np.linalg.norm(delta)

# Rótulo para o cálculo do expoente de Lyapunov
label = 5

# Carregar os dados do arquivo de entrada
t_list, theta_list, kappa, vel = np.loadtxt('DadosTratados/' + str(Nome) +"_(T_Th_Ka_V).dat", unpack=True)

# Número de passos de tempo no conjunto de dados
n_steps = len(t_list)

# Abrir arquivo de saída para escrita
with open('Lyapunov/' + str(Nome) + '.dat', 'w') as fout:
    lambda_ = 0.0
    # Iterar através dos passos de tempo
    for ii in range(n_steps):
        # Atualizar delta de acordo com as equações
        u = delta[0]
        delta[0] = u + t_list[ii] * delta[1]
        delta[1] = delta[1]

        u = delta[0]
        delta[0] = -u
        delta[1] = vel[ii] * 2. * kappa[ii] / np.cos(theta_list[ii]) * u - delta[1]

        # Atualizar o valor do expoente de Lyapunov
        lambda_ += np.log(np.linalg.norm(delta))
        # Escrever os valores de tempo e expoente de Lyapunov no arquivo de saída
        fout.write("%f %f\n" % (sum(t_list[:(ii + 1)]), lambda_ / sum(t_list[:(ii + 1)])))

        # Normalizar novamente o vetor delta para comprimento unitário
        delta /= np.linalg.norm(delta)

# Exibir o valor calculado do expoente de Lyapunov
print(f'lambda({label}) = {lambda_ / sum(t_list[:n_steps])}')
LE = lambda_ / sum(t_list[:n_steps])  # Calcular o valor do expoente de Lyapunov
# Carregar dados do arquivo de saída para plotagem
x, y = np.loadtxt('Lyapunov/' + str(Nome) + '.dat', unpack=True)

# Plotagem do gráfico
plt.axhline(LE, color='black', linestyle='solid', linewidth=1, alpha=1, label=f'LE ({LE:.5f})')

plt.plot(x, y, color='#ff972f', )

plt.minorticks_on()

#plt.grid(which='minor', linestyle='dashdot', linewidth='0.1', color='gray', alpha=0.5)
#plt.grid(True)
plt.legend(loc='lower right')

#plt.gca().set_aspect('equal', adjustable='box')
plt.ylabel(r'$\gamma$')
plt.xlabel('t')
plt.savefig('Gráficos/' + str(Nome) +'_LE='+str(LE)+ '.png', dpi=350)
plt.show()
