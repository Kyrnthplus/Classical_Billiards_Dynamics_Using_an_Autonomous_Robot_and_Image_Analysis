import os
import sys
import argparse
import random
import numpy as np

# Adds parent directory to system path to import geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def run_simulation(init_file=None, test_mode=False, custom_gamma=0.5):
    print("Starting Lemon Billiard Numerical Simulation...")

    # Default parameters
    R1 = 1.0
    R2 = 1.0
    gamma = custom_gamma
    a = R1 * gamma  # Half distance between centers based on average radius and gamma
    mean_V = 0.5
    x0 = 0.1
    y0 = 0.1
    vx0 = 0.4
    vy0 = 0.3
    output_name = "simulation"

    # If an experimental file is provided to replicate initial conditions
    if init_file:
        base = os.path.basename(init_file)
        filename_without_ext = os.path.splitext(base)[0]
        output_name = f"{filename_without_ext}"

        # Loads raw coordinates to extract initial position and velocity
        try:
            X, Y, _, _ = np.loadtxt(init_file, unpack=True)
        except Exception:
            try:
                X, Y = np.loadtxt(init_file, usecols=(0, 1), unpack=True)
            except Exception as e:
                print(f"Error loading initialization file: {e}")
                return

        x0 = X[0]
        y0 = Y[0]
        # Estimating initial velocities
        if len(X) > 2:
            vx0 = (X[1] - X[0]) * 30.0
            vy0 = (Y[1] - Y[0]) * 30.0
            mean_V = np.mean(np.sqrt(np.gradient(X, 1.0/30.0)**2 + np.gradient(Y, 1.0/30.0)**2))
        else:
            vx0 = 0.3
            vy0 = 0.3
            mean_V = 0.4

        # Read processed parameters if they exist
        processed_xy = f"../../data/processed/{filename_without_ext}_Colisao(X-Y).dat"
        if os.path.exists(processed_xy):
            try:
                X_C, Y_C = np.loadtxt(processed_xy, unpack=True)
                mean_cy_threshold = 0.0
                upper_x = []
                upper_y = []
                lower_x = []
                lower_y = []
                for i in range(len(Y_C)):
                    if Y_C[i] > mean_cy_threshold:
                        upper_x.append(X_C[i])
                        upper_y.append(Y_C[i])
                    else:
                        lower_x.append(X_C[i])
                        lower_y.append(Y_C[i])
                _, R1, _, _ = gu.fit_circle_parameters(upper_x, upper_y)
                _, R2, _, _ = gu.fit_circle_parameters(lower_x, lower_y)
                upper_center, _, _, _ = gu.fit_circle_parameters(upper_x, upper_y)
                lower_center, _, _, _ = gu.fit_circle_parameters(lower_x, lower_y)
                a = (lower_center[1] - upper_center[1]) / 2.0
                gamma = 2.0 * a / (R1 + R2)
            except Exception as e:
                print(f"Warning: Failed to load parameters from processed files. Error: {e}")

    dt = 0.01
    x_traj = [x0]
    y_traj = [y0]

    # Max collisions to simulate
    max_collisions = 20 if test_mode else 100
    collisions = [[x0], [y0]]

    x = x0
    y = y0
    v = np.array([vx0, vy0])
    v = gu.calculate_unit_vector(v) * mean_V
    vm = gu.calculate_magnitude(v)

    centers = [[0.0, 0.0], [a, -a]] # centers[0] = x_cent, centers[1] = y_cent
    step_multiplier = 10
    stabilization_steps = 1000

    print(f"Simulation Parameters: R1={R1:.3f}, R2={R2:.3f}, a={a:.3f}, Gamma={gamma:.4f}, Vm={mean_V:.4f}")
    print(f"Initial Position: ({x0:.3f}, {y0:.3f}) | Initial Velocity: ({v[0]:.3f}, {v[1]:.3f})")

    steps_count = 0
    max_steps = 10000 if test_mode else 1000000

    while len(collisions[0]) <= max_collisions and steps_count < max_steps:
        x += v[0] * dt
        y += v[1] * dt
        steps_count += 1

        # Elastic reflections on boundary arcs
        if y <= 0.0:
            radius1 = np.sqrt((x - centers[0][0])**2 + (y - centers[1][0])**2)
            if radius1 > R1:
                # Prevent getting stuck by stepping back
                dist = np.sqrt((x - collisions[0][-1])**2 + (y - collisions[1][-1])**2)
                if dist <= vm * 15.0:
                    x = x_traj[-1]
                    y = y_traj[-1]
                collisions[0].append(x)
                collisions[1].append(y)

                num_collisions = len(collisions[0])
                velocity_dir = [collisions[0][num_collisions - 1] - collisions[0][num_collisions - 2], collisions[1][num_collisions - 1] - collisions[1][num_collisions - 2]]
                radius_dir = [collisions[0][num_collisions - 1] - centers[0][0], collisions[1][num_collisions - 1] - centers[1][0]]
                _, phi_rad = gu.calculate_angle(velocity_dir, radius_dir)
                theta_reflection = np.pi - 2.0 * phi_rad

                cross_z = gu.cross_product(radius_dir, velocity_dir)
                if cross_z > 0.0:
                    reflected_velocity = np.array([v[0] * np.cos(theta_reflection) - v[1] * np.sin(theta_reflection), +v[0] * np.sin(theta_reflection) + v[1] * np.cos(theta_reflection)])
                else:
                    reflected_velocity = np.array([v[0] * np.cos(theta_reflection) + v[1] * np.sin(theta_reflection), -v[0] * np.sin(theta_reflection) + v[1] * np.cos(theta_reflection)])

                v[0] = reflected_velocity[0]
                v[1] = reflected_velocity[1]

                for _ in range(stabilization_steps):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * step_multiplier * dt
                y += v[1] * step_multiplier * dt
        else:
            radius2 = np.sqrt((x - centers[0][1])**2 + (y - centers[1][1])**2)
            if radius2 > R2:
                dist = np.sqrt((x - collisions[0][-1])**2 + (y - collisions[1][-1])**2)
                if dist <= vm * 15.0:
                    x = x_traj[-1]
                    y = y_traj[-1]
                collisions[0].append(x)
                collisions[1].append(y)

                num_collisions = len(collisions[0])
                velocity_dir = [collisions[0][num_collisions - 1] - collisions[0][num_collisions - 2], collisions[1][num_collisions - 1] - collisions[1][num_collisions - 2]]
                radius_dir = [collisions[0][num_collisions - 1] - centers[0][1], collisions[1][num_collisions - 1] - centers[1][1]]
                _, phi_rad = gu.calculate_angle(velocity_dir, radius_dir)
                theta_reflection = np.pi - 2.0 * phi_rad

                cross_z = gu.cross_product(radius_dir, velocity_dir)
                if cross_z > 0.0:
                    reflected_velocity = np.array([v[0] * np.cos(theta_reflection) - v[1] * np.sin(theta_reflection), +v[0] * np.sin(theta_reflection) + v[1] * np.cos(theta_reflection)])
                else:
                    reflected_velocity = np.array([v[0] * np.cos(theta_reflection) + v[1] * np.sin(theta_reflection), -v[0] * np.sin(theta_reflection) + v[1] * np.cos(theta_reflection)])

                v[0] = reflected_velocity[0]
                v[1] = reflected_velocity[1]

                for _ in range(stabilization_steps):
                    x_traj.append(x)
                    y_traj.append(y)
                x += v[0] * step_multiplier * dt
                y += v[1] * step_multiplier * dt

        x_traj.append(x)
        y_traj.append(y)

    # Ensure raw data folder exists
    os.makedirs("../../data/raw", exist_ok=True)
    out_file = f"../../data/raw/{output_name}_T_S.txt"
    with open(out_file, "w") as f:
        for i in range(len(x_traj)):
            f.write(f"{x_traj[i]:.6f} {y_traj[i]:.6f} {x_traj[i]:.6f} {y_traj[i]:.6f}\n")

    print(f"Simulation completed! Trajectory saved in {out_file} ({len(x_traj)} points).")

def main():
    parser = argparse.ArgumentParser(description="Lemon Billiard Numerical Simulator")
    parser.add_argument("--init_file", type=str, help="Experimental file to replicate initial conditions")
    parser.add_argument("--gamma", type=float, default=0.5, help="Billiard Gamma parameter (default: 0.5)")
    parser.add_argument("--test", action="store_true", help="Runs a quick test simulation for verification")
    args = parser.parse_args()

    # Change working directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    run_simulation(init_file=args.init_file, test_mode=args.test, custom_gamma=args.gamma)

if __name__ == "__main__":
    main()
