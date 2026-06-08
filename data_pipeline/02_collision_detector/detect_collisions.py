import os
import sys
import argparse
import glob
import numpy as np
from scipy.signal import butter, filtfilt

# Adiciona o caminho pai para importar geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def Lowpass(data, cutoff, fs, order):
    normal_cutoff = cutoff / fs
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def StraightWalk(t, x, y, v):
    ts = []
    xs = []
    ys = []
    for i in range(len(x)):
        if v[i] > 0.1:
            xs.append(x[i])
            ys.append(y[i])
            ts.append(t[i])
    return ts, xs, ys

def Col(ts, xs, ys, dt):
    tdiff = np.diff(ts)
    cont0 = 0
    Fl = 0
    refp = [[], []]
    T = []
    for i in range(len(ts)-1):
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            refp[0].append(x1)
            refp[1].append(y1)
            T.append(Fl)
            Fl = 0
        Fl = Fl + dt
    return refp[0], refp[1], np.array(T).T

def process_file(file_path):
    print(f"Processando arquivo: {file_path}")
    base_name = os.path.basename(file_path)
    nome_sem_extensao = os.path.splitext(base_name)[0]

    # Carrega dados
    try:
        X, Y, ex, ey = np.loadtxt(file_path, unpack=True)
    except Exception as e:
        print(f"Erro ao ler arquivo {file_path}: {e}")
        # Tenta ler com apenas duas colunas caso seja simulação
        try:
            X, Y, _, _ = np.loadtxt(file_path, unpack=True)
        except Exception as e2:
            try:
                X, Y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)
            except Exception as e3:
                print(f"Falha total ao ler coordenadas: {e3}")
                return

    # Correção de rotação (se não for simulado com sufixo T_S)
    if not nome_sem_extensao.endswith("T_S"):
        Menor_X = np.min(X)
        X_i = np.where(X == Menor_X)[0][0]
        Maior_X = np.max(X)
        X_I = np.where(X == Maior_X)[0][0]

        Vx_Exp = [X[X_I] - X[X_i], Y[X_I] - Y[X_i]]
        Vi = [1, 0]
        Ang_Expg, Ang_Expr = gu.calcular_angulo(Vx_Exp, Vi)
        print(f"Angulo de correcao de rotacao: {Ang_Expg:.3f} graus")
        
        TamX = len(X)
        if Ang_Expg < 5:
            if Vx_Exp[1] < 0:
                for i in range(TamX - 1):
                    X[i] = +X[i] * np.cos(Ang_Expr) - Y[i] * np.sin(Ang_Expr)
                    Y[i] = +X[i] * np.sin(Ang_Expr) + Y[i] * np.cos(Ang_Expr)
            else:
                for i in range(TamX - 1):
                    X[i] = +X[i] * np.cos(Ang_Expr) + Y[i] * np.sin(Ang_Expr)
                    Y[i] = -X[i] * np.sin(Ang_Expr) + Y[i] * np.cos(Ang_Expr)

        Norm = (np.max(Y) - np.min(Y)) * 0.5
        RrR = 1.2 / 533
        Xr = (X - np.mean(X)) * RrR
        Yr = (Y - np.mean(Y)) * RrR
        X = Xr
        Y = Yr
    else:
        # Se for simulado, já está em dimensões corretas
        Xr = X.copy()
        Yr = Y.copy()

    # Cálculo da velocidade para detecção de colisões
    N = len(X)
    t = np.linspace(0, (N - 1) / 30, N)
    dt = t[1] - t[0]

    Vx = np.gradient(X, dt)
    Vy = np.gradient(Y, dt)
    V = np.sqrt(Vx**2 + Vy**2)
    Vm = np.mean(V)

    # Transformada de Fourier para estimar frequências
    freq = np.fft.fftfreq(N, dt)
    modulo = freq > 0
    fourier = freq[modulo]
    F = np.sqrt(fourier ** 2)
    fs = max(F)
    cutoff = fs / 10
    order = 3

    # Filtragem passa-baixa de velocidade e aceleração
    Vn = Lowpass(V, cutoff, fs, order)

    # Detecção das colisões por descontinuidade da velocidade
    ts, Xs, Ys = StraightWalk(t, X, Y, Vn)
    Cx, Cy, TList = Col(ts, Xs, Ys, dt)

    print(f"Colisoes detectadas: {len(Cx)}")
    if len(Cx) < 3:
        print("Aviso: Poucas colisões detectadas. O arquivo pode não ter dados suficientes ou o limiar é inadequado.")
        return

    Cym = 0.0
    Altura_y = max(Cy) + np.abs(min(Cy))

    # Separação dos pontos superior e inferior para ajuste dos círculos
    pontos_x_sup = []
    pontos_y_sup = []
    pontos_x_inf = []
    pontos_y_inf = []
    for i in range(len(Cy)):
        if Cy[i] > Cym:
            pontos_x_sup.append(Cx[i])
            pontos_y_sup.append(Cy[i])
        else:
            pontos_x_inf.append(Cx[i])
            pontos_y_inf.append(Cy[i])

    # Ajuste dos círculos
    centro_sup, raio_sup, _, _ = gu.encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
    centro_inf, raio_inf, _, _ = gu.encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)

    centro_AB = (centro_inf[0] - centro_sup[0], centro_inf[1] - centro_sup[1])
    a = (centro_inf[1] - centro_sup[1]) / 2
    gamma = 2 * a / (raio_sup + raio_inf)

    R = np.pi / (2 * np.arcsin(np.sqrt(1 - (gamma)**2)))
    Re = (raio_sup + raio_inf) / 2
    L0 = 2 * np.pi
    L1 = 5.01
    h = L1 * (1 - gamma) / (2 * np.arcsin(np.sqrt(1 - gamma**2)))
    
    # Fatores de normalização geométrica
    N_y = R / Re
    N_Yy = h / Altura_y

    # Aplicação da normalização geométrica
    Cx_norm = (Cx - np.mean(Cx)) * N_y
    Cy_norm = (Cy - np.mean(Cy)) * N_y
    X_norm = (X - np.mean(X)) * N_y
    Y_norm = (Y - np.mean(Y)) * N_y

    L1_wall, L2_wall = gu.LemonWall(X_norm, Y_norm, (raio_sup + raio_inf)/2, a)
    Inc, Ref, AngEff, FF = gu.EffA(ts, Xs, Ys, L1_wall, L2_wall, a)

    # Cálculo das coordenadas de Poincaré
    Comp = []
    Kappa = []
    V_col = []
    ThetaList = []
    AlphaList = []
    PerList = []
    Nsteps = len(Cx_norm)

    for i in range(1, Nsteps - 1):
        c1 = [Cx_norm[i + 1], Cy_norm[i + 1]]
        c2 = [Cx_norm[i], Cy_norm[i]]
        c3 = [Cx_norm[i - 1], Cy_norm[i - 1]]
        xx = Cx_norm[i]
        yy = Cy_norm[i]

        if yy >= np.mean(Cy_norm):
            R_vec = gu.Sub(c2, [centro_sup[0], centro_sup[1]])
            Per = np.arccos(xx / (np.sqrt(xx**2 + yy**2))) + np.pi
        else:
            R_vec = gu.Sub(c2, [centro_inf[0], centro_inf[1]])
            Per = np.arccos(-xx / (np.sqrt(xx**2 + yy**2)))

        vec = gu.Sub(c2, c3)
        vecRef = gu.Sub(c2, c1)
        Reflec = gu.Ang(vec, R_vec)

        if (c2[0] * vecRef[1] - c2[1] * vecRef[0]) < 0:
            Reflec = -Reflec

        Alf = gu.Ang(vecRef, R_vec)
        Comp.append(np.linalg.norm(vec))
        Kappa.append(1.0 / np.linalg.norm(R_vec))
        Velo = np.linalg.norm(vec) / TList[i]
        V_col.append(Velo)
        ThetaList.append(Reflec)
        AlphaList.append(Alf)
        PerList.append(Per)

    # Garantir que a pasta processed exista
    os.makedirs("../../data/processed", exist_ok=True)

    # Salva arquivos de saída processados
    traj_path = f"../../data/processed/{nome_sem_extensao}_(Traj).dat"
    with open(traj_path, "w") as f:
        for i in range(len(Xr)):
            f.write(f"{Xr[i]:.6f} {Yr[i]:.6f} {X_norm[i]:.6f} {Y_norm[i]:.6f}\n")

    th_ka_path = f"../../data/processed/{nome_sem_extensao}_(T_Th_Ka_V).dat"
    mean_V_col = np.mean(V_col) if len(V_col) > 0 else 1.0
    # Calcular VList / mean(V) como no código original
    VList = FF / TList
    with open(th_ka_path, "w") as f:
        for i in range(len(Kappa)):
            f.write(f"{(TList[i] * mean_V_col):.6f} {ThetaList[i]:.6f} {Kappa[i]:.6f} {(VList[i] / mean_V_col):.6f}\n")

    per_sin_path = f"../../data/processed/{nome_sem_extensao}_(Per_SinTheta).dat"
    with open(per_sin_path, "w") as f:
        for i in range(len(PerList)):
            f.write(f"{PerList[i]:.6f} {np.sin(ThetaList[i]):.6f}\n")

    col_xy_path = f"../../data/processed/{nome_sem_extensao}_Colisao(X-Y).dat"
    with open(col_xy_path, "w") as f:
        for i in range(1, len(Cx_norm) - 1):
            f.write(f"{Cx_norm[i]:.6f} {Cy_norm[i]:.6f}\n")

    print(f"Arquivos processados gerados com sucesso para: {nome_sem_extensao}")

def main():
    parser = argparse.ArgumentParser(description="Detecção de colisões e pré-processador Lemon Billiard")
    parser.add_argument("--file", type=str, help="Arquivo específico em data/raw/ para processar")
    args = parser.parse_args()

    # Define o diretório de execução relativo ao script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    raw_dir = "../../data/raw"
    if args.file:
        file_path = os.path.join(raw_dir, args.file)
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print(f"Erro: Arquivo {file_path} não encontrado.")
    else:
        # Modo lote: processa todos os arquivos .txt em data/raw
        files = glob.glob(os.path.join(raw_dir, "*.txt"))
        if not files:
            print(f"Nenhum arquivo .txt encontrado em {raw_dir}")
            return
        for f in sorted(files):
            process_file(f)

if __name__ == "__main__":
    main()
