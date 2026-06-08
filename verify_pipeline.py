import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n==========================================")
    print(f"Executando: {description}")
    print(f"Comando: {' '.join(command)}")
    print(f"==========================================")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Saída:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Erro durante a execução:")
        print(e.stderr)
        print(e.stdout)
        return False

def main():
    # Caminhos relativos a partir da raiz do repositório
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    print("Iniciando verificação do pipeline Lemon Billiard...")

    # 1. Executa a Simulação de Teste
    sim_cmd = [sys.executable, "data_pipeline/04_simulator/simulator.py", "--test"]
    if not run_command(sim_cmd, "Etapa 1/3 - Simulação Numérica de Teste (--test)"):
        print("Falha na Etapa 1.")
        sys.exit(1)

    # 2. Executa a Detecção de Colisões
    det_cmd = [sys.executable, "data_pipeline/02_collision_detector/detect_collisions.py", "--file", "simulacao_T_S.txt"]
    if not run_command(det_cmd, "Etapa 2/3 - Detecção de Colisões e Ajuste Geométrico"):
        print("Falha na Etapa 2.")
        sys.exit(1)

    # 3. Executa a Análise de Dinâmica Caótica
    ana_cmd = [sys.executable, "data_pipeline/03_analysis/analyze_dynamics.py", "--file", "simulacao_T_S"]
    if not run_command(ana_cmd, "Etapa 3/3 - Reconstrução Dinâmica e Geração de Gráficos"):
        print("Falha na Etapa 3.")
        sys.exit(1)

    print("\n==========================================")
    print("Sucesso! Todo o pipeline Lemon Billiard foi executado e validado ponta a ponta.")
    print("Os dados intermediários estão em 'data/processed/' e os gráficos/resultados em 'data/results/'.")
    print("==========================================")

if __name__ == "__main__":
    main()
