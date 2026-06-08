import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import sys
from scipy.signal import butter, filtfilt
from scipy.optimize import curve_fit
import os
import random

'''
Juntando Todas As Def de ambos os codigos antes de filtrar
'''
Graph=False

def Lowpass(data, cutoff, fs, order):
    """
    Aplica um filtro passa-baixa de Butterworth aos dados de entrada.

    Args:
    - data: Os dados que serão filtrados.
    - cutoff: A frequência de corte do filtro passa-baixa em Hz.
    - fs: A frequência de amostragem dos dados.
    - order: A ordem do filtro Butterworth.

    Returns:
    - y: Os dados filtrados.
    """

    # Normaliza a frequência de corte pelo dobro da frequência de Nyquist
    normal_cutoff = cutoff / fs

    # Obtém os coeficientes do filtro
    b, a = butter(order, normal_cutoff, btype='low', analog=False)

    # Aplica o filtro bidirecionalmente para minimizar a distorção de fase
    y = filtfilt(b, a, data)

    # Retorna os dados filtrados
    return y

def Ang(a, b):
    m = len(a)
    prod = 0
    for i in range(m):
        prod = prod + a[i] * b[i]
    mod = np.linalg.norm(a) * np.linalg.norm(b)
    ang = np.arccos(prod / mod)
    return (ang)

def LemonWall(x, y, r, a): #é construido o contorno do limão
    theta = np.linspace(0,2*np.pi,1000)
    x1 = r*np.cos(theta)
    y1 = r*np.sin(theta) + a
    x2 = r*np.cos(theta)
    y2 = r*np.sin(theta) - a
    return [x1,y1], [x2,y2]

def StraightWalk(t, x, y, v): #Registra a trajetoria o vôo do robô até a proxima colisão, onde a velocidade é maior que 0.1
    """
    Filtra os pontos da trajetória onde a velocidade excede um limiar e retorna os tempos,
    coordenadas x e y correspondentes.

    Parâmetros:
    t : array_like
        Array contendo os tempos.
    x : array_like
        Array contendo as coordenadas x.
    y : array_like
        Array contendo as coordenadas y.
    v : array_like
        Array contendo as velocidades.

    Retorna:
    ts : list
        Lista contendo os tempos filtrados.
    xs : list
        Lista contendo as coordenadas x correspondentes aos tempos filtrados.
    ys : list
        Lista contendo as coordenadas y correspondentes aos tempos filtrados.
    """
    vm = np.mean(V)  # Calcula a velocidade média a partir do vetor de velocidades
    ts = []  # Lista para armazenar os tempos filtrados
    xs = []  # Lista para armazenar as coordenadas x correspondentes aos tempos filtrados
    ys = []  # Lista para armazenar as coordenadas y correspondentes aos tempos filtrados

    # Loop sobre os índices do vetor de coordenadas x
    for i in range(len(x)):
        # Verifica se a velocidade no ponto atual excede o limiar (0.1 m/s)
        if v[i] > 0.1:  # Observação: o comentário indica que o correto é v[i] < vm, mas o código usa v[i] > 0.1
            # Se a condição for satisfeita, o ponto é considerado válido e adicionado às listas
            xs.append(x[i])  # Adiciona a coordenada x correspondente ao tempo i
            ys.append(y[i])  # Adiciona a coordenada y correspondente ao tempo i
            ts.append(t[i])  # Adiciona o tempo i à lista de tempos

    # Retorna as listas contendo os tempos e as coordenadas filtradas
    return ts, xs, ys

def Fits(ts, xs, ys):
    tdiff = np.diff(ts)
    cont0 = 0
    r2 = []
    b = []
    for i in range(len(ts)-1):
        if tdiff[i] > 5/30:
            vec = [xs[cont0:i],ys[cont0:i]]
            reg = linregress(vec[0], vec[1])
            r = reg.rvalue**2
            if r<0.2:
            #     print(ts[i])
            #     plt.plot(xs[cont0:i],ys[cont0:i])
            #     plt.xlim([-1.1,1.1])
            #     plt.ylim([-1.1,1.1])
            #     ####plt.show()
                continue
            r2.append(r)
            b.append(abs(reg.slope))
            cont0 = i
    return r2, b

