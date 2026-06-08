import numpy as np
from scipy.optimize import curve_fit

def fit_linear_function(x1, y1, x2, y2):
    # Calculates slope and intercept for a 1D linear fit
    m = (y2 - y1) / (x2 - x1)
    c = y1 - m * x1
    return lambda x: m * x + c

def cross_product(v1, v2):
    if len(v1) != 2 or len(v2) != 2:
        raise ValueError("Vectors must have two components (x, y)")
    return v1[0] * v2[1] - v1[1] * v2[0]

def calculate_magnitude(vector):
    return np.linalg.norm(vector)

def calculate_unit_vector(vector):
    magnitude = np.linalg.norm(vector)
    if magnitude == 0:
        return np.array([0.0, 0.0])
    return vector / magnitude

def calculate_angle(v_dir, p_dir):
    dot_product = np.dot(v_dir, p_dir)
    norm_v = np.linalg.norm(v_dir)
    norm_p = np.linalg.norm(p_dir)
    if norm_v == 0 or norm_p == 0:
        return 0.0, 0.0
    cos_theta = dot_product / (norm_v * norm_p)
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    angle_radians = np.arccos(cos_theta)
    angle_degrees = np.degrees(angle_radians)
    return angle_degrees, angle_radians

def calculate_angle_vectors(a, b):
    m = len(a)
    prod = 0.0
    for i in range(m):
        prod = prod + a[i] * b[i]
    mod = np.linalg.norm(a) * np.linalg.norm(b)
    if mod == 0:
        return 0.0
    val = prod / mod
    val = np.clip(val, -1.0, 1.0)
    return np.arccos(val)

def get_lemon_wall_boundary(x, y, r, a):
    # Generates boundary coordinates for the lemon billiard shape
    theta = np.linspace(0, 2*np.pi, 1000)
    x1 = r*np.cos(theta)
    y1 = r*np.sin(theta) + a
    x2 = r*np.cos(theta)
    y2 = r*np.sin(theta) - a
    return [x1, y1], [x2, y2]

def vector_add(v1, v2):
    m = len(v1)
    return [v1[i] + v2[i] for i in range(m)]

def vector_sub(v1, v2):
    m = len(v1)
    return [v1[i] - v2[i] for i in range(m)]

def vector_norm(v):
    return np.linalg.norm(v)

def vector_dot(v1, v2):
    return np.dot(v1, v2)

def vector_scale(k, v1):
    return [k * x for x in v1]

def vector_project(v1, v2):
    m = len(v1)
    dot_val = vector_dot(v1, v2)
    norm_val = vector_norm(v1)
    if norm_val == 0:
        return [0.0] * m
    div = (dot_val / norm_val ** 2)
    u = []
    m = m - 1
    while m >= 0:
        w = div * v1[m]
        u.insert(0, w)
        m = m - 1
    return u

def circle_equation(x, h, k, r):
    return (x[0] - h) ** 2 + (x[1] - k) ** 2 - r ** 2

def fit_circle_parameters(points_x, points_y):
    x_data = np.array(points_x)
    y_data = np.array(points_y)
    initial_estimate = (0.0, 0.0, 1.0)
    optimal_params, covariance = curve_fit(
        circle_equation, 
        (x_data, y_data), 
        np.zeros(len(points_x)), 
        p0=initial_estimate,
        maxfev=10000
    )
    h, k, r = optimal_params
    errors = np.sqrt(np.diag(covariance))
    h_error, k_error, r_error = errors[0], errors[1], errors[2]
    return (h, k), r, (h_error, k_error), r_error

def calculate_reflection_efficiency(ts, xs, ys, l1, l2, initial_a):
    a = initial_a
    tdiff = np.diff(ts)
    cont0 = 0
    ang_in = []
    ang_out = []
    ang_diff = []
    flight_lengths = []
    for i in range(len(ts)-1):
        x0, y0 = xs[cont0], ys[cont0]
        if tdiff[i] > 5/30:
            x1, y1 = xs[i], ys[i]
            vec = [x1 - x0, y1 - y0]
            vec2 = [x0 - x1, y0 - y1]

            if y1 >= 0:
                a = -a
                diff1 = list(np.sqrt((l2[0] - x1)**2 + (l2[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l2[0][aa], l2[1][aa]]

                if y0 >= 0:
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
            if y1 < 0:
                diff1 = list(np.sqrt((l1[0] - x1)**2 + (l1[1] - y1)**2))
                aa = diff1.index(np.min(diff1))
                lvec = [l1[0][aa], l1[1][aa]]

                if y0 < 0:
                    diff2 = list(np.sqrt((l1[0] - x0)**2 + (l1[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]
                else:
                    diff2 = list(np.sqrt((l2[0] - x0)**2 + (l2[1] - y0)**2))
                    aa2 = diff2.index(np.min(diff2))
                    lvec2 = [l1[0][aa2], l1[1][aa2]]

            inc = calculate_angle_vectors(lvec, vec)
            ref = calculate_angle_vectors(lvec2, vec2)

            if inc > ref:
                dif = ref / inc
            else:
                dif = inc / ref

            ang_in.append(inc)
            ang_out.append(ref)
            ang_diff.append(dif)
            flight_lengths.append(np.linalg.norm(vec))
            cont0 = i + 1

    return np.array(ang_in), np.array(ang_out), np.array(ang_diff), np.array(flight_lengths)
