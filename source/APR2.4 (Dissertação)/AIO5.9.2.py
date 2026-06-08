import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
import sys
from scipy.signal import butter, filtfilt
from scipy.optimize import curve_fit
import os
import random

def funcao_primeiro_grau(x1, y1, x2, y2):
    # Calcula o coeficiente angular
    m = (y2 - y1) / (x2 - x1)

    # Calcula o coeficiente linear (intercepto y)
    c = y1 - m * x1

    # Define a função de primeiro grau
    def linear_function(x):
        return m * x + c

    return linear_function
def produto_vetorial(v1, v2):
    # Verifica se ambos os vetores têm duas componentes
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Os vetores devem ter duas componentes (x, y)")

    # Calcula o componente z do vetor resultante
    z = v1[0] * v2[1] - v1[1] * v2[0]

    return z
def calcular_modulo(vetor):
    # Use a função norm do numpy para calcular o módulo
    modulo = np.linalg.norm(vetor)
    return modulo
def calcular_versor(vetor):
    # Calcule o módulo do vetor
    modulo = np.linalg.norm(vetor)

    # Evite divisão por zero
    if modulo == 0:
        return np.array([0, 0])  # Se o módulo for zero, retornar vetor nulo

    # Calcule o versor dividindo o vetor pelo seu módulo
    versor = vetor / modulo

    return versor
def calcular_angulo(Vdir, Pdir):
    # Calcule o produto escalar
    dot_product = np.dot(Vdir, Pdir)

    # Calcule as normas dos vetores
    norm_Vdir = np.linalg.norm(Vdir)
    norm_Pdir = np.linalg.norm(Pdir)

    # Evite divisão por zero
    if norm_Vdir == 0 or norm_Pdir == 0:
        return 0, 0

    # Calcule o cosseno do ângulo entre os vetores
    cos_theta = dot_product / (norm_Vdir * norm_Pdir)

    # Certifique-se de que o cosseno está dentro do intervalo [-1, 1]
    #cos_theta = np.clip(cos_theta, -1, 1)

    # Calcule o ângulo em radianos
    angle_radians = np.arccos(cos_theta)

    # Converta o ângulo para graus
    angle_degrees = np.degrees(angle_radians)

    return angle_degrees, angle_radians
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
    refp=[[],[]]
    T   =[]
    for i in range(len(ts)-1):
        x0, y0 = xs[cont0], ys[cont0]
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            refp[0].append(x1)  # Adicionando x1 à primeira sublista
            refp[1].append(y1)  # Adicionando y1 à segunda sublista
            T.append(Fl)
            Fl = 0
        Fl = Fl+dt


    return refp[0],refp[1] ,np.array(T).T #np.array(refp).T , np.array(T).T

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

Simu=int(input('Simular? 1(Sim) 0(Não): '))
delet=int(input('Deletar simulações ruins?? 1(Sim) 0(Não): '))

#Inserindo os dados
GammaList=[]
lista_LE =[]
Lista_LEG=[]
# Listar arquivos na pasta DadosCrus com extensão .txt e ordená-los
arquivos_dadoscrus = sorted([arq.split('.')[0] for arq in os.listdir('DadosCrus') if arq.endswith('.txt')])
# Listar arquivos na pasta Gráficos e ordená-los
arquivos_grafico = sorted([arq.split('.')[0] for arq in os.listdir('Gráficos') if arq.endswith('.png')])
# Verificar arquivos que ainda não foram processados e ordená-los
arquivos_para_processar = sorted([arq for arq in arquivos_dadoscrus if arq not in arquivos_grafico])

# Solicit user input for file name and width of the plot
print("Arquivos encontrados para processamento:", arquivos_dadoscrus)
print("############################################################")
print("Arquivos que podem ser processados:", arquivos_para_processar)
print("############################################################")
opcao = str(input("Todos os arquivos (digite 'todos') ou os que não forão processados (digite 'novos')?, caso um aarquivo especifico digite o nome: "))

if opcao == 'todos':
    arquivos = arquivos_dadoscrus
elif opcao == 'novos':
    arquivos = arquivos_para_processar
else:
    arquivos = opcao
