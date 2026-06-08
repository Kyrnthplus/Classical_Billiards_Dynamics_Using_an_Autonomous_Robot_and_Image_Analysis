import subprocess
import sys

def menu():
    print("\n================ LEMON BILLIARD - MENU DE EXECUÇÃO ================")
    print("1. Executar Simulador (simulator.py)")
    print("2. Executar Detector de Colisões (detect_collisions.py)")
    print("3. Executar Analisador de Dinâmica e Gráficos (analyze_dynamics.py)")
    print("4. Executar Pipeline Completo (verify_pipeline.py)")
    print("5. Executar Limpeza do Projeto (clean_project.sh)")
    print("0. Sair")
    print("====================================================================")

def main():
    while True:
        menu()
        try:
            opcao = input("Escolha uma opção (0-5): ").strip()
        except KeyboardInterrupt:
            print("\nEncerrando.")
            break

        if opcao == "1":
            gamma = input("Defina o valor do parâmetro Gamma (Enter para default 0.5): ").strip()
            cmd = [sys.executable, "data_pipeline/04_simulator/simulator.py"]
            if gamma:
                cmd.extend(["--gamma", gamma])
            subprocess.run(cmd)
            
        elif opcao == "2":
            arquivo = input("Nome do arquivo em data/raw/ (Enter para processar todos em lote): ").strip()
            cmd = [sys.executable, "data_pipeline/02_collision_detector/detect_collisions.py"]
            if arquivo:
                cmd.extend(["--file", arquivo])
            subprocess.run(cmd)
            
        elif opcao == "3":
            arquivo = input("Prefixo do arquivo processado em data/processed/ (Enter para processar todos): ").strip()
            cmd = [sys.executable, "data_pipeline/03_analysis/analyze_dynamics.py"]
            if arquivo:
                cmd.extend(["--file", arquivo])
            subprocess.run(cmd)
            
        elif opcao == "4":
            subprocess.run([sys.executable, "verify_pipeline.py"])
            
        elif opcao == "5":
            subprocess.run(["./clean_project.sh"])
            
        elif opcao == "0":
            print("Encerrando menu de controle.")
            break
        else:
            print("Opção inválida. Selecione uma opção válida.")

if __name__ == "__main__":
    main()
