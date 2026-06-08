import subprocess
import sys

def menu():
    print("\n================ LEMON BILLIARD - EXECUTION MENU ================")
    print("1. Run Numerical Simulator (simulator.py)")
    print("2. Run Collision Detector (detect_collisions.py)")
    print("3. Run Chaotic Dynamics Analyzer and Plotter (analyze_dynamics.py)")
    print("4. Run Complete Verification Pipeline (verify_pipeline.py)")
    print("5. Run Project Cleanup (clean_project.sh)")
    print("0. Exit")
    print("==================================================================")

def main():
    while True:
        menu()
        try:
            option = input("Choose an option (0-5): ").strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        if option == "1":
            gamma = input("Define Gamma parameter (Enter for default 0.5): ").strip()
            cmd = [sys.executable, "data_pipeline/04_simulator/simulator.py"]
            if gamma:
                cmd.extend(["--gamma", gamma])
            subprocess.run(cmd)
            
        elif option == "2":
            file = input("Filename in data/raw/ (Enter to batch process all): ").strip()
            cmd = [sys.executable, "data_pipeline/02_collision_detector/detect_collisions.py"]
            if file:
                cmd.extend(["--file", file])
            subprocess.run(cmd)
            
        elif option == "3":
            file = input("Processed prefix in data/processed/ (Enter to batch process all): ").strip()
            cmd = [sys.executable, "data_pipeline/03_analysis/analyze_dynamics.py"]
            if file:
                cmd.extend(["--file", file])
            subprocess.run(cmd)
            
        elif option == "4":
            subprocess.run([sys.executable, "verify_pipeline.py"])
            
        elif option == "5":
            subprocess.run(["./clean_project.sh"])
            
        elif option == "0":
            print("Exiting control menu.")
            break
        else:
            print("Invalid option. Please select a valid number.")

if __name__ == "__main__":
    main()
