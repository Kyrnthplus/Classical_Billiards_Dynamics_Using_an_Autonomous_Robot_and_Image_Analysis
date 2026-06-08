import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n==========================================")
    print(f"Executing: {description}")
    print(f"Command: {' '.join(command)}")
    print(f"==========================================")
    try:
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Output:")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Error during execution:")
        print(e.stderr)
        print(e.stdout)
        return False

def main():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    print("Starting Lemon Billiard pipeline verification...")

    # 1. Runs Test Simulation
    sim_cmd = [sys.executable, "data_pipeline/04_simulator/simulator.py", "--test"]
    if not run_command(sim_cmd, "Step 1/3 - Numerical Test Simulation (--test)"):
        print("Failed on Step 1.")
        sys.exit(1)

    # 2. Runs Collision Detector
    det_cmd = [sys.executable, "data_pipeline/02_collision_detector/detect_collisions.py", "--file", "simulacao_T_S.txt"]
    if not run_command(det_cmd, "Step 2/3 - Collision Detection and Geometric Calibration"):
        print("Failed on Step 2.")
        sys.exit(1)

    # 3. Runs Dynamics Analyzer
    ana_cmd = [sys.executable, "data_pipeline/03_analysis/analyze_dynamics.py", "--file", "simulacao_T_S"]
    if not run_command(ana_cmd, "Step 3/3 - Dynamical Reconstruction and Figure Generation"):
        print("Failed on Step 3.")
        sys.exit(1)

    print("\n==========================================")
    print("Success! The entire Lemon Billiard pipeline has been executed and validated end-to-end.")
    print("Intermediate data is stored in 'data/processed/' and plots/results in 'data/results/'.")
    print("==========================================")

if __name__ == "__main__":
    main()
