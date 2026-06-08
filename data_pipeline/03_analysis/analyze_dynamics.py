import os
import sys
import argparse
import glob
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Configura para execução sem interface gráfica (non-interactive)
import matplotlib.pyplot as plt

# Adiciona o caminho pai para importar geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def analyze_file(file_prefix):
    print(f"Analisando dinâmica para prefixo: {file_prefix}")
    base_name = os.path.basename(file_prefix)
    nome_sem_extensao = os.path.splitext(base_name)[0]

    # Define os caminhos dos arquivos de dados processados
    traj_path = f"../../data/processed/{nome_sem_extensao}_(Traj).dat"
    th_ka_path = f"../../data/processed/{nome_sem_extensao}_(T_Th_Ka_V).dat"
    per_sin_path = f"../../data/processed/{nome_sem_extensao}_(Per_SinTheta).dat"
    col_xy_path = f"../../data/processed/{nome_sem_extensao}_Colisao(X-Y).dat"

    # Verifica se os arquivos necessários existem
    for p in [traj_path, th_ka_path, per_sin_path, col_xy_path]:
        if not os.path.exists(p):
            print(f"Erro: Arquivo processado {p} não encontrado. Execute o detector de colisões primeiro.")
            return

    # Carrega dados
    Xr, Yr, X, Y = np.loadtxt(traj_path, unpack=True)
    t_list, theta_list, kappa, vel = np.loadtxt(th_ka_path, unpack=True)
    X_P, Y_P = np.loadtxt(per_sin_path, unpack=True)
    X_C, Y_C = np.loadtxt(col_xy_path, unpack=True)

    # Re-estimação de parâmetros geométricos a partir das colisões
    Cym = 0.0
    pontos_x_sup = []
    pontos_y_sup = []
    pontos_x_inf = []
    pontos_y_inf = []
    for i in range(len(Y_C)):
        if Y_C[i] > Cym:
            pontos_x_sup.append(X_C[i])
            pontos_y_sup.append(Y_C[i])
        else:
            pontos_x_inf.append(X_C[i])
            pontos_y_inf.append(Y_C[i])

    centro_sup, raio_sup, _, _ = gu.encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
    centro_inf, raio_inf, _, _ = gu.encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)

    centro_AB = (centro_inf[0] - centro_sup[0], centro_inf[1] - centro_sup[1])
    a = (centro_inf[1] - centro_sup[1]) / 2
    gamma = 2 * a / (raio_sup + raio_inf)
    modulo_AB = np.linalg.norm(centro_AB)

    print(f"Parâmetros estimados: Gamma = {gamma:.5f}, a = {a:.5f}, Raio Superior = {raio_sup:.3f}, Raio Inferior = {raio_inf:.3f}")

    # Cálculo do expoente de Lyapunov
    delta = np.array([random.uniform(0.1, 1.0), random.uniform(0.1, 1.0)])
    delta /= np.linalg.norm(delta)
    n_steps = len(t_list)

    os.makedirs("../../data/results", exist_ok=True)
    lyap_data_path = f"../../data/results/{nome_sem_extensao}_Lyapunov.dat"

    with open(lyap_data_path, "w") as fout:
        lambda_ = 0.0
        for ii in range(n_steps):
            u = delta[0]
            delta[0] = u + t_list[ii] * delta[1]
            delta[1] = delta[1]

            u = delta[0]
            delta[0] = -u
            delta[1] = vel[ii] * 2. * kappa[ii] / np.cos(theta_list[ii]) * u - delta[1]

            lambda_ += np.log(np.linalg.norm(delta))
            fout.write(f"{sum(t_list[:(ii + 1)]):.6f} {(lambda_ / sum(t_list[:(ii + 1)])):.6f}\n")
            delta /= np.linalg.norm(delta)

    LE = lambda_ / sum(t_list[:n_steps])
    print(f"Expoente de Lyapunov calculado (LE): {LE:.5f}")

    # Cores baseadas no tipo de arquivo
    if not nome_sem_extensao.endswith("T_S"):
        COR = '#ff972f'  # Laranja para experimental
    else:
        COR = '#812fff'  # Roxo para simulado

    # Carrega dados do Lyapunov calculado para plot
    lyap_x, lyap_y = np.loadtxt(lyap_data_path, unpack=True)

    # Geração dos Gráficos
    FS = 12
    plt.figure(figsize=(15, 10))
    plt.suptitle(f"{nome_sem_extensao} | Gamma = {gamma:.5f} | Expoente Lyapunov = {LE:.5f} | Colisões = {len(theta_list)}")

    # Plot 1: Trajetória
    plt.subplot(2, 3, 1)
    plt.plot(X, Y, color=COR, linestyle='solid', linewidth=1)
    plt.xlabel('X', fontsize=FS)
    plt.ylabel('Y', fontsize=FS)
    plt.axis('square')
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 2: Posições de Colisão
    # Recalcula escalas para plot igual ao original
    NX = np.max(X) - np.min(X)
    NXc = np.max(X_C) - np.min(X_C)
    N_ratio = NX / NXc if NXc > 0 else 1.0
    X_C_scaled = X_C * N_ratio
    Y_C_scaled = Y_C * N_ratio

    plt.subplot(2, 3, 2)
    plt.plot(X_C_scaled, Y_C_scaled, color=COR, linestyle='none', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X', fontsize=FS)
    plt.ylabel('Y', fontsize=FS)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 3: Mapa de Poincaré
    plt.subplot(2, 3, 3)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    pi_value = np.pi
    x_ticks_positions = [0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value]
    x_ticks_labels = ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    plt.xticks(x_ticks_positions, x_ticks_labels)
    plt.xlabel(r'$\rho$', fontsize=FS)
    plt.ylabel(r'sin $\phi$', fontsize=FS)
    plt.yticks([-1, -0.5, 0, 0.5, 1])
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 4: Evolução de Lyapunov
    plt.subplot(2, 3, 4)
    plt.axhline(LE, color='black', linestyle='solid', linewidth=1, alpha=1, label=f'LE ({LE:.5f})')
    plt.plot(lyap_x, lyap_y, color=COR)
    plt.ylim(lyap_y[-1] - 0.55, lyap_y[-1] + 0.55)
    plt.ylabel(r'$\gamma$', fontsize=FS)
    plt.xlabel('t', fontsize=FS)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 5: Recorrência e Recurrence Rate (RR) com e=0.05
    P_norm = X_P / (2 * np.pi)
    A_norm = (Y_P + 1) / 2
    Tam = len(P_norm)

    e1 = 0.05
    MQ1 = np.zeros((Tam, Tam))
    SOMA1 = 0
    for i in range(Tam):
        for k in range(Tam):
            if P_norm[i] <= 0.1 and P_norm[k] >= 0.9:
                if abs(P_norm[i] - P_norm[k] - 1) < e1 and abs(A_norm[i] - A_norm[k] - 1) < e1:
                    MQ1[i][k] = 1
                    SOMA1 += 1
            if abs(P_norm[i] - P_norm[k]) < e1 and abs(A_norm[i] - A_norm[k]) < e1:
                MQ1[i][k] = 1
                SOMA1 += 1
    RR1 = SOMA1 / (Tam * Tam) if Tam > 0 else 0
    x_coords1, y_coords1 = np.where(MQ1 == 1)

    plt.subplot(2, 3, 5)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.plot(x_coords1, y_coords1, color=COR, linestyle='none', marker='o', markersize=3, markeredgecolor='black')
    plt.title(f'RR={RR1:.4f} | e = {e1}')
    plt.xlabel('Índice k')
    plt.ylabel('Índice i')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 6: Recorrência e RR com e=0.01
    e2 = 0.01
    MQ2 = np.zeros((Tam, Tam))
    SOMA2 = 0
    for i in range(Tam):
        for k in range(Tam):
            if (P_norm[i] <= 0.1 and P_norm[k] >= 0.9) or (P_norm[k] <= 0.1 and P_norm[i] >= 0.9):
                if abs(P_norm[i] - P_norm[k] - 1) < e2 and abs(A_norm[i] - A_norm[k] - 1) < e2:
                    MQ2[i][k] = 1
                    SOMA2 += 1
            if abs(P_norm[i] - P_norm[k]) < e2 and abs(A_norm[i] - A_norm[k]) < e2:
                MQ2[i][k] = 1
                SOMA2 += 1
    RR2 = SOMA2 / (Tam * Tam) if Tam > 0 else 0
    x_coords2, y_coords2 = np.where(MQ2 == 1)

    plt.subplot(2, 3, 6)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.plot(x_coords2, y_coords2, color=COR, linestyle='none', marker='o', markersize=3, markeredgecolor='black')
    plt.title(f'RR={RR2:.3g} | e = {e2}')
    plt.xlabel('Índice k')
    plt.ylabel('Índice i')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Salva o gráfico agrupado
    plt.savefig(f"../../data/results/{nome_sem_extensao}.png", dpi=350)
    plt.close('all')

    # Reconfigura fontes para PDF
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'stix'

    # Gráfico Extra em PDF com 3 colunas (Trajectory, Poincaré, Recurrence e=0.01)
    FS_PDF = 24
    plt.figure(figsize=(17, 6.3))
    plt.suptitle(f"{nome_sem_extensao} | "r"$\gamma$" f" = {gamma:.3g} | "r"$\lambda$" f" = {LE:.3g} | Colisões = {len(theta_list)} | $RR$={RR2:.3g} | "r"$\varepsilon$" f" = {e2}", fontsize=FS_PDF*3/4)

    # Coluna 1: Trajetória + Colisão
    plt.subplot(1, 3, 1)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.scatter(X, Y, color='black', s=0.1, alpha=0.55, zorder=2, marker='o')
    plt.plot(X_C_scaled, Y_C_scaled, color=COR, linestyle='none', marker='.', markersize=10, markeredgecolor='black', zorder=3)
    plt.xlabel(r'$X$', fontsize=FS_PDF)
    plt.ylabel(r'$Y$', fontsize=FS_PDF)
    plt.xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF*3/4)
    plt.yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF*3/4)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Coluna 2: Mapa de Poincaré
    plt.subplot(1, 3, 2)
    plt.plot(X_P, Y_P, color=COR, linestyle='none', marker='.', markersize=10, markeredgecolor='black')
    plt.xticks(x_ticks_positions, x_ticks_labels, fontsize=FS_PDF*3/4)
    plt.xlabel(r'$\ell$', fontsize=FS_PDF)
    plt.ylabel(r'sin $\phi$', fontsize=FS_PDF)
    plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS_PDF*3/4)
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Coluna 3: Matriz de Recorrência
    plt.subplot(1, 3, 3)
    plt.minorticks_on()
    plt.xticks(fontsize=FS_PDF*3/4)
    plt.yticks(fontsize=FS_PDF*3/4)
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.plot(x_coords2, y_coords2, color=COR, linestyle='none', marker='o', markersize=5, markeredgecolor='black', alpha=1)
    plt.xlabel(r'Índice $i$', fontsize=FS_PDF)
    plt.ylabel(r'Índice $j$', fontsize=FS_PDF)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
    plt.subplots_adjust(left=0.075, right=0.975, top=0.85, bottom=0.15, wspace=0.25)

    plt.savefig(f"../../data/results/{nome_sem_extensao}_report.png", dpi=350)
    plt.close('all')

    # Gráfico Isolado de Trajetória + Colisão
    plt.figure(figsize=(8, 7))
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.scatter(X, Y, color='black', s=0.3, alpha=0.55, zorder=2, marker='o', label='Trajetória')
    plt.plot(X_C_scaled, Y_C_scaled, color=COR, linestyle='none', marker='.', markersize=12.5, markeredgecolor='black', zorder=3, label='Colisão')
    plt.legend(loc='upper right', fontsize=FS_PDF*3/4)
    plt.xlabel(r'$X$', fontsize=FS_PDF)
    plt.ylabel(r'$Y$', fontsize=FS_PDF)
    plt.xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF)
    plt.yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True, pad=10)
    plt.subplots_adjust(left=0.2, right=0.90, top=0.95, bottom=0.15, wspace=0.25)
    plt.savefig(f"../../data/results/{nome_sem_extensao}_TC.png", dpi=350)
    plt.close('all')

    # Gráfico Isolado de Poincaré (Modelo Tiago)
    NX_T = 9
    NY_T = 6
    FS_T = 30
    PAD_T = 10
    plt.figure(figsize=(NX_T, NY_T))
    plt.plot(X_P, Y_P, color=COR, linestyle='none', marker='.', markersize=10, markeredgecolor='black', label='Medição')
    plt.xlabel(r'$ \ell $', fontsize=FS_T)
    plt.ylabel(r'sin$~\phi$', fontsize=FS_T)
    plt.yticks(np.arange(-1, 1.001, 0.5), fontsize=FS_T*4/5)
    plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value],
               ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'],
               fontsize=FS_T*4/5)
    plt.ylim(-1, 1)
    plt.xlim(0, 2 * pi_value + 0.01)
    plt.tick_params(axis='y', which='major', pad=PAD_T)
    plt.tick_params(axis='x', which='major', pad=PAD_T)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.20)
    plt.savefig(f"../../data/results/{nome_sem_extensao}Tiago.png")
    plt.close('all')

    print(f"Gráficos salvos com sucesso em data/results/ para: {nome_sem_extensao}")

    # Atualiza ou gera arquivo acumulado de parâmetros na pasta results
    val_file = "../../data/results/N_G_LE_Ri_Rs_M_valores.txt"
    exists = os.path.exists(val_file)
    with open(val_file, "a" if exists else "w") as f:
        if not exists:
            f.write("Nome do Exp | Gamma | Expoent Lyapunov | Zeta | R_i | R_s | Modulo\n")
        f.write(f"{nome_sem_extensao} {gamma:.6f} {LE:.6f} {N_ratio:.6f} {raio_inf:.6f} {raio_sup:.6f} {modulo_AB/2:.6f}\n")

def main():
    parser = argparse.ArgumentParser(description="Análise dinâmica Lemon Billiard (Lyapunov e Poincaré)")
    parser.add_argument("--file", type=str, help="Nome do arquivo em data/processed/ (sem sufixos) para analisar")
    args = parser.parse_args()

    # Define o diretório de execução relativo ao script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    processed_dir = "../../data/processed"
    if args.file:
        prefix = os.path.join(processed_dir, args.file)
        analyze_file(prefix)
    else:
        # Modo lote: busca arquivos (Traj).dat na pasta processed para deduzir os prefixos
        files = glob.glob(os.path.join(processed_dir, "*_(Traj).dat"))
        if not files:
            print(f"Nenhum arquivo processado encontrado em {processed_dir}")
            return
        for f in sorted(files):
            prefix = f.replace("_(Traj).dat", "")
            analyze_file(prefix)

if __name__ == "__main__":
    main()
