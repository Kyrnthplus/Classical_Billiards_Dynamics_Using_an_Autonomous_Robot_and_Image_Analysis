# Master's Project Pending Checklist - Lemon Billiard

This document lists all tasks required to complete the objectives of the master's research project, categorized by areas of development.

## 1. Documentation and Planning
- [x] **Compile robot manuals**: Gather and reference datasheets and manuals of components in `docs/manuals/` (completed: [datasheets.bib](file:///media/Externos/HDEX/Dropbox/Obsidian/Quirino/10 - Anexos/10.03 - Projetos/10.03.12 - Lemon_Billiard/docs/manuals/datasheets.bib)).
- [x] **Electronic schematics**: Draw and include schematic diagrams of the robot circuitry (Arduino connections, drivers, sensors) in `docs/circuit/` (completed: `schema.svg` and `schema_lemon_robot.png`).

## 2. Hardware and 3D Printing
- [x] **CAD file organization**: Catalog and upload the final 3D modeling files (`.stl`) to the folder `hardware/3d_printing/` (completed: `LemonRobot.stl`).
- [x] **Slicing configuration**: Create a descriptive file containing the ideal printing parameters (temperatures, infill density, print speed, support) for the parts (completed: [slicing_config.md](file:///media/Externos/HDEX/Dropbox/Obsidian/Quirino/10 - Anexos/10.03 - Projetos/10.03.12 - Lemon_Billiard/hardware/3d_printing/slicing_config.md)).

## 3. Robot Software (Embedded Firmware)
- [x] **File structure**: Move the embedded control source code of the robot (Arduino firmware) to the folder `robot_software/` (completed: `RobotLemon_v1.ino`).
- [ ] **Refactoring and documentation**: Clean the embedded code, organize functions for motion and sensor readings, and document key robot control parameters.

## 4. Data Processing and Analysis Pipeline
- [ ] **Real trajectory tracking**: Execute the MATLAB script `data_pipeline/01_frame_extractor/robo_stadium_mac.m` to process video sequences of real physical experiments and extract raw coordinates to `data/raw/`.
- [ ] **Batch processing execution**: Run the modular pipeline (`main.py` options 2 and 3) to process raw coordinates, calculate geometric coefficients ($\gamma$), Lyapunov exponents ($\lambda$), and generate Poincaré maps under `data/results/`.
- [ ] **Comparative analysis**: Compare experimental results with numerical data from the simulator (`simulator.py`) to validate the chaotic billiard model.