for Nome0 in arquivos:
    try:
        # Extrair o nome do arquivo sem a extensão
        Nome_sem_extensao = os.path.splitext(Nome0)[0]
        Nome = Nome_sem_extensao
        #linhas = Nome0.readlines()
        # Verifica se o arquivo tem exatamente 1.000.000 de linhas


        X, Y, ex, ey = np.loadtxt('DadosCrus/'+str(Nome)+'.txt', unpack=True)
        if len(X) % 1000 == 0 and delet ==1:
            # Apaga o arquivo se tiver 1.000.000 de linhas
            os.remove(os.path.join('DadosCrus/'+str(Nome)+'.txt'))
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            printf("O arquivo {Nome} foi excluído pois possui {len(X)} de linhas.")
            print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            continue  # Passa para o próximo arquivo
        print("############################################################")
        print(f'Nome do arquivo: {Nome}')
        '''
        O objetivo aqui é normalizar os dados
        Primeira etapa será centralizar
        '''
        '''
        Norm = (np.max(Y)- np.min(Y))*0.5# Multiplicado por 0.5 para que o valor maximo de Y seja de [-1,1]
        X = (X-np.mean(X))/Norm
        Y = (Y-np.mean(Y))/Norm
        '''
        #Caso de curiosidade segue os dados:
        #'''
        #plt.plot(X,Y)
        #plt.show()
        #sys.exit()
        #'''
        #Rotacionando os dados

        #print(Ang_Expr)
        if not Nome.endswith('T_S'):
            Menor_X = np.min(X)
            X_i = np.where(X == Menor_X)[0][0]  # Encontra o índice do menor valor em X

            Maior_X = np.max(X)
            X_I = np.where(X == Maior_X)[0][0]  # Encontra o índice do maior valor em X


            Vx_Exp = [X[X_I]-X[X_i],Y[X_I]-Y[X_i]]
            #print(Vx_Exp)
            Vi = [1,0]
            Ang_Expg,Ang_Expr = calcular_angulo(Vx_Exp,Vi)
            print(f'angulo em graus:{Ang_Expg}')
            TamX=len(X)
            if Ang_Expg<5:
                if Vx_Exp[1]<0:
                    for i in range(TamX-1):
                        X[i]=+X[i]*np.cos(Ang_Expr)-Y[i]*np.sin(Ang_Expr)
                        Y[i]=+X[i]*np.sin(Ang_Expr)+Y[i]*np.cos(Ang_Expr)

                else:
                    for i in range(TamX-1):
                        X[i]=+X[i]*np.cos(Ang_Expr)+Y[i]*np.sin(Ang_Expr)
                        Y[i]=-X[i]*np.sin(Ang_Expr)+Y[i]*np.cos(Ang_Expr)
                    #Caso de curiosidade segue os dados:
            #'''
            Norm = (np.max(Y)- np.min(Y))*0.5# Multiplicado por 0.5 para que o valor maximo de Y seja de [-1,1]
            X = (X-np.mean(X))/Norm
            Y = (Y-np.mean(Y))/Norm

        #plt.plot(X,Y)
        #plt.show()
        #sys.exit()
        #'''
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
        ##sys.exit()
        '''
        #Usarei StraightWalk para encontrar os pontos de colisões
        ts, Xs, Ys = StraightWalk(t, X, Y, Vn)
        #Coli = [[],[]]
        Cx,Cy, TList=Col(ts, Xs, Ys)
        #print(TList)
        #print(len(TList))
        #sys.exit()

        '''
        plt.scatter(X[:1000],Y[:1000], s=10,c='r')
        plt.scatter(Cx[:20],Cy[:20],c='g',s=10)
        #plt.scatter()#x_traj,y_traj,c='b',s=2)
        plt.show()
        '''
        '''

        #print(Cx)
        plt.plot(Cx,Cy,'o')
        plt.show()
        sys.exit()

        '''
        #Pronto, até aqui eu tenho todas as colisçoes
        #Cx = Cx
        #Cy = Cy
        #print(Cx)
        print(f'max:{max(Cx)}')
        #print(min(Cy))
        Cym= 0#np.mean(Cy)
        Altura_y = max(Cy)+np.abs(min(Cy))
        #print(Cym)
        #sys.exit()
        #Partindo para identificação dos circulos
        conjunto_sup_cs = []  # Valores de Y acima da média
        conjunto_sup_xs = []  # Valores de X correspondentes
        conjunto_inf_ci = []  # Valores de Y abaixo da média
        conjunto_inf_xi = []  # Valores de X correspondentes
        # Calcula os valores de alfa e gamma
        for i in range(len(Cy)):
            if Cy[i] > Cym:
                conjunto_sup_xs.append(Cx[i])
                conjunto_sup_cs.append(Cy[i])
            else:
                conjunto_inf_xi.append(Cx[i])
                conjunto_inf_ci.append(Cy[i])

        pontos_x_sup = conjunto_sup_xs
        pontos_y_sup = conjunto_sup_cs

        pontos_x_inf = conjunto_inf_xi
        pontos_y_inf = conjunto_inf_ci

        #Encontra os parâmetros do círculo para os conjuntos acima e abaixo da média
        centro_sup, raio_sup, erro_centro_sup, erro_raio_sup = encontrar_parametros_circulo(pontos_x_sup, pontos_y_sup)
        centro_inf, raio_inf, erro_centro_inf, erro_raio_inf = encontrar_parametros_circulo(pontos_x_inf, pontos_y_inf)

        # Calcula a diferença entre as coordenadas dos centros dos círculos
        centro_AB = (centro_inf[0] - centro_sup[0], centro_inf[1] - centro_sup[1])
        print(f'Centrosup:x:{centro_sup[0]} y:{centro_sup[1]}')
        print(f'Centroinf:x:{centro_inf[0]} y:{centro_inf[1]}')
        print(f'raiosup:{raio_sup}')
        print(f'raioinf:{raio_inf}')
        #sys.exit()
        #plt.plot(Cx,Cy)
        #print(centro_AB)
        jj=[0,1]
        Ang_Cg,Ang_Cr = calcular_angulo(centro_AB,jj)
        print(Ang_Cr)
        '''
        if centro_AB[0]<0:
            for i in range(len(Cx)):
                Cx[i]=+Cx[i]*np.cos(Ang_Cr)-Cy[i]*np.sin(Ang_Cr)
                Cy[i]=+Cx[i]*np.sin(Ang_Cr)+Cy[i]*np.cos(Ang_Cr)

        else:
            for i in range(len(Cx)):
                Cx[i]=+Cx[i]*np.cos(Ang_Cr)+Cy[i]*np.sin(Ang_Cr)
                Cy[i]=-Cx[i]*np.sin(Ang_Cr)+Cy[i]*np.cos(Ang_Cr)
        '''
        #'''
        #plt.scatter(Cx,Cy)
        #plt.show()
        #sys.exit()
        #'''
        # Calcula o módulo (norma) da diferença entre os centros
        '''
        plt.scatter(X[:1000],Y[:1000], s=10,c='r')
        plt.scatter(Cx[:12],Cy[:12],c='g',s=10)
        #plt.scatter()#x_traj,y_traj,c='b',s=2)
        plt.show()
        '''
        modulo_AB = np.linalg.norm(centro_AB)

        #gamma = 1 - Altura_Y/(raio_sup+raio_inf)
        a = (centro_inf[1] - centro_sup[1])/2
        gamma = 2*a/(raio_sup+raio_inf)
        print(f'Novo:{a}  |  Antigo:{modulo_AB/2}')
        #Altura_Y=(1-gamma)*(raio_sup+raio_inf)
        #print(f'gamma:{gamma}')
        #sys.exit()
        #gamma=abs(gamma)
        #por facilidade
        #
        # Calcula o ângulo entre a reta centro_sup - centro_inf e o eixo Y
        angulo_radianos = np.arctan2(centro_AB[1], centro_AB[0])

        # Converte o ângulo de radianos para graus
        angulo_graus = np.degrees(angulo_radianos)-90
        R=np.pi/(2*np.arcsin(np.sqrt(1-(gamma)**2)))
        Re=(raio_sup+raio_inf)/2
        # Calcula os valores de alfa e gamma
        L0 =2*np.pi
        L1 =5.01 #tamanho do experimento
        H = L0*(1-gamma)/(2*np.arcsin(np.sqrt(1-gamma**2)))
        h = L1*(1-gamma)/(2*np.arcsin(np.sqrt(1-gamma**2))) #altura real
        N_y= R/Re
        #H/Altura_y #H/Altura_Y #Fator de normalização
        N_Yy=R/Re#h/Altura_y #H/Altura_Y #Fator de normalização
        N = len(Cx)
        #Norm = (np.max(Cy)- np.min(Cy))/H# 260
        #if not Nome.endswith('T_S'):
        Cx = (Cx-np.mean(Cx))*N_y
        Cy = (Cy-np.mean(Cy))*N_y

        X = (X-np.mean(X))*N_y
        Y = (Y-np.mean(Y))*N_y
        #Cx = (Cx-np.mean(X))/Norm
        #Cy = (Cy-np.mean(Y))/Norm

        
        #print("norma: "+str(Norm))
        print("Gamma: "+str(gamma))
        print("Altura teorica: "+str(H))
        print("Altura: "+str(np.max(Cy)+np.abs(np.min(Cy))))
        print("largura: "+str(np.max(Cx)+np.abs(np.min(Cx))))
        Xx = (X-np.mean(X))*N_Yy
        Yy = (Y-np.mean(Y))*N_Yy

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
        AngEff = [0. for i in range(len(Cx))]
        Nsteps = len(Cx)


        CgT=L0*np.sqrt(1-gamma**2)/(2*np.arcsin(np.sqrt(1-gamma**2)))
        largurax=max(Cx)+abs(min(Cx))
        if max(Cx) > CgT/2 or min(Cx)< -CgT/2:
            if max(Cx)>abs(min(Cx)):
                Cg=max(Cx)
            else:
                Cg=abs(min(Cx))
        else:
            Cg=CgT/2

        for i in range(1, Nsteps-1):

            TList[i] = TList[i] # MARCADORRRRRRRRRRRRRRRRRRRRRRRRRRRR

            if (Cy[i] >= np.mean(Cy)):
                c1 = [Cx[i + 1], Cy[i + 1]]
                c2 = [Cx[i], Cy[i]]
                c3 = [Cx[i - 1], Cy[i - 1]]
                R = Sub(c2,[ centro_sup[0], centro_sup[1]])
                RR= 1#raio_sup
                x_d = 1#np.sqrt(RR*RR - a*a)
                xx=Cx[i]
                yy=Cy[i]

                Per= np.arccos((xx)/(np.sqrt(xx**2+yy**2)))+np.pi

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
                ThetaList.append(Reflec)
                AlphaList.append(Alf)
                PerList.append(Per)

            if (Cy[i] < np.mean(Cy)):
                c1 = [Cx[i + 1], Cy[i + 1]]
                c2 = [Cx[i], Cy[i]]
                c3 = [Cx[i - 1], Cy[i - 1]]
                R = Sub(c2,[centro_inf[0], centro_inf[1]])
                RR = 1#raio_inf
                x_d = 1#np.sqrt(RR*RR - a*a)
                #RR=np.linalg.norm(R)*np.linalg.norm(R)
                xx=Cx[i]
                yy=Cy[i]
                '''
                if xx <- x_d:
                    xx=-np.sqrt(RR -(yy-a)**2)
                '''

                Per= np.arccos((-xx)/(np.sqrt(xx**2+yy**2)))

                if Per <0:
                    print(f'X_D: {-x_d} | x: {xx} | y: {yy} | Per: {Per}')
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
                ThetaList.append(Reflec)
                AlphaList.append(Alf)
                PerList.append(Per)
        #print('MinPerList: ' +str(np.min(PerList)))
        '''
        plt.scatter(X[:1000],Y[:1000], s=10,c='r')
        plt.scatter(Cx[:12],Cy[:12],c='g',s=10)
        #plt.scatter()#x_traj,y_traj,c='b',s=2)
        plt.show()
        '''
        '''
        if np.min(PerList)<0:
            PerList = PerList + abs(np.min(PerList))
            PerList = (PerList/(np.min(PerList)+np.max(PerList)))*(2*np.pi)
        if np.max(PerList)>2*np.pi:
            PerList = PerList - abs(np.min(PerList))
            PerList = (PerList/(np.min(PerList)+np.max(PerList)))*(2*np.pi)
        '''
        #print("PerList: "+str(len(PerList)))
        #print("EffAng: "+str(len(EffAng)))
        ###############################################################################

        data = open('DadosTratados/' + Nome + '_(Traj).dat', 'w+')
        print(Xx)
        for i in range(len(Xx)):
            # Calculate and write transformed data to the file
            data.write('%f %f %f %f\n' % (float(Xx[i]), float(Yy[i]), float(X[i]), float(Y[i])))
        data.close()

        # Ensure 'Nome' is defined appropriately before this code segment
        
        # Create and open a file for writing data
        data = open('DadosTratados/' + Nome + '_(T_Th_Ka_V).dat', 'w+')

        # Print the mean of V for reference
        #print("Media da velocidade V:", np.mean(V))

        # Iterate over the data and write to the file
        for i in range(len(Kappa)):
            # Calculate and write transformed data to the file
            data.write('%f %f %f %f\n' % (float(TList[i]*np.mean(V)), float(ThetaList[i]), float(Kappa[i]), float(VList[i]/np.mean(V))))

        # Close the file after writing
        data.close()

        # Create and open another file for writing data
        data = open('DadosTratados/' + Nome + '_(Per_SinTheta).dat', 'w+')

        # Print the mean of V for reference
        #print("Mean of V:", np.mean(V))

        # Iterate over the data and write to the file
        for i in range(len(PerList)):
            # Write transformed data to the file
            data.write('%f %f\n' % (float(PerList[i]), float((np.sin(ThetaList[i]) ))))  # Change Theta to sin(Theta)

        # Close the file after writing
        data.close()

        # Create and open a file for writing collision data
        data1 = open('DadosTratados/' + str(Nome) + '_Colisao(X-Y).dat', 'w+')

        # Iterate over collision data and write to the file
        for i in range(1,len(Cx)-1):
            data1.write('%f %f\n' % (float(Cx[i]), float(Cy[i])))

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
        '''
        print(f'---- {n_steps}')
        n_steps= len(t_list)/5
        print(f'----{n_steps}')
        n_steps=int(n_steps)
        print(f'----{n_steps}')
        '''
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
        Lista_LEG.append((Nome_sem_extensao, gamma, LE ,raio_inf,raio_sup,modulo_AB/2,))

        #####################################################
        #Graficos
        ########################################
        FS = 12
        nome_arquivo = Nome_sem_extensao

        # Load collision data
        caminho_arquivo_Colisao = 'DadosTratados/' + str(nome_arquivo) + '_Colisao(X-Y).dat'
        X_C, Y_C = np.loadtxt(caminho_arquivo_Colisao, unpack=True)

        # Load Poincaré map data
        caminho_arquivo_Poincare = 'DadosTratados/' + str(nome_arquivo) + '_(Per_SinTheta).dat'
        X_P, Y_P = np.loadtxt(caminho_arquivo_Poincare, unpack=True)

        # Determine color based on file name
        if not Nome.endswith('T_S'):
            COR = '#ff972f'
        else:
            COR = '#812fff'

        print(f'Tamanho de Poincarre:{len(X_P)}')
        print(f'Tamanho de Coli:{len(X_C)}')

        # Plot
        plt.figure(figsize=(15, 10))
        plt.suptitle(f'{nome_arquivo} | Gamma = {gamma:.5f} | Expoente Lyapunov = {LE:.5f} | Coli = {len(EffAng)}')

        # Plot 1: Trajectory
        plt.subplot(2, 3, 1)
        plt.plot(X, Y, color=COR, linestyle='solid', drawstyle='default', linewidth=1)
        plt.xlabel('X', fontsize=FS)
        plt.ylabel('Y', fontsize=FS)
        plt.axis('square')
        plt.ylim(-1.51, 1.51)
        plt.xlim(-1.51, 1.51)
        plt.grid(True)
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
        # Plot 2: Collision data
        plt.subplot(2,3, 2)
        plt.plot(X_C, Y_C, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
        plt.xlabel('X', fontsize=FS)
        plt.ylabel('Y', fontsize=FS)
        plt.axis('square')
        plt.ylim(-1.51, 1.51)
        plt.xlim(-1.51, 1.51)
        plt.grid(True)
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
        # Plot 3: Poincaré map data
        plt.subplot(2, 3, 3)
        plt.plot(X_P, Y_P, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='.', markersize=10, markeredgecolor='black')

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
        plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
        plt.grid(True)
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
        # Plot 4: Lyapunov data
        x, y = np.loadtxt('Lyapunov/' + Nome_sem_extensao + '.dat', unpack=True)
        plt.subplot(2, 3, 4)
        plt.axhline(LE, color='black', linestyle='solid', linewidth=1, alpha=1, label=f'LE ({LE:.5f})')
        plt.plot(x, y, color=COR)
        plt.ylim(y[-1] - 0.55, y[-1] + 0.55)
        plt.ylabel(r'$\gamma$', fontsize=FS)
        plt.xlabel('t', fontsize=FS)
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
        plt.grid(True)
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
        #plot 5
        P, A = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
        Tam = len(P)
        P=P/(2*np.pi)
        A=(A+1)/2

        e = 0.05
        e1= 0.01
        I = np.arange(Tam)
        DADOS0 = np.column_stack((I, P, A))
        MQ = np.zeros((Tam, Tam))
        SOMA =0
        for i in range(Tam):
            for k in range(Tam):
                if DADOS0[i][1] <= 0.1 and DADOS0[k][1] >= 0.9:
                    if abs(DADOS0[i][1] - DADOS0[k][1]-1) < e and abs(DADOS0[i][2] - DADOS0[k][2]-1) < e:                 
                        MQ[i][k] = 1
                        SOMA +=1  
                if abs(DADOS0[i][1] - DADOS0[k][1]) < e and abs(DADOS0[i][2] - DADOS0[k][2]) < e:                       
                    MQ[i][k] = 1
                    SOMA +=1
        RR = SOMA / (Tam * Tam)
        RR_f = format(RR, '.4f')
        x_coords, y_coords = np.where(MQ == 1)
        plt.subplot(2, 3, 5)
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
        plt.grid(True)
        plt.plot(x_coords, y_coords, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='o', markersize=3, markeredgecolor='black',alpha=1)
        plt.title(f'RR={RR_f} | e = {e}')
        plt.xlabel('Índice k')
        plt.ylabel('Índice i')
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)        
        #plot 6
        P, A = np.loadtxt(caminho_arquivo_Poincare, unpack=True)
        Tam = len(P)
        P=P/(2*np.pi)
        A=(A+1)/2

        e = 0.01
        I = np.arange(Tam)
        DADOS0 = np.column_stack((I, P, A))
        MQ = np.zeros((Tam, Tam))
        SOMA =0
        for i in range(Tam):
            for k in range(Tam):
                if (DADOS0[i][1] <= 0.1 and DADOS0[k][1] >= 0.9) or (DADOS0[k][1] <= 0.1 and DADOS0[i][1] >= 0.9):
                    if abs(DADOS0[i][1] - DADOS0[k][1]-1) < e and abs(DADOS0[i][2] - DADOS0[k][2]-1) < e:                 
                        MQ[i][k] = 1
                        SOMA +=1  
                if abs(DADOS0[i][1] - DADOS0[k][1]) < e and abs(DADOS0[i][2] - DADOS0[k][2]) < e:                       
                    MQ[i][k] = 1
                    SOMA +=1
        RR = SOMA / (Tam * Tam)
        RR_f = format(RR, '.4f')
        x_coords, y_coords = np.where(MQ == 1)
        plt.subplot(2, 3, 6)
        plt.minorticks_on()
        plt.grid(which='minor', linestyle=':', linewidth='0.1', color='gray')
        plt.grid(True)
        plt.plot(x_coords, y_coords, color=COR, linestyle='none', drawstyle='default', linewidth=1, marker='o', markersize=3, markeredgecolor='black',alpha=1)
        plt.title(f'RR={RR_f} | e = {e}')
        plt.xlabel('Índice k')
        plt.ylabel('Índice i')
        plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
        
        

        #plt.show()
        plt.savefig('Gráficos/' + str(nome_arquivo) + '.png', dpi=350)
        plt.close('all')
        # plt.show()  # Optionally display the plots interactively
    ######################################################
        if not Nome.endswith('T_S') and Simu==1:
            a= ((raio_sup+raio_inf)/2)*gamma
            # Tamanho do quadrado
            R1 = raio_sup
            R2 = raio_inf

            # Posição inicial aleatória dentro do quadrado
            x0 = X[0]
            y0 = Y[0]

            #vx0 = np.array([],[])
            # Tempo total de simulação e tamanho do passo de tempo
            dt = 0.01

            # Número de passos de tempo
            # Listas para armazenar posições ao longo do tempo
            x_traj = []
            y_traj = []
            print(f'X[0]:{X[0]} Y[0]:{Y[0]}')
            print(f'0-Cx:{Cx[0]} Cy:{Cy[0]}')
            print(f'1-Cx:{Cx[1]} Cy:{Cy[1]}')

            coli = [[X[0]],[Y[0]]]  # Inicialize coli como uma lista de listas
            # Loop de simulação usando o método de Euler
            x, y = x0, y0
            v = np.array([Cx[0]-X[0],Cy[0]-Y[0]])/dt
            v= calcular_versor(v)*Vm
            vm= calcular_modulo(v)

            centro = [[0,0],[a,-a]] # o centro inf é a parte inferior do limão, ou seja o circulo superior
            ii = [1,0]
            jj = [0,1]
            Anda = 10
            print(centro)
            #sys.exit()
            Para = 1000
            #x += v[0] *10* dt
            #y += v[1] *10* dt
            x_traj.append(x)
            y_traj.append(y)
            print(f'vm:{Vm} ')

            print(f'X[0]:{X[0]},x[0]:{x_traj[0]} ')
            count=0
            while len(coli[0]) <= 10*len(Cx):
                # Calcular novas posições usando o método de Euler
                x += v[0] * dt#*np.random.normal(1,0.1)
                y += v[1] * dt#*np.random.normal(1,0.1)
                #print(f'X: {X[count]} x:{x}')
                count +=1
                # Reflexão nas bordas do quadrado
                if y<=0:
                    raio1 = np.sqrt((x-centro[0][0])**2 + (y-centro[1][0])**2)
                    '''
                    plt.scatter(Cx[:len(coli[0])],Cy[:len(coli[0])],c='g',s=10)
                    plt.scatter(X[:len(x_traj)],Y[:len(x_traj)],s=10,c='r')
                plt.scatter(x_traj,y_traj,c='b',s=2)
                    plt.show()
                    '''

                    if raio1 > R1:
                        dist=np.sqrt( (x-coli[0][-1])**2+(y-coli[1][-1])**2 )
                        if dist <= vm*15:
                            x=x_traj[-1]
                            y=y_traj[-1]
                        coli[0].append(x)  # Adicione x à lista de colisões
                        coli[1].append(y)  # Adicione y à lista de colisões
                        #plt.scatter(X[0],Y[0],s=10,c='r')
                        #plt.scatter(coli[0],coli[1],c='b',s=2),
                        '''
                        plt.scatter(Cx[:len(coli[0])],Cy[:len(coli[0])],c='g',s=10)
                        plt.scatter(X[:len(x_traj)],Y[:len(x_traj)],s=10,c='r')
                        plt.scatter(x_traj,y_traj,c='b',s=2)
                        plt.show()
                        '''
                        Tcoli = len(coli[0])
                        Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                        Rdir = [coli[0][Tcoli - 1] - centro[0][0], coli[1][Tcoli - 1] - centro[1][0]]
                        Vvdir = calcular_versor(Vdir)
                        Rvdir = calcular_versor(Rdir)
                        phig, phir = calcular_angulo(Vdir, Rdir)

                        #print(v[0])

                        thetar=np.pi - 2*phir

                        vz=produto_vetorial(Rdir,Vdir)
                        if vz >0:
                            Fdir = np.array([v[0] * np.cos(thetar)-v[1]*np.sin(thetar), +v[0] * np.sin(thetar)+v[1]*np.cos(thetar)])  # Vetor resultante rotacionado
                        else:
                            Fdir = np.array([v[0] * np.cos(thetar)+v[1]*np.sin(thetar), -v[0] * np.sin(thetar)+v[1]*np.cos(thetar)])  # Vetor resultante rotacionado

                        #print(f'Fdir[0]{Fdir[0]}')
                        v[0] = Fdir[0]
                        v[1] = Fdir[1]
                        for i in range(Para):
                            x_traj.append(x)
                            y_traj.append(y)
                        x += v[0] *Anda* dt
                        y += v[1] *Anda* dt

                else:
                    raio2 = np.sqrt((x-centro[0][1])**2 + (y-centro[1][1])**2)
                    '''
                    plt.scatter(Cx[:len(coli[0])],Cy[:len(coli[0])],c='g',s=10)
                    plt.scatter(X[:len(x_traj)],Y[:len(x_traj)],s=10,c='r')
                plt.scatter(x_traj,y_traj,c='b',s=2)
                    plt.show()
                    '''
                    if raio2 > R2:
                        dist=np.sqrt( (x-coli[0][-1])**2+(y-coli[1][-1])**2 )
                        if dist <= vm*15:
                            x=x_traj[-1]
                            y=y_traj[-1]
                        coli[0].append(x)  # Adicione x à lista de colisões
                        coli[1].append(y)  # Adicione y à lista de colisões

                        '''
                        plt.scatter(Cx[:len(coli[0])],Cy[:len(coli[0])],c='g',s=10)
                        plt.scatter(X[:len(x_traj)],Y[:len(x_traj)],s=10,c='r')
                        plt.scatter(x_traj,y_traj,c='b',s=2)
                        plt.show()
                        '''

                        Tcoli = len(coli[0])
                        Vdir = [coli[0][Tcoli - 1] - coli[0][Tcoli - 2], coli[1][Tcoli - 1] - coli[1][Tcoli - 2]]
                        Rdir = [coli[0][Tcoli - 1] - centro[0][1], coli[1][Tcoli - 1] - centro[1][1]]
                        Vvdir = calcular_versor(Vdir)
                        Rvdir = calcular_versor(Rdir)
                        phig, phir = calcular_angulo(Vdir, Rdir)

                        #print(v[0])

                        thetar=np.pi - 2*phir

                        vz=produto_vetorial(Rdir,Vdir)
                        if vz >0:
                            Fdir = np.array([v[0] * np.cos(thetar)-v[1]*np.sin(thetar), +v[0] * np.sin(thetar)+v[1]*np.cos(thetar)])  # Vetor resultante rotacionado
                        else:
                            Fdir = np.array([v[0] * np.cos(thetar)+v[1]*np.sin(thetar), -v[0] * np.sin(thetar)+v[1]*np.cos(thetar)])  # Vetor resultante rotacionado

                        #print(f'Fdir[0]{Fdir[0]}')
                        v[0] = Fdir[0]
                        v[1] = Fdir[1]
                        for i in range(Para):
                            x_traj.append(x)
                            y_traj.append(y)
                        x += v[0] *Anda* dt
                        y += v[1] *Anda* dt
                # Armazenar novas posições''
                x_traj.append(x)
                y_traj.append(y)

                # Obter data e hora atual
            agora = datetime.datetime.now()

            # Formatar data e hora para incluir no nome do arquivo
            data_hora_formatada = agora.strftime("%Y-%m-%d_%H-%M-%S")

            # Nome do arquivo com data e hora
            nome_arquivo1 = f'{str(nome_arquivo)}_T_S.txt'#_{data_hora_formatada}.txt'
        #print(len(x_traj))  # Verifica o tamanho de x_traj
        #print(len(y_traj))  # Verifica o tamanho de y_traj

            # Abrir arquivo para escrita
            with open('DadosCrus/DadosSimulados/'+str(nome_arquivo1), 'w') as data:
                # Escreve cabeçalho


                # Loop sobre os dados da trajetória
                for i in range(len(y_traj)):
                    # Escreve os dados transformados no arquivo
                    data.write('%f %f %f %f\n' % (float(x_traj[i]), float(y_traj[i]), float(x_traj[i]), float(y_traj[i])))
            '''
            # Plotar a trajetória da partícula dentro do quadrado
            plt.figure(figsize=(6, 6))
            plt.plot(x_traj, y_traj, color = 'black', linestyle='none', drawstyle='default', linewidth=0.1, marker='.', markersize=1, markeredgecolor='black')
            plt.scatter(coli[0], coli[1], color='red')  # Adicione as colisões ao gráfico
            circle = plt.Circle((0, a), R1, color='black', fill=False)
            circle1 = plt.Circle((0, -a), R2, color='black', fill=False)
            plt.gca().add_patch(circle)
            plt.gca().add_patch(circle1)
            plt.xlim(-5,5)
            plt.ylim(-5,5)
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Trajetória da Partícula dentro do Limão')
            plt.grid(True)
            plt.close('all')

            #plt.show()
            '''
    ######################################################
    except Exception as e:
        print("Ocorreu o erro ao processar o arquivo {}:".format(str(e)))
        if Nome.endswith('T_S'):
            os.remove(os.path.join('DadosCrus/'+str(Nome)+'.txt'))
            print(f'O arquivo {Nome} Foi deletado, por ser uma Simulação.')
        continue
# Abrir arquivo de texto para escrita
with open('Lyapunov/N_G_LE_valores.txt', 'w') as arquivo_txt:
    arquivo_txt.write('Nome do Exp | Gamma | Expoent Lyapunov\n')
    for item in Lista_LEG:
        arquivo_txt.write(f'{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]} \n')

