import os
import sys
import argparse
import random
import numpy as np

# Adiciona o caminho pai para importar geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def run_simulation(init_file=None, test_mode=False, custom_gamma=0.5):
    print("Iniciando Simulação Lemon Billiard...")

    # Parâmetros padrão
    R1 = 1.0
    R2 = 1.0
    gamma = custom_gamma
    a = R1 * gamma  # R1 e R2 médios vezes gamma
    Vm = 0.5       # Velocidade média padrão
    x0 = 0.1
    y0 = 0.1
    vx0 = 0.4
    vy0 = 0.3
    nome_saida = "simulacao"

    # Se fornecido um arquivo experimental para mimetizar
    if init_file:
        base = os.path.basename(init_file)
        nome_sem_extensao = os.path.splitext(base)[0]
        nome_saida = f"{nome_sem_extensao}"

        # Tenta carregar os dados brutos para extrair velocidade e posição inicial
        try:
            X, Y, _, _ = np.loadtxt(init_file, unpack=True)
        except Exception:
            try:
                X, Y = np.loadtxt(init_file, usecols=(0, 1), unpack=True)
            except Exception as e:
                print(f"Erro ao carregar arquivo de inicialização: {e}")
                return

        x0 = X[0]
        y0 = Y[0]
        # Estima velocidade inicial baseada nos primeiros passos
        if len(X) > 2:
            vx0 = (X[1] - X[0]) * 30
            vy0 = (Y[1] - Y[0]) * 30
            Vm = np.mean(np.sqrt(np.gradient(X, 1/30)**2 + np.gradient(Y, 1/30)**2))
        else:
            vx0 = 0.3
            vy0 = 0.3
            Vm = 0.4

        # Recalcula geometria simulada se o arquivo processado existir
        processed_xy = f"../../data/processed/{nome_sem_extensao}_Colisao(X-Y).dat"
        if os.path.exists(processed_xy):
            try:
                X_C, Y_C = np.loadtxt(processed_xy, unpack=True)
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
                _, R1, _, _ = gu.encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
                _, R2, _, _ = gu.encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)
                centro_sup, _, _, _ = gu.encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
                centro_inf, _, _, _ = gu.encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)
                a = (centro_inf[1] - centro_sup[1]) / 2
                gamma = 2 * a / (R1 + R2)
            except Exception as e:
                print(f"Aviso: Falha ao ler parâmetros processados, usando defaults. Erro: {e}")

    dt = 0.01
    x_traj = [x0]
    y_traj = [y0]

    # Limite de colisões a simular
    max_colisoes = 20 if test_mode else 100
    coli = [[x0], [y0]]

    x = x0
    y = y0
    v = np.array([vx0, vy0])
    v = gu.calcular_versor(v) * Vm
    vm = gu.calcular_modulo(v)

    centro = [[0, 0], [a, -a]] # centro[0] = x_cent, centro[1] = y_cent
    Anda = 10
    Para = 1000

    print(f"Parâmetros da Simulação: R1={R1:.3f}, R2={R2:.3f}, a={a:.3f}, Gamma={gamma:.4f}, Vm={Vm:.4f}")
    print(f"Posição Inicial: ({x0:.3f}, {y0:.3f}) | Velocidade Inicial: ({v[0]:.3f}, {v[1]:.3f})")

    steps_count = 0
    max_steps = 10000 if test_mode else 1000000

    while len(coli[0]) <= max_colisoes and steps_count < max_steps:
        x += v[0] * dt
        y += v[1] * dt
        steps_count += 1

        # Reflexão nas bordas
        if y <= 0:
            raio1 = np.sqrt((x - centro[0][0])**2 + (y - centro[1][0])**2)
            if raio1 > R1:
                # Evita colisões múltiplas no mesmo ponto recuando um passo
                dist = np.sqrt((x - coli[0][-1])**2 + (y - coli[1][-1])**2)
                if dist <= vm * 15:
                    x = x_traj[-1]
                    y = y_traj[-1]
                coli[0].append(x)
                coli[1].append(y)

                Tcoli = len(coli[0])
                Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][0]]
                phig, phir = gu.calcular_angulo(Vdir, Rdir)
                thetar = np.pi - 2 * phir

                vz = gu.produto_vetorial(Rdir, Vdir)
                if vz > 0:
                    Fdir = np.array([v[0] * np.cos(thetar) - v[1] * np.sin(thetar), +v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                else:
                    Fdir = np.array([v[0] * np.cos(thetar) + v[1] * np.sin(thetar), -v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])

                v[0] = Fdir[0]
                v[1] = Fdir[1]

                for _ in range(Para):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * Anda * dt
                y += v[1] * Anda * dt
        else:
            raio2 = np.sqrt((x - centro[0][1])**2 + (y - centro[1][1])**2)
            if raio2 > R2:
                dist = np.sqrt((x - coli[0][-1])**2 + (y - coli[1][-1])**2)
                if dist <= vm * 15:
                    x = x_traj[-1]
                    y = y_traj[-1]
                coli[0].append(x)
                coli[1].append(y)

                Tcoli = len(coli[0])
                Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                Rdir = [coli[0][Tcoli - 1] - centro[0][1], coli[1][Tcoli - 1] - centro[1][1]]
                phig, phir = gu.calcular_angulo(Vdir, Rdir)
                thetar = np.pi - 2 * phir

                vz = gu.produto_vetorial(Rdir, Vdir)
                if vz > 0:
                    Fdir = np.array([v[0] * np.cos(thetar) - v[1] * np.sin(thetar), +v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])
                else:
                    Fdir = np.array([v[0] * np.cos(thetar) + v[1] * np.sin(thetar), -v[0] * np.sin(thetar) + v[1] * np.cos(thetar)])

                v[0] = Fdir[0]
                v[1] = Fdir[1]

                for _ in range(Para):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * Anda * dt
                y += v[1] * Anda * dt

        x_traj.append(x)
        y_traj.append(y)

    # Cria pasta raw se necessário
    os.makedirs("../../data/raw", exist_ok=True)
    out_file = f"../../data/raw/{nome_saida}_T_S.txt"
    with open(out_file, "w") as f:
        for i in range(len(x_traj)):
            f.write(f"{x_traj[i]:.6f} {y_traj[i]:.6f} {x_traj[i]:.6f} {y_traj[i]:.6f}\n")

    print(f"Simulação concluída com sucesso! Trajetória gravada em {out_file} ({len(x_traj)} pontos).")

def main():
    parser = argparse.ArgumentParser(description="Simulador Lemon Billiard")
    parser.add_argument("--init_file", type=str, help="Arquivo experimental para copiar condições iniciais")
    parser.add_argument("--gamma", type=float, default=0.5, help="Parâmetro Gamma do bilhar (default: 0.5)")
    parser.add_argument("--test", action="store_true", help="Executa simulação rápida para verificação de teste")
    args = parser.parse_args()

    # Define o diretório de execução relativo ao script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    run_simulation(init_file=args.init_file, test_mode=args.test, custom_gamma=args.gamma)

if __name__ == "__main__":
    main()
