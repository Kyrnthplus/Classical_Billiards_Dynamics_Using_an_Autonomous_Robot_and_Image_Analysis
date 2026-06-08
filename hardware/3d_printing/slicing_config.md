# 3D Printing Slicing Parameters (PLA)

This document specifies the recommended slicing parameters for manufacturing the structural parts of the robot (e.g. [LemonRobot.stl](file:///media/Externos/HDEX/Dropbox/Obsidian/Quirino/10 - Anexos/10.03 - Projetos/10.03.12 - Lemon_Billiard/hardware/3d_printing/LemonRobot.stl)).

## Thermal Parameters
* **Material**: PLA (Polylactic Acid)
* **Nozzle Temperature (Extruder)**: 200 °C (Reference range: 190 °C - 210 °C)
* **Bed Temperature (Build Plate)**: 60 °C (Reference range: 50 °C - 60 °C)

## Structure and Infill
* **Infill Density**: 50% (High mechanical strength for the chassis)
* **Infill Pattern**: Gyroid
  * *Note*: The gyroid pattern distributes mechanical strength isotropically (in three dimensions) and reduces shear stresses during high-speed printing.
* **Layer Height**: 0.2 mm (Standard for balancing surface finish and printing time)
* **Perimeters (Walls)**: 3 wall loops (minimum 1.2 mm wall thickness)
* **Top/Bottom Layers**: 4 solid layers

## Cooling and Speed
* **Print Speed**: 50 mm/s (Outer perimeters: 35 mm/s; infill: 60 mm/s)
* **Cooling Fan**: 100% active (disabled on the first layer to improve bed adhesion)
* **Supports**: Enable automatic supports for overhang angles greater than 45°.
