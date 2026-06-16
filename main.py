import subprocess
import sys

def menu():
    print("\n================ LEMON BILLIARD - EXECUTION MENU ================")
    print("1. Extract Frames from Video (extract_frames.sh)")
    print("2. Track Trajectory - Python Interactive (track_trajectory.py)")
    print("3. Track Trajectory - MATLAB/Octave (track_trajectory.m)")
    print("4. Run Collision Detector (detect_collisions.py)")
    print("5. Run Chaotic Dynamics Analyzer and Plotter (analyze_dynamics.py)")
    print("6. Run Complete Verification Pipeline (verify_pipeline.py)")
    print("7. Run Project Cleanup (clean_project.sh)")
    print("0. Exit")
    print("==================================================================")

def main():
    while True:
        menu()
        try:
            option = input("Choose an option (0-7): ").strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            break

        if option == "1":
            print("\nExtracting frames from raw videos...")
            subprocess.run(["bash", "data_pipeline/01_frame_extractor/extract_frames.sh"])
            
        elif option == "2":
            print("\nTracking trajectory coordinates (Python Interactive)...")
            cmd = [sys.executable, "data_pipeline/01_frame_extractor/track_trajectory.py"]
            subprocess.run(cmd)

        elif option == "3":
            print("\nTracking trajectory coordinates (MATLAB/Octave)...")
            success = False
            for cmd_name in ["octave", "matlab"]:
                try:
                    if cmd_name == "octave":
                        cmd = ["octave", "--no-gui", "--eval", "run('data_pipeline/01_frame_extractor/track_trajectory.m')"]
                    else:
                        cmd = ["matlab", "-batch", "run('data_pipeline/01_frame_extractor/track_trajectory.m')"]
                    
                    res = subprocess.run(cmd)
                    if res.returncode == 0:
                        print("Trajectory coordinate tracking finished successfully.")
                        success = True
                        break
                except FileNotFoundError:
                    continue
            
            if not success:
                print("Error: Neither Octave nor MATLAB was found in your PATH.")
                print("Please make sure Octave (e.g. 'sudo apt install octave') or MATLAB is installed.")

        elif option == "4":
            file = input("Filename in data/raw/ (Enter to batch process all): ").strip()
            cmd = [sys.executable, "data_pipeline/02_collision_detector/detect_collisions.py"]
            if file:
                cmd.extend(["--file", file])
            subprocess.run(cmd)
            
        elif option == "5":
            file = input("Processed prefix in data/processed/ (Enter to batch process all): ").strip()
            cmd = [sys.executable, "data_pipeline/03_analysis/analyze_dynamics.py"]
            if file:
                cmd.extend(["--file", file])
            subprocess.run(cmd)
            
        elif option == "6":
            subprocess.run([sys.executable, "verify_pipeline.py"])
            
        elif option == "7":
            subprocess.run(["bash", "./clean_project.sh"])
            
        elif option == "0":
            print("Exiting control menu.")
            break
        else:
            print("Invalid option. Please select a valid number.")

if __name__ == "__main__":
    main()
