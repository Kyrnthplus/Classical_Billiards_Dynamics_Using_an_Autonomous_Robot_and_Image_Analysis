import os
import sys
import argparse
import glob
import random
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt

# Adds parent directory to system path to import geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def analyze_file(file_prefix):
    print(f"Analyzing dynamics for prefix: {file_prefix}")
    base_name = os.path.basename(file_prefix)
    filename_without_ext = os.path.splitext(base_name)[0]

    # Paths to processed intermediate data files
    traj_path = f"../../data/processed/{filename_without_ext}_(Traj).dat"
    th_ka_path = f"../../data/processed/{filename_without_ext}_(T_Th_Ka_V).dat"
    per_sin_path = f"../../data/processed/{filename_without_ext}_(Per_SinTheta).dat"
    col_xy_path = f"../../data/processed/{filename_without_ext}_Colisao(X-Y).dat"

    # Verify input file existence
    for p in [traj_path, th_ka_path, per_sin_path, col_xy_path]:
        if not os.path.exists(p):
            print(f"Error: Processed file {p} not found. Run the collision detector first.")
            return

    # Load data
    Xr, Yr, X, Y = np.loadtxt(traj_path, unpack=True)
    t_list, theta_list, kappa, vel = np.loadtxt(th_ka_path, unpack=True)
    X_P, Y_P = np.loadtxt(per_sin_path, unpack=True)
    X_C, Y_C = np.loadtxt(col_xy_path, unpack=True)

    # Re-estimate geometry parameters from collision points
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

    upper_center, upper_radius, _, _ = gu.fit_circle_parameters(upper_x, upper_y)
    lower_center, lower_radius, _, _ = gu.fit_circle_parameters(lower_x, lower_y)

    centers_difference = (lower_center[0] - upper_center[0], lower_center[1] - upper_center[1])
    a = (lower_center[1] - upper_center[1]) / 2.0
    gamma = 2.0 * a / (upper_radius + lower_radius)
    centers_distance = np.linalg.norm(centers_difference)

    print(f"Estimated parameters: Gamma = {gamma:.5f}, a = {a:.5f}, Upper Radius = {upper_radius:.3f}, Lower Radius = {lower_radius:.3f}")

    # Calculate Lyapunov exponent
    delta = np.array([random.uniform(0.1, 1.0), random.uniform(0.1, 1.0)])
    delta /= np.linalg.norm(delta)
    n_steps = len(t_list)

    os.makedirs("../../data/results", exist_ok=True)
    lyap_data_path = f"../../data/results/{filename_without_ext}_Lyapunov.dat"

    with open(lyap_data_path, "w") as fout:
        lambda_ = 0.0
        for ii in range(n_steps):
            u = delta[0]
            delta[0] = u + t_list[ii] * delta[1]
            delta[1] = delta[1]

            u = delta[0]
            delta[0] = -u
            delta[1] = vel[ii] * 2. * kappa[ii] / np.cos(theta_list[ii]) * u - delta[1]

            lambda_ += np.log(np.linalg.norm(delta))
            fout.write(f"{sum(t_list[:(ii + 1)]):.6f} {(lambda_ / sum(t_list[:(ii + 1)])):.6f}\n")
            delta /= np.linalg.norm(delta)

    LE = lambda_ / sum(t_list[:n_steps])
    print(f"Calculated Lyapunov Exponent (LE): {LE:.5f}")

    # Set plot colors based on simulated/experimental suffix
    if not filename_without_ext.endswith("T_S"):
        PLOT_COLOR = '#ff972f'  # Orange for experimental data
    else:
        PLOT_COLOR = '#812fff'  # Purple for simulation

    # Load calculated Lyapunov values for plotting
    lyap_x, lyap_y = np.loadtxt(lyap_data_path, unpack=True)

    # Plot Configuration and Generation
    FS = 12
    plt.figure(figsize=(15, 10))
    plt.suptitle(f"{filename_without_ext} | Gamma = {gamma:.5f} | Lyapunov Exponent = {LE:.5f} | Collisions = {len(theta_list)}")

    # Plot 1: Trajectory
    plt.subplot(2, 3, 1)
    plt.plot(X, Y, color=PLOT_COLOR, linestyle='solid', linewidth=1)
    plt.xlabel('X', fontsize=FS)
    plt.ylabel('Y', fontsize=FS)
    plt.axis('square')
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 2: Collision coordinates
    # Rescale for display
    NX = np.max(X) - np.min(X)
    NXc = np.max(X_C) - np.min(X_C)
    N_ratio = NX / NXc if NXc > 0 else 1.0
    X_C_scaled = X_C * N_ratio
    Y_C_scaled = Y_C * N_ratio

    plt.subplot(2, 3, 2)
    plt.plot(X_C_scaled, Y_C_scaled, color=PLOT_COLOR, linestyle='none', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
    plt.xlabel('X', fontsize=FS)
    plt.ylabel('Y', fontsize=FS)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 3: Poincaré phase space mapping
    plt.subplot(2, 3, 3)
    plt.plot(X_P, Y_P, color=PLOT_COLOR, linestyle='none', linewidth=1, marker='.', markersize=10, markeredgecolor='black')
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
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 4: Lyapunov Convergence
    plt.subplot(2, 3, 4)
    plt.axhline(LE, color='black', linestyle='solid', linewidth=1, alpha=1, label=f'LE ({LE:.5f})')
    plt.plot(lyap_x, lyap_y, color=PLOT_COLOR)
    plt.ylim(lyap_y[-1] - 0.55, lyap_y[-1] + 0.55)
    plt.ylabel(r'$\gamma$', fontsize=FS)
    plt.xlabel('t', fontsize=FS)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 5: Recurrence Plot and Recurrence Rate (RR) at epsilon = 0.05
    P_norm = X_P / (2 * np.pi)
    A_norm = (Y_P + 1) / 2
    Tam = len(P_norm)

    e1 = 0.05
    MQ1 = np.zeros((Tam, Tam))
    SOMA1 = 0
    for i in range(Tam):
        for k in range(Tam):
            if P_norm[i] <= 0.1 and P_norm[k] >= 0.9:
                if abs(P_norm[i] - P_norm[k] - 1) < e1 and abs(A_norm[i] - A_norm[k] - 1) < e1:
                    MQ1[i][k] = 1
                    SOMA1 += 1
            if abs(P_norm[i] - P_norm[k]) < e1 and abs(A_norm[i] - A_norm[k]) < e1:
                MQ1[i][k] = 1
                SOMA1 += 1
    RR1 = SOMA1 / (Tam * Tam) if Tam > 0 else 0
    x_coords1, y_coords1 = np.where(MQ1 == 1)

    plt.subplot(2, 3, 5)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.plot(x_coords1, y_coords1, color=PLOT_COLOR, linestyle='none', marker='o', markersize=3, markeredgecolor='black')
    plt.title(f'RR={RR1:.4f} | e = {e1}')
    plt.xlabel('Index k')
    plt.ylabel('Index i')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Plot 6: Recurrence Plot and RR at epsilon = 0.01
    e2 = 0.01
    MQ2 = np.zeros((Tam, Tam))
    SOMA2 = 0
    for i in range(Tam):
        for k in range(Tam):
            if (P_norm[i] <= 0.1 and P_norm[k] >= 0.9) or (P_norm[k] <= 0.1 and P_norm[i] >= 0.9):
                if abs(P_norm[i] - P_norm[k] - 1) < e2 and abs(A_norm[i] - A_norm[k] - 1) < e2:
                    MQ2[i][k] = 1
                    SOMA2 += 1
            if abs(P_norm[i] - P_norm[k]) < e2 and abs(A_norm[i] - A_norm[k]) < e2:
                MQ2[i][k] = 1
                SOMA2 += 1
    RR2 = SOMA2 / (Tam * Tam) if Tam > 0 else 0
    x_coords2, y_coords2 = np.where(MQ2 == 1)

    plt.subplot(2, 3, 6)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray')
    plt.grid(True)
    plt.plot(x_coords2, y_coords2, color=PLOT_COLOR, linestyle='none', marker='o', markersize=3, markeredgecolor='black')
    plt.title(f'RR={RR2:.3g} | e = {e2}')
    plt.xlabel('Index k')
    plt.ylabel('Index i')
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Save 2x3 Plot as PNG
    plt.savefig(f"../../data/results/{filename_without_ext}.png", dpi=350)
    plt.close('all')

    # Reconfigure fonts for publication figures
    plt.rcParams['font.family'] = 'serif'
    plt.rcParams['mathtext.fontset'] = 'stix'

    # Widescreen 3-Column Figure (Trajectory, Poincaré, Recurrence e=0.01)
    FS_PDF = 24
    plt.figure(figsize=(17, 6.3))
    plt.suptitle(f"{filename_without_ext} | "r"$\gamma$" f" = {gamma:.3g} | "r"$\lambda$" f" = {LE:.3g} | Collisions = {len(theta_list)} | $RR$={RR2:.3g} | "r"$\varepsilon$" f" = {e2}", fontsize=FS_PDF*3/4)

    # Column 1: Trajectory + Collisions
    plt.subplot(1, 3, 1)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.scatter(X, Y, color='black', s=0.1, alpha=0.55, zorder=2, marker='o')
    plt.plot(X_C_scaled, Y_C_scaled, color=PLOT_COLOR, linestyle='none', marker='.', markersize=10, markeredgecolor='black', zorder=3)
    plt.xlabel(r'$X$', fontsize=FS_PDF)
    plt.ylabel(r'$Y$', fontsize=FS_PDF)
    plt.xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF*3/4)
    plt.yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF*3/4)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Column 2: Poincaré map
    plt.subplot(1, 3, 2)
    plt.plot(X_P, Y_P, color=PLOT_COLOR, linestyle='none', marker='.', markersize=10, markeredgecolor='black')
    plt.xticks(x_ticks_positions, x_ticks_labels, fontsize=FS_PDF*3/4)
    plt.xlabel(r'$\ell$', fontsize=FS_PDF)
    plt.ylabel(r'sin $\phi$', fontsize=FS_PDF)
    plt.yticks([-1, -0.5, 0, 0.5, 1], fontsize=FS_PDF*3/4)
    plt.ylim(-1, 1)
    plt.xlim(-0.2, 2 * np.pi + 0.2)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)

    # Column 3: Recurrence Matrix
    plt.subplot(1, 3, 3)
    plt.minorticks_on()
    plt.xticks(fontsize=FS_PDF*3/4)
    plt.yticks(fontsize=FS_PDF*3/4)
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.plot(x_coords2, y_coords2, color=PLOT_COLOR, linestyle='none', marker='o', markersize=5, markeredgecolor='black', alpha=1)
    plt.xlabel(r'Index $i$', fontsize=FS_PDF)
    plt.ylabel(r'Index $j$', fontsize=FS_PDF)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
    plt.subplots_adjust(left=0.075, right=0.975, top=0.85, bottom=0.15, wspace=0.25)

    plt.savefig(f"../../data/results/{filename_without_ext}_report.png", dpi=350)
    plt.close('all')

    # Isolated Trajectory + Collisions Plot
    plt.figure(figsize=(8, 7))
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.scatter(X, Y, color='black', s=0.3, alpha=0.55, zorder=2, marker='o', label='Trajectory')
    plt.plot(X_C_scaled, Y_C_scaled, color=PLOT_COLOR, linestyle='none', marker='.', markersize=12.5, markeredgecolor='black', zorder=3, label='Collision')
    plt.legend(loc='upper right', fontsize=FS_PDF*3/4)
    plt.xlabel(r'$X$', fontsize=FS_PDF)
    plt.ylabel(r'$Y$', fontsize=FS_PDF)
    plt.xticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF)
    plt.yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], fontsize=FS_PDF)
    plt.ylim(-1.01, 1.01)
    plt.xlim(-1.01, 1.01)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True, pad=10)
    plt.subplots_adjust(left=0.2, right=0.90, top=0.95, bottom=0.15, wspace=0.25)
    plt.savefig(f"../../data/results/{filename_without_ext}_TC.png", dpi=350)
    plt.close('all')

    # Isolated Poincaré Plot (Tiago Model)
    NX_T = 9
    NY_T = 6
    FS_T = 30
    PAD_T = 10
    plt.figure(figsize=(NX_T, NY_T))
    plt.plot(X_P, Y_P, color=PLOT_COLOR, linestyle='none', marker='.', markersize=10, markeredgecolor='black', label='Measurement')
    plt.xlabel(r'$ \ell $', fontsize=FS_T)
    plt.ylabel(r'sin$~\phi$', fontsize=FS_T)
    plt.yticks(np.arange(-1, 1.001, 0.5), fontsize=FS_T*4/5)
    plt.xticks([0, 0.5 * pi_value, pi_value, 1.5 * pi_value, 2 * pi_value],
               ['0', r'$\frac{\pi}{2}$', r'$\pi$', r'$\frac{3\pi}{2}$', r'$2\pi$'],
               fontsize=FS_T*4/5)
    plt.ylim(-1, 1)
    plt.xlim(0, 2 * pi_value + 0.01)
    plt.tick_params(axis='y', which='major', pad=PAD_T)
    plt.tick_params(axis='x', which='major', pad=PAD_T)
    plt.minorticks_on()
    plt.grid(which='minor', linestyle=':', linewidth=0.1, color='gray', alpha=0.25)
    plt.grid(which='major', linestyle='-', linewidth=0.5, color='gray', alpha=0.25)
    plt.tick_params(axis='both', which='both', direction='in', top=True, right=True, bottom=True, left=True)
    plt.subplots_adjust(left=0.15, right=0.95, top=0.90, bottom=0.20)
    plt.savefig(f"../../data/results/{filename_without_ext}Tiago.png")
    plt.close('all')

    print(f"Plots saved successfully in data/results/ for: {filename_without_ext}")

    # Update consolidated parameter log file in results folder
    val_file = "../../data/results/N_G_LE_Ri_Rs_M_valores.txt"
    exists = os.path.exists(val_file)
    with open(val_file, "a" if exists else "w") as f:
        if not exists:
            f.write("Exp Name | Gamma | Lyapunov Exponent | Zeta | R_i | R_s | Modulus\n")
        f.write(f"{filename_without_ext} {gamma:.6f} {LE:.6f} {N_ratio:.6f} {lower_radius:.6f} {upper_radius:.6f} {centers_distance/2:.6f}\n")

def main():
    parser = argparse.ArgumentParser(description="Lemon Billiard Chaotic Dynamics Analyzer")
    parser.add_argument("--file", type=str, help="Prefix of the processed file in data/processed/ to analyze")
    args = parser.parse_args()

    # Change working directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    processed_dir = "../../data/processed"
    if args.file:
        prefix = os.path.join(processed_dir, args.file)
        analyze_file(prefix)
    else:
        # Batch processing: finds all *_(Traj).dat files
        files = glob.glob(os.path.join(processed_dir, "*_(Traj).dat"))
        if not files:
            print(f"No processed files found in {processed_dir}")
            return
        for f in sorted(files):
            prefix = f.replace("_(Traj).dat", "")
            analyze_file(prefix)

if __name__ == "__main__":
    main()