def EffA(ts, xs, ys, l1, l2):
    """
    Calcula o ângulo de incidência, ângulo de reflexão, eficiência da reflexão
    e comprimento dos voos livres.

    Parâmetros:
    ts : array_like
        Array contendo os tempos.
    xs : array_like
        Array contendo as coordenadas x.
    ys : array_like
        Array contendo as coordenadas y.
    l1 : array_like
        Array contendo as coordenadas do primeiro ponto.
    l2 : array_like
        Array contendo as coordenadas do segundo ponto.

    Retorna:
    angin : ndarray
        Array contendo os ângulos de incidência.
    angout : ndarray
        Array contendo os ângulos de reflexão.
    angdiff : ndarray
        Array contendo a eficiência da reflexão.
    fly : ndarray
        Array contendo o comprimento dos voos livres.
    """
    global a  # Variável global (não definida no código fornecido)
    tdiff = np.diff(ts)  # Calcula as diferenças de tempo entre os pontos
    cont0 = 0  # Inicializa um contador
    angin = []  # Lista para armazenar os ângulos de incidência
    angout = []  # Lista para armazenar os ângulos de reflexão
    angdiff = []  # Lista para armazenar a eficiência da reflexão
    fly = []  # Lista para armazenar o comprimento dos voos livres
    b = []  # Lista (não utilizada no código fornecido)
    # Loop sobre os índices dos tempos (exceto o último)
    for i in range(len(ts)-1):
        x0, y0 = xs[cont0], ys[cont0]  # Coordenadas do ponto inicial
        if tdiff[i] > 5/30:  # Verifica se a diferença de tempo é maior que 5/30
            x1, y1 = xs[i], ys[i]  # Coordenadas do ponto atual
            refp = [x1, y1]  # Ponto de reflexão
            vec = [x1 - x0, y1 - y0]  # Vetor da trajetória incidente
            vec2 = [x0 - x1, y0 - y1]  # Vetor da trajetória refletida (reflexão anterior)

            # Verifica se o ponto de reflexão está acima do eixo x
            if y1 >= 0:
                a = -a  # Altera o sinal de 'a' (variável global)
                # Calcula a menor distância para o ponto l2 (provavelmente uma fruta)
                diff1 = list(np.sqrt((l2[0] - x1)**2 + (l2[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l2[0][aa], l2[1][aa]]  # Coordenadas do ponto de l2 mais próximo
                dist = np.sqrt((lvec[0] - refp[0])**2 + (lvec[1] - refp[1])**2)  # Distância entre lvec e refp

                # Verifica se o ponto anterior está acima do eixo x
                if y0 >= 0:
                    # Calcula a distância para o ponto l1 ou l2 (dependendo do ponto anterior)
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]

                # Verifica se a distância é maior que 0.3 ou Graph é verdadeiro (variável não definida)
                if dist > 0.3 or Graph:
                    # Plotagem dos pontos
                    plt.plot(xs[cont0:i], ys[cont0:i], color='black')
                    plt.plot(L1[0], L1[1])
                    plt.plot(L2[0], L2[1])
                    plt.scatter(x1, y1, color='red', s=10)

            # Verifica se o ponto de reflexão está abaixo do eixo x
            if y1 < 0:
                # Calcula a menor distância para o ponto l1
                diff1 = list(np.sqrt((l1[0] - x1)**2 + (l1[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l1[0][aa], l1[1][aa]]  # Coordenadas do ponto de l1 mais próximo
                dist = np.sqrt((lvec[0] - refp[0])**2 + (lvec[1] - refp[1])**2)  # Distância entre lvec e refp

                # Verifica se o ponto anterior está abaixo do eixo x
                if y0 < 0:
                    # Calcula a distância para o ponto l1 ou l2 (dependendo do ponto anterior)
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]

                # Verifica se a distância é maior que 0.3 ou Graph é verdadeiro (variável não definida)
                if dist > 0.3 or Graph:
                    # Plotagem dos pontos
                    plt.plot(xs[cont0:i], ys[cont0:i], color='black')
                    plt.plot(L1[0], L1[1])
                    plt.plot(L2[0], L2[1])
                    plt.scatter(x1, y1, color='red', s=10)

            # Calcula os ângulos de incidência e reflexão
            inc = Ang(lvec, vec)
            ref = Ang(lvec2, vec2)

            # Calcula a eficiência da reflexão
            if inc > ref:
                dif = ref / inc
            else:
                dif = inc / ref

            # Armazena os resultados
            angin.append(inc)
            angout.append(ref)
            angdiff.append(dif)
            fly.append(np.linalg.norm(vec))
            cont0 = i + 1  # Atualiza o contador

    # Retorna os resultados como arrays numpy
    return np.array(angin), np.array(angout), np.array(angdiff), np.array(fly)

def Col(ts, xs, ys):
    global a  # Variável global
    tdiff = np.diff(ts)
    cont0 = 0  # Inicializa um contador
    Fl = 0
    refp=[]
    T   =[]
    for i in range(len(ts)-1):
        x0, y0 = xs[cont0], ys[cont0]
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            refp.append([x1, y1])
            T.append(Fl)
            Fl = 0
        Fl = Fl+dt


    return np.array(refp).T , np.array(T).T

def Soma(v1, v2):
    m = len(v1)
    m = m - 1
    u = [0 for i in range(m)]
    while m >= 0:
        u[m] = v1[m] + v2[m]
        # print(u[m])
        m = m - 1
    return u

def Sub(v1, v2):
    m = len(v1)
    # print(m)
    # m = m - 1
    u = [0 for i in range(m)]
    for i in range(m):
        # print(i)
        # print(v1[0])
        u[i]= v1[i] - v2[i]
    # while m >= 0:
    #     print(u)
        # u[m] = v1[m] - v2[m]
        # print(u[m])
        # m = m - 1
    return u

def Modulo(v):
    global soma
    m = len(v)
    soma = 0
    for i in range(m):
        soma = soma + v[i] ** 2
    mod = np.sqrt(soma)
    return mod

def Interno(v1, v2):
    m = len(v1)
    int = 0
    for i in range(m):
        int = int + v1[i] * v2[i]
    return int

def Escalar(k, v1):
    m1 = len(v1)
    u = [0 for i in range(m1)]
    for i in range(m1):
        u[i] = k * v1[i]
    return u

def Proj(v1, v2):
    m = len(v1)
    u = []
    int = Interno(v1, v2)
    mod = Modulo(v1)
    div = (int / mod ** 2)
    m = m - 1
    while m >= 0:
        w = div * v1[m]
        u.insert(0, w)
        # print(w)
        m = m - 1
    return u

def Nnan(x):
    n=1#len(x)
    m=len(x)
    inf = 0
    sup = 0
    step = 0.0
    # for h in range(n): #n individuos
    for i in range(0, m): # m pontos

        if x[i] == 0.0: #and i != 0:
            inf = i
            for j in range(inf + 1, m):
                if x[j] != 0.0:
                    sup = j
                    if inf == 0:
                        step = [sup]
                    else:
                        step = (x[sup] - x[inf-1]) / ((sup - inf) + 1)
                    break
                if j == m-1:
                    sup = m
                    step = 0.0
        for k in range(inf, sup):
            if inf == 0:
                x[k] = step
                continue
            else:
                x[k] = x[k-1] + step
    return x

def Radius(Pmean,Point):
    R = Sub(Point,Pmean)
    return R

# Define a equação de um círculo
def equacao_circulo(x, h, k, r):
    return (x[0] - h) ** 2 + (x[1] - k) ** 2 - r ** 2

# Encontra os parâmetros do círculo
def encontrar_parametros_circulo(pontos_x, pontos_y):
    x_dados = np.array(pontos_x)
    y_dados = np.array(pontos_y)

    estimativa_inicial = (0, 0, 1)  # Estimativa inicial para os parâmetros (centro e raio)

    # Realiza o ajuste da curva usando a função curve_fit
    parametros_otimos, covariancia = curve_fit(equacao_circulo, (x_dados, y_dados), np.zeros(len(pontos_x)), p0=estimativa_inicial)

    # Extrai os valores dos parâmetros estimados
    h, k, r = parametros_otimos

    # Calcula os erros dos parâmetros
    erros = np.sqrt(np.diag(covariancia))

    h_erro, k_erro, r_erro = erros[0], erros[1], erros[2]

    return (h, k), r, (h_erro, k_erro), r_erro

#Inserindo os dados
GammaList=[]
lista_LE =[]
Lista_LEG=[]
arquivos = [arq for arq in os.listdir('DadosCrus') if arq.endswith('.txt')]
# Solicit user input for file name and width of the plot
print(arquivos)
for Nome in arquivos:
    # Extrair o nome do arquivo sem a extensão
    Nome_sem_extensao = os.path.splitext(Nome)[0]
    Nome = Nome_sem_extensao

    X, Y, ex, ey = np.loadtxt('DadosCrus/'+str(Nome)+'.txt', unpack=True)

    '''
    O objetivo aqui é normalizar os dados
    Primeira etapa será centralizar
    '''
    Norm = (np.max(Y)- np.min(Y))*0.5# Multiplicado por 0.5 para que o valor maximo de Y seja de [-1,1]
    X = (X-np.mean(X))/Norm
    Y = (Y-np.mean(Y))/Norm

    #Caso de curiosidade segue os dados:
    '''
    plt.plot(X,Y)
    plt.show()
    sys.exit()
    '''
    #Para encontrar os pontos de colisões precido da velocidade

    import numpy as np

    # Determina o número de elementos em X
    N = len(X)

    # Cria uma lista de tempo, supondo uma frequência de amostragem de 30 Hz
    t = np.linspace(0, (N-1)/30, N)

    # Calcula o intervalo de tempo entre as amostras
    dt = t[1] - t[0]

    # Calcula as componentes da velocidade Vx e Vy usando a derivada numérica
    Vx = np.gradient(X, dt)
    Vy = np.gradient(Y, dt)

    # Calcula a magnitude da velocidade V
    V = np.sqrt(Vx**2 + Vy**2)
    # Calcula a média e o desvio padrão da magnitude da velocidade
    Vm = np.mean(V)
    Vstd = np.std(V)

    # Calcula as componentes da aceleração Ax e Ay usando a segunda derivada numérica
    Ax = np.gradient(Vx, dt)
    Ay = np.gradient(Vy, dt)

    # Calcula a magnitude da aceleração A
    A = np.sqrt(Vx**2 + Vy**2)


    '''
    plt.plot(t,A,'o')
    plt.show()
    sys.exit()
    '''
    # Calcula as frequências da transformada discreta de Fourier (DFT) correspondentes ao domínio da frequência

    # onde N é a quantidade de dados e dt é o intervalo de tempo entre as amostras
    freq = np.fft.fftfreq(N, dt)

    # Cria uma máscara booleana para selecionar apenas as frequências positivas
    modulo = freq > 0

    # Calcula a transformada de Fourier dos dados de velocidade V
    fft = np.fft.fft(V)

    # Calcula o espectro de frequência normalizado para os dados de velocidade V
    Vmod = 2.0 * np.abs(fft / N)

    # Seleciona apenas as frequências positivas e correspondentes ao espectro de frequência de V
    fourier = freq[modulo]
    Vmod = Vmod[modulo]

    # Calcula a magnitude das frequências positivas
    F = np.sqrt((fourier) ** 2)

    # Converte Vmod para uma lista
    Vmod = list(Vmod)

    # Encontra a amplitude máxima do espectro de frequência e a frequência principal do sinal
    Am = np.max(Vmod)
    print(Nome)
    Fm = F[Vmod.index(np.max(Vmod))]  # frequência principal do sinal

    # Requisitos do filtro.
    # Determina a frequência de amostragem máxima e a frequência de corte desejada para o filtro passa-baixa
    fs = max(F)
    cutoff = fs / 10  # frequência de corte desejada do filtro, Hz
    order = 3

    # Aplica um filtro passa-baixa aos dados de velocidade V
    Vn = Lowpass(V, cutoff, fs, order)

    # Calcula a transformada de Fourier dos dados de aceleração A
    fft = np.fft.fft(A)

    # Calcula o espectro de frequência normalizado para os dados de aceleração A
    Amod = 2.0 * np.abs(fft / N)

    # Seleciona apenas as frequências positivas e correspondentes ao espectro de frequência de A
    Amod = Amod[modulo]

    # Calcula a magnitude das frequências positivas
    F = np.sqrt((fourier) ** 2)

    # Converte Amod para uma lista
    Amod = list(Amod)

    # Requisitos do filtro.
    # Determina a frequência de amostragem máxima e a frequência de corte desejada para o filtro passa-baixa
    fs = max(F)
    cutoff = fs / 10  # frequência de corte desejada do filtro, Hz
    order = 3

    # Aplica um filtro passa-baixa aos dados de aceleração A

    An = Lowpass(A, cutoff, fs, order)

    '''
    plt.plot(t,Vn)
    plt.show()
    sys.exit()
    '''
    #Usarei StraightWalk para encontrar os pontos de colisões
    ts, Xs, Ys = StraightWalk(t, X, Y, Vn)
    Coli, TList=Col(ts, Xs, Ys)
    #print(TList)
    #print(len(TList))
    #sys.exit()

    '''

    print(Coli[0])
    plt.plot(Coli[0],Coli[1],'o')
    plt.show()
    sys.exit()

    '''
    #Pronto, até aqui eu tenho todas as colisçoes
    Cx = Coli[0]
    Cy = Coli[1]
    Cym= np.mean(Cy)
    Altura_Y = np.max(Cy)+np.abs(np.min(Cy))

    print(Cym)
    #sys.exit()
    #Partindo para identificação dos circulos
    conjunto_sup_cs = []  # Valores de Y acima da média
    conjunto_sup_xs = []  # Valores de X correspondentes
    conjunto_inf_ci = []  # Valores de Y abaixo da média
    conjunto_inf_xi = []  # Valores de X correspondentes
    # Calcula os valores de alfa e gamma
    for i in range(len(Coli[1])):
        if Coli[1][i] > Cym:
            conjunto_sup_xs.append(Coli[0][i])
            conjunto_sup_cs.append(Coli[1][i])
        else:
            conjunto_inf_xi.append(Coli[0][i])
            conjunto_inf_ci.append(Coli[1][i])

    pontos_x_sup = conjunto_sup_cs
    pontos_y_sup = conjunto_sup_xs

    pontos_x_inf = conjunto_inf_ci
    pontos_y_inf = conjunto_inf_xi

    #Encontra os parâmetros do círculo para os conjuntos acima e abaixo da média
    centro_sup, raio_sup, erro_centro_sup, erro_raio_sup = encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
    centro_inf, raio_inf, erro_centro_inf, erro_raio_inf = encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)

    # Calcula a diferença entre as coordenadas dos centros dos círculos
    centro_AB = (centro_inf[0] - centro_sup[0], centro_inf[1] - centro_sup[1])

    # Calcula o módulo (norma) da diferença entre os centros
    modulo_AB = np.linalg.norm(centro_AB)

    gamma = 1 - Altura_Y/(raio_sup+raio_inf)
    alfa = gamma*(raio_sup+raio_inf)/2
    #gamma=abs(gamma)
    #por facilidade
    a=gamma
    # Calcula o ângulo entre a reta centro_sup - centro_inf e o eixo Y
    angulo_radianos = np.arctan2(centro_AB[1], centro_AB[0])

    # Converte o ângulo de radianos para graus
    angulo_graus = np.degrees(angulo_radianos)-90

    # Calcula os valores de alfa e gamma
    L0 =2*np.pi
    H = L0*(1-gamma)/(2*np.arcsin(np.sqrt(1-gamma**2)))
    N_y=H/Altura_Y #H/Altura_Y #Fator de normalização
    N = len(Cx)
    Norm = (np.max(Cy)- np.min(Cy))/H# 260
    Cx = (Cx-np.mean(Cx))*N_y
    Cy = (Cy-np.mean(Cy))*N_y
    Coli[0]=Cx
    Coli[1]=Cy
    print("norma: "+str(Norm))
    print("Gamma: "+str(gamma))
    print("Altura teorica: "+str(H))
    print("Altura: "+str(np.max(Cy)+np.abs(np.min(Cy))))
    print("largura: "+str(np.max(Cx)+np.abs(np.min(Cx))))


    L1, L2 = LemonWall(X, Y, (raio_sup+raio_inf)/2, a)
    #print(f'{ts} {Xs} {Ys} {L1} {L2}')
    Inc, Ref, AngEff, FF = EffA(ts, Xs, Ys, L1, L2)
    EffAng = (Ref) # Difference between incidence and reflection angle
    AngDev = np.mean(np.rad2deg(EffAng))
    AngDevStd = np.std(np.rad2deg(EffAng))

    VList=(FF/TList)
    #print(len(VList))

    #Aparti daqui mantem o anterior

    Comp = []
    Kappa = []
    V = []
    ThetaList = []
    AlphaList = []
    PerList = []
    AngEff = [0. for i in range(len(Coli[0]))]
    Nsteps = len(Coli[0])
    for i in range(1, Nsteps-1):

        TList[i] = TList[i] # MARCADORRRRRRRRRRRRRRRRRRRRRRRRRRRR

        if (Coli[1][i] >= 0.0):
            c1 = [Coli[0][i + 1], Coli[1][i + 1]]
            c2 = [Coli[0][i], Coli[1][i]]
            c3 = [Coli[0][i - 1], Coli[1][i - 1]]
            R = Sub(c2,[0.0, -a])
            x_d = np.sqrt(np.linalg.norm(R)*np.linalg.norm(R) - a*a)
            Per =3*np.arcsin(x_d/np.linalg.norm(R)) - np.arcsin(Coli[0][i]/np.linalg.norm(R))
            Per= Per*np.linalg.norm(R)

            vec = Sub(c2, c3)  # antes da reflec
            vecRef = Sub(c2, c1)  # dps da reflexão
            Reflec = Ang(vec, R) #reflexao

            if (c2[0]*vecRef[1]-c2[1]*vecRef[0]) <0:
                Reflec=-Reflec

            Alf = Ang(vecRef, R) #incidencia
            AngEff[i] = 1 - np.abs(Reflec-Alf)
            Comp.append(np.linalg.norm(vec))
            #########Kappa normalizado
            Kappa.append(1 / np.linalg.norm(R))#Radius([pxmean + a, pymean], c2)))
            ########### Velocidade normalizada
            Velo = np.linalg.norm(vec) / TList[i]
            V.append(Velo)
            ThetaList.append(np.sin(Reflec))
            AlphaList.append(Alf)
            PerList.append(Per)

        if (Coli[1][i] <= 0.0):
            c1 = [Coli[0][i + 1], Coli[1][i + 1]]
            c2 = [Coli[0][i], Coli[1][i]]
            c3 = [Coli[0][i - 1], Coli[1][i - 1]]
            R = Sub(c2,[0.0, a])
            x_d = np.sqrt(np.linalg.norm(R)*np.linalg.norm(R) - a*a)
            Per =np.arcsin(Coli[0][i]/np.linalg.norm(R)) + np.arcsin(x_d/np.linalg.norm(R))
            Per=Per*np.linalg.norm(R)
            vec = Sub(c2, c3)  # antes da reflec
            vecRef = Sub(c2, c1)  # dps da reflexão

            Reflec = Ang(vec, R) #reflexao

            if (c2[0]*vecRef[1]-c2[1]*vecRef[0]) <0:
                Reflec=-Reflec

            Alf = Ang(vecRef, R)
            AngEff[i] = 1 - np.abs(Reflec-Alf)
            Comp.append(np.linalg.norm(vec))
            ##########Kappa normalizado
            Kappa.append(1 / np.linalg.norm(R)) #Radius([pxmean - a, pymean], c2)))
            ########### Velocidade normalizada
            Velo = np.linalg.norm(vec) / TList[i]
            V.append(Velo)
            ThetaList.append(np.sin(Reflec))
            AlphaList.append(Alf)
            PerList.append(Per)

    print("PerList: "+str(len(PerList)))
    print("EffAng: "+str(len(EffAng)))

    ###############################################################################


    # Ensure 'Nome' is defined appropriately before this code segment

    # Create and open a file for writing data
    data = open('DadosTratados/' + Nome + '_(T_Th_Ka_V).dat', 'w+')

    # Print the mean of V for reference
    print("Media da velocidade V:", np.mean(V))

    # Iterate over the data and write to the file
    for i in range(len(Kappa)):
        # Calculate and write transformed data to the file
        data.write('%f %f %f %f\n' % (float(TList[i]*np.mean(V)), float(ThetaList[i]), float(Kappa[i]), float(VList[i]/np.mean(V))))

    # Close the file after writing
    data.close()

    # Create and open another file for writing data
    data = open('DadosTratados/' + Nome + '_(Per_SinTheta).dat', 'w+')

    # Print the mean of V for reference
    print("Mean of V:", np.mean(V))

    # Iterate over the data and write to the file
    for i in range(len(PerList)):
        # Write transformed data to the file
        data.write('%f %f\n' % (float(PerList[i]), float((np.sin(ThetaList[i]) ))))  # Change Theta to sin(Theta)

    # Close the file after writing
    data.close()

    # Create and open a file for writing collision data
    data1 = open('DadosTratados/' + str(Nome) + '_Colisao(X-Y).dat', 'w+')

    # Iterate over collision data and write to the file
    for i in range(len(Coli[0])):
        data1.write('%f %f\n' % (float(Coli[0][i]), float(Coli[1][i])))

    # Close the file after writing
    data1.close()
    GammaList.append((Nome_sem_extensao, gamma))
    ###
    Nome_sem_extensao = os.path.splitext(Nome)[0]

    # Cálculo do expoente de Lyapunov
    delta = [random.uniform(0, 1), random.uniform(0, 1)]
    delta /= np.linalg.norm(delta)
    label = 5

    # Carregar os dados do arquivo de entrada
    t_list, theta_list, kappa, vel = np.loadtxt('DadosTratados/' + Nome_sem_extensao + '_(T_Th_Ka_V).dat', unpack=True)
    n_steps = len(t_list)

    # Abrir arquivo de saída para escrita
    with open('Lyapunov/' + Nome_sem_extensao + '.dat', 'w') as fout:
        lambda_ = 0.0
        for ii in range(n_steps):
            u = delta[0]
            delta[0] = u + t_list[ii] * delta[1]
            delta[1] = delta[1]

            u = delta[0]
            delta[0] = -u
            delta[1] = vel[ii] * 2. * kappa[ii] / np.cos(theta_list[ii]) * u - delta[1]

            lambda_ += np.log(np.linalg.norm(delta))
            fout.write("%f %f\n" % (sum(t_list[:(ii + 1)]), lambda_ / sum(t_list[:(ii + 1)])))
            delta /= np.linalg.norm(delta)

    LE = lambda_ / sum(t_list[:n_steps])


    lista_LE.append((Nome_sem_extensao, LE))
    Lista_LEG.append((Nome_sem_extensao, gamma, LE))

    #####################
    FS=12

    nome_arquivo = Nome_sem_extensao
    # Load data from the specified file
    caminho_arquivo = 'DadosCrus/' + str(nome_arquivo) + '.txt'
    X, Y, ex, ey = np.loadtxt(caminho_arquivo, unpack=True)

    # Calculate the midpoint of X and Y and center the data
    ponto_medio_X = np.mean(X)
    ponto_medio_Y = np.mean(Y)
    X = X - np.mean(X)
    Y = Y - np.mean(Y)
    # Normalize the data
    max_X = np.max(X)
    min_X = np.min(X)
    Norm = max_X + abs(min_X)
    X = (X / Norm) * 2
    Y = (Y / Norm) * 2

    # Load collision data
    caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
    X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)

    # Load Poincaré map data
    caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
    X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
    X_P = X_P * 2 * np.pi / np.max(X_P)

    # Plot
    plt.figure(figsize=(10, 10))
    plt.suptitle(f'{nome_arquivo} | Gamma = {gamma:.5f} | Expoente Lyapunov = {LE:.5f} | Coli = {len(EffAng)}')
    # Plot 1: Trajectory
    plt.subplot(2, 2, 1)
    plt.plot(X, Y, color='#ff972f', linestyle='solid', drawstyle='default', linewidth=1)
    plt.xlabel('X',fontsize=FS)
    plt.ylabel('Y',fontsize=FS)
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 2: Collision data
    plt.subplot(2, 2, 2)
    plt.plot(X_C, Y_C, color='#ff972f', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X',fontsize=FS)
    plt.ylabel('Y',fontsize=FS)
    plt.axis('square')
    plt.ylim(-1.51, 1.51)
    plt.xlim(-1.51, 1.51)
    plt.grid(True)

    # Plot 3: Poincaré map data
    plt.subplot(2, 2, 3)
    plt.plot(X_P, Y_P, color='#ff972f', linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')


    pi_value = np.pi

    x_ticks_positions = [0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value]
    x_ticks_labels = ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$']
    plt.xticks(x_ticks_positions, x_ticks_labels)
    plt.xlabel(r'$\rho$', fontsize=FS)
    plt.ylabel(r'sin $\phi$', fontsize=FS)
    plt.yticks([-1,-0.5, 0,0.5, 1])
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)
    #plt.tight_layout()

    x, y = np.loadtxt('Lyapunov/' + Nome_sem_extensao + '.dat', unpack=True)


    plt.subplot(2, 2, 4)
    plt.axhline(LE, color='black', linestyle='solid', linewidth=1, alpha=1, label=f'LE ({LE:.5f})')
    plt.plot(x, y, color='#ff972f')
    plt.minorticks_on()
    #plt.legend(loc='lower right')
    plt.yticks([-0.5,-0.25, 0,0.25,0.5])
    plt.ylim(-0.55, 0.55)

    plt.ylabel(r'$\gamma$',fontsize=FS)
    plt.xlabel('t',fontsize=FS)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
    plt.grid(True)

    plt.savefig('Gráficos/' + str(nome_arquivo) + '.png', dpi=350)

    #plt.show()

# Abrir arquivo de texto para escrita
with open('Lyapunov/N_G_LE_valores.txt', 'w') as arquivo_txt:
    arquivo_txt.write('Nome do Exp | Gamma | Expoent Lyapunov\n')
    for item in Lista_LEG:
        arquivo_txt.write(f'{item[0]} {item[1]} {item[2]}\n')

