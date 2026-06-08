import os
import sys
import argparse
import glob
import numpy as np
from scipy.signal import butter, filtfilt

# Adds parent directory to system path to import geometry_utils
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import geometry_utils as gu

def lowpass_filter(data, cutoff, fs, order):
    normal_cutoff = cutoff / fs
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

def straight_walk_detector(t, x, y, v):
    ts = []
    xs = []
    ys = []
    for i in range(len(x)):
        if v[i] > 0.1:
            xs.append(x[i])
            ys.append(y[i])
            ts.append(t[i])
    return ts, xs, ys

def detect_collisions(ts, xs, ys, dt):
    tdiff = np.diff(ts)
    start_idx = 0
    flight_duration = 0.0
    collision_x = []
    collision_y = []
    time_intervals = []
    for i in range(len(ts)-1):
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            collision_x.append(x1)
            collision_y.append(y1)
            time_intervals.append(flight_duration)
            flight_duration = 0.0
        flight_duration = flight_duration + dt
    return collision_x, collision_y, np.array(time_intervals).T

def process_file(file_path):
    print(f"Processing file: {file_path}")
    base_name = os.path.basename(file_path)
    filename_without_ext = os.path.splitext(base_name)[0]

    # Loads raw coordinate data
    try:
        X, Y, ex, ey = np.loadtxt(file_path, unpack=True)
    except Exception:
        try:
            X, Y, _, _ = np.loadtxt(file_path, unpack=True)
        except Exception:
            try:
                X, Y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)
            except Exception as e:
                print(f"Failed to read file {file_path}: {e}")
                return

    # Rotational correction for experimental data
    if not filename_without_ext.endswith("T_S"):
        min_x = np.min(X)
        idx_min = np.where(X == min_x)[0][0]
        max_x = np.max(X)
        idx_max = np.where(X == max_x)[0][0]

        experimental_vector = [X[idx_max] - X[idx_min], Y[idx_max] - Y[idx_min]]
        unit_x = [1.0, 0.0]
        angle_deg, angle_rad = gu.calculate_angle(experimental_vector, unit_x)
        print(f"Rotational correction angle: {angle_deg:.3f} degrees")
        
        len_x = len(X)
        if angle_deg < 5.0:
            if experimental_vector[1] < 0.0:
                for i in range(len_x - 1):
                    X[i] = +X[i] * np.cos(angle_rad) - Y[i] * np.sin(angle_rad)
                    Y[i] = +X[i] * np.sin(angle_rad) + Y[i] * np.cos(angle_rad)
            else:
                for i in range(len_x - 1):
                    X[i] = +X[i] * np.cos(angle_rad) + Y[i] * np.sin(angle_rad)
                    Y[i] = -X[i] * np.sin(angle_rad) + Y[i] * np.cos(angle_rad)

        norm_factor = (np.max(Y) - np.min(Y)) * 0.5
        scale_ratio = 1.2 / 533
        Xr = (X - np.mean(X)) * scale_ratio
        Yr = (Y - np.mean(Y)) * scale_ratio
        X = Xr
        Y = Yr
    else:
        # Simulation coordinates are already in correct scale
        Xr = X.copy()
        Yr = Y.copy()

    # Calculate velocity and time vector
    N = len(X)
    t = np.linspace(0, (N - 1) / 30, N)
    dt = t[1] - t[0]

    Vx = np.gradient(X, dt)
    Vy = np.gradient(Y, dt)
    V = np.sqrt(Vx**2 + Vy**2)
    mean_V = np.mean(V)

    # FFT frequency analysis for lowpass filtering
    freq = np.fft.fftfreq(N, dt)
    positive_mask = freq > 0
    fourier_freqs = freq[positive_mask]
    magnitude_freqs = np.sqrt(fourier_freqs ** 2)
    fs = max(magnitude_freqs)
    cutoff = fs / 10
    order = 3

    # Apply low-pass Butterworth filter
    filtered_V = lowpass_filter(V, cutoff, fs, order)

    # Detect collisions based on straight paths
    ts, Xs, Ys = straight_walk_detector(t, X, Y, filtered_V)
    cx, cy, time_intervals = detect_collisions(ts, Xs, Ys, dt)

    print(f"Collisions detected: {len(cx)}")
    if len(cx) < 3:
        print("Warning: Insufficient number of collisions detected.")
        return

    mean_cy_threshold = 0.0
    total_height = max(cy) + np.abs(min(cy))

    # Split collisions to fit upper and lower circle boundaries
    upper_x = []
    upper_y = []
    lower_x = []
    lower_y = []
    for i in range(len(cy)):
        if cy[i] > mean_cy_threshold:
            upper_x.append(cx[i])
            upper_y.append(cy[i])
        else:
            lower_x.append(cx[i])
            lower_y.append(cy[i])

    # Fit boundary circles
    upper_center, upper_radius, _, _ = gu.fit_circle_parameters(upper_x, upper_y)
    lower_center, lower_radius, _, _ = gu.fit_circle_parameters(lower_x, lower_y)

    centers_difference = (lower_center[0] - upper_center[0], lower_center[1] - upper_center[1])
    a = (lower_center[1] - upper_center[1]) / 2.0
    gamma = 2.0 * a / (upper_radius + lower_radius)

    R_geom = np.pi / (2 * np.arcsin(np.sqrt(1.0 - (gamma)**2)))
    mean_radius = (upper_radius + lower_radius) / 2.0
    theoretical_height = 5.01 * (1.0 - gamma) / (2.0 * np.arcsin(np.sqrt(1.0 - gamma**2)))
    
    # Scale normalization factors
    norm_factor_y = R_geom / mean_radius
    norm_factor_real_y = theoretical_height / total_height

    # Normalize coordinate trajectories
    cx_normalized = (cx - np.mean(cx)) * norm_factor_y
    cy_normalized = (cy - np.mean(cy)) * norm_factor_y
    x_normalized = (X - np.mean(X)) * norm_factor_y
    y_normalized = (Y - np.mean(Y)) * norm_factor_y

    l1_wall, l2_wall = gu.get_lemon_wall_boundary(x_normalized, y_normalized, mean_radius, a)
    ang_in, ang_out, ang_diff, flight_lengths = gu.calculate_reflection_efficiency(ts, Xs, Ys, l1_wall, l2_wall, a)

    # Compute Poincaré coordinates (arc length and reflection angle)
    flight_lengths_coll = []
    kappa_coll = []
    velocity_coll = []
    theta_list = []
    alpha_list = []
    perimeter_list = []
    num_steps = len(cx_normalized)

    for i in range(1, num_steps - 1):
        c1 = [cx_normalized[i + 1], cy_normalized[i + 1]]
        c2 = [cx_normalized[i], cy_normalized[i]]
        c3 = [cx_normalized[i - 1], cy_normalized[i - 1]]
        xx = cx_normalized[i]
        yy = cy_normalized[i]

        if yy >= np.mean(cy_normalized):
            R_vec = gu.vector_sub(c2, [upper_center[0], upper_center[1]])
            perimeter = np.arccos(xx / (np.sqrt(xx**2 + yy**2))) + np.pi
        else:
            R_vec = gu.vector_sub(c2, [lower_center[0], lower_center[1]])
            perimeter = np.arccos(-xx / (np.sqrt(xx**2 + yy**2)))

        vec = gu.vector_sub(c2, c3)
        vec_ref = gu.vector_sub(c2, c1)
        reflection_angle = gu.calculate_angle_vectors(vec, R_vec)

        if (c2[0] * vec_ref[1] - c2[1] * vec_ref[0]) < 0.0:
            reflection_angle = -reflection_angle

        alpha = gu.calculate_angle_vectors(vec_ref, R_vec)
        flight_lengths_coll.append(np.linalg.norm(vec))
        kappa_coll.append(1.0 / np.linalg.norm(R_vec))
        velocity = np.linalg.norm(vec) / time_intervals[i]
        velocity_coll.append(velocity)
        theta_list.append(reflection_angle)
        alpha_list.append(alpha)
        perimeter_list.append(perimeter)

    # Ensure processed directory exists
    os.makedirs("../../data/processed", exist_ok=True)

    # Save processed coordinate data
    traj_path = f"../../data/processed/{filename_without_ext}_(Traj).dat"
    with open(traj_path, "w") as f:
        for i in range(len(Xr)):
            f.write(f"{Xr[i]:.6f} {Yr[i]:.6f} {x_normalized[i]:.6f} {y_normalized[i]:.6f}\n")

    th_ka_path = f"../../data/processed/{filename_without_ext}_(T_Th_Ka_V).dat"
    mean_V_coll = np.mean(velocity_coll) if len(velocity_coll) > 0 else 1.0
    flight_velocity = flight_lengths / time_intervals
    with open(th_ka_path, "w") as f:
        for i in range(len(kappa_coll)):
            f.write(f"{(time_intervals[i] * mean_V_coll):.6f} {theta_list[i]:.6f} {kappa_coll[i]:.6f} {(flight_velocity[i] / mean_V_coll):.6f}\n")

    per_sin_path = f"../../data/processed/{filename_without_ext}_(Per_SinTheta).dat"
    with open(per_sin_path, "w") as f:
        for i in range(len(perimeter_list)):
            f.write(f"{perimeter_list[i]:.6f} {np.sin(theta_list[i]):.6f}\n")

    col_xy_path = f"../../data/processed/{filename_without_ext}_Colisao(X-Y).dat"
    with open(col_xy_path, "w") as f:
        for i in range(1, len(cx_normalized) - 1):
            f.write(f"{cx_normalized[i]:.6f} {cy_normalized[i]:.6f}\n")

    print(f"Processed output files generated successfully for: {filename_without_ext}")

def main():
    parser = argparse.ArgumentParser(description="Lemon Billiard Collision Detection and Preprocessor")
    parser.add_argument("--file", type=str, help="Specific file name in data/raw/ to process")
    args = parser.parse_args()

    # Change working directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    raw_dir = "../../data/raw"
    if args.file:
        file_path = os.path.join(raw_dir, args.file)
        if os.path.exists(file_path):
            process_file(file_path)
        else:
            print(f"Error: File {file_path} not found.")
    else:
        # Batch processing: processes all .txt files in data/raw/
        files = glob.glob(os.path.join(raw_dir, "*.txt"))
        if not files:
            print(f"No .txt files found in {raw_dir}")
            return
        for f in sorted(files):
            process_file(f)

if __name__ == "__main__":
    main()
