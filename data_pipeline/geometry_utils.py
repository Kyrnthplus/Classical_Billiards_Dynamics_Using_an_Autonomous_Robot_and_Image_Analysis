import numpy as np
from scipy.optimize import curve_fit

def funcao_primeiro_grau(x1, y1, x2, y2):
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return lambda x: m * x + c

def produto_vetorial(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Os vetores devem ter duas componentes (x, y)")
    return v1[0] * v2[1] - v1[1] * v2[0]

def calcular_modulo(vetor):
    return np.linalg.norm(vetor)

def calcular_versor(vetor):
    modulo = np.linalg.norm(vetor)
    if modulo == 0:
        return np.array([0, 0])
    return vetor / modulo

def calcular_angulo(Vdir, Pdir):
    dot_product = np.dot(Vdir, Pdir)
    norm_Vdir = np.linalg.norm(Vdir)
    norm_Pdir = np.linalg.norm(Pdir)
    if norm_Vdir == 0 or norm_Pdir == 0:
        return 0, 0
    cos_theta = dot_product / (norm_Vdir * norm_Pdir)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_radians = np.arccos(cos_theta)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees, angle_radians

def Ang(a, b):
    m = len(a)
    prod = 0
    for i in range(m):
        prod = prod + a[i] * b[i]
    mod = np.linalg.norm(a) * np.linalg.norm(b)
    if mod == 0:
        return 0.0
    val = prod / mod
    val = np.clip(val, -1.0, 1.0)
    return np.arccos(val)

def LemonWall(x, y, r, a):
    theta = np.linspace(0, 2*np.pi, 1000)
    x1 = r*np.cos(theta)
    y1 = r*np.sin(theta) + a
    x2 = r*np.cos(theta)
    y2 = r*np.sin(theta) - a
    return [x1, y1], [x2, y2]

def Soma(v1, v2):
    m = len(v1)
    u = [v1[i] + v2[i] for i in range(m)]
    return u

def Sub(v1, v2):
    m = len(v1)
    u = [v1[i] - v2[i] for i in range(m)]
    return u

def Modulo(v):
    return np.linalg.norm(v)

def Interno(v1, v2):
    return np.dot(v1, v2)

def Escalar(k, v1):
    return [k * x for x in v1]

def Proj(v1, v2):
    m = len(v1)
    u = []
    val_interno = Interno(v1, v2)
    val_modulo = Modulo(v1)
    if val_modulo == 0:
        return [0.0] * m
    div = (val_interno / val_modulo ** 2)
    m = m - 1
    while m >= 0:
        w = div * v1[m]
        u.insert(0, w)
        m = m - 1
    return u

def equacao_circulo(x, h, k, r):
    return (x[0] - h) ** 2 + (x[1] - k) ** 2 - r ** 2

def encontrar_parametros_circulo(pontos_x, pontos_y):
    x_dados = np.array(pontos_x)
    y_dados = np.array(pontos_y)
    estimativa_inicial = (0, 0, 1)
    parametros_otimos, covariancia = curve_fit(
        equacao_circulo, 
        (x_dados, y_dados), 
        np.zeros(len(pontos_x)), 
        p0=estimativa_inicial,
        maxfev=10000
    )
    h, k, r = parametros_otimos
    erros = np.sqrt(np.diag(covariancia))
    h_erro, k_erro, r_erro = erros[0], erros[1], erros[2]
    return (h, k), r, (h_erro, k_erro), r_erro

def EffA(ts, xs, ys, l1, l2, initial_a):
    a = initial_a
    tdiff = np.diff(ts)
    cont0 = 0
    angin = []
    angout = []
    angdiff = []
    fly = []
    for i in range(len(ts)-1):
        x0, y0 = xs[cont0], ys[cont0]
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            refp = [x1, y1]
            vec = [x1 - x0, y1 - y0]
            vec2 = [x0 - x1, y0 - y1]

            if y1 >= 0:
                a = -a
                diff1 = list(np.sqrt((l2[0] - x1)**2 + (l2[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l2[0][aa], l2[1][aa]]

                if y0 >= 0:
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
            if y1 < 0:
                diff1 = list(np.sqrt((l1[0] - x1)**2 + (l1[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l1[0][aa], l1[1][aa]]

                if y0 < 0:
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]

            inc = Ang(lvec, vec)
            ref = Ang(lvec2, vec2)

            if inc > ref:
                dif = ref / inc
            else:
                dif = inc / ref

            angin.append(inc)
            angout.append(ref)
            angdiff.append(dif)
            fly.append(np.linalg.norm(vec))
            cont0 = i + 1

    return np.array(angin), np.array(angout), np.array(angdiff), np.array(fly)
