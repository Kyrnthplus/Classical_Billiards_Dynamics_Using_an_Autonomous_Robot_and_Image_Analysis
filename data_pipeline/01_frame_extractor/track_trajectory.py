import os
import glob
import datetime
import numpy as np
import cv2
import scipy.io as sio

# Global flag to track OpenCV GUI availability
GUI_SUPPORTED = True

def select_initial_point(first_frame):
    global GUI_SUPPORTED
    h, w = first_frame.shape[:2]
    max_disp_size = 800
    scale = 1.0
    if max(h, w) > max_disp_size:
        scale = max_disp_size / max(h, w)
    
    disp_frame = cv2.resize(first_frame, (int(w * scale), int(h * scale)))
    clicked_point = []

    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            orig_x = int(x / scale)
            orig_y = int(y / scale)
            clicked_point.append((orig_x, orig_y))
            try:
                cv2.circle(disp_frame, (x, y), 5, (0, 0, 255), -1)
                cv2.imshow("Click the Robot's LED/Light (Press any key to confirm)", disp_frame)
            except cv2.error:
                pass

    try:
        cv2.namedWindow("Click the Robot's LED/Light (Press any key to confirm)")
        cv2.imshow("Click the Robot's LED/Light (Press any key to confirm)", disp_frame)
        cv2.setMouseCallback("Click the Robot's LED/Light (Press any key to confirm)", mouse_callback)
        
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        if len(clicked_point) > 0:
            return clicked_point[-1]
        else:
            return (420, 420)
    except cv2.error:
        GUI_SUPPORTED = False
        print("\n[WARNING] OpenCV GUI is not supported by your current package (headless version).")
        print("To enable interactive point selection, please reinstall OpenCV with GUI support:")
        print("  pip uninstall -y opencv-python-headless")
        print("  pip install opencv-python")
        print("\nFallback: Enter the starting coordinate manually.")
        try:
            x_in = input("Enter X coordinate (default 420): ").strip()
            y_in = input("Enter Y coordinate (default 420): ").strip()
            x = int(x_in) if x_in else 420
            y = int(y_in) if y_in else 420
            return (x, y)
        except Exception:
            return (420, 420)

def main():
    global GUI_SUPPORTED
    script_dir = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.normpath(os.path.join(script_dir, "../../data/raw/video/images"))
    
    frame_files = sorted(glob.glob(os.path.join(images_dir, "*.jpg")))
    N = len(frame_files)
    
    if N == 0:
        print(f"Error: No frames found in {images_dir} matching '*.jpg'.")
        print("Please extract frames first using option 1.")
        return
    
    print(f"Loaded {N} frames.")
    
    first_frame_path = frame_files[0]
    first_frame = cv2.imread(first_frame_path)
    if first_frame is None:
        print(f"Error: Could not read first frame: {first_frame_path}")
        return
    
    xm, ym = select_initial_point(first_frame)
    print(f"Initial tracking coordinates: X = {xm}, Y = {ym}")
    
    window_radius = 50  
    sb = 20            
    
    xpos = np.zeros(N)
    ypos = np.zeros(N)
    xerro = np.zeros(N)
    yerro = np.zeros(N)
    
    if GUI_SUPPORTED:
        try:
            cv2.namedWindow("Trajectory Tracking (Press 'q' to abort)", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Trajectory Tracking (Press 'q' to abort)", 800, 600)
        except cv2.error:
            GUI_SUPPORTED = False
    
    for ii, frame_path in enumerate(frame_files):
        frame = cv2.imread(frame_path)
        if frame is None:
            continue
            
        if len(frame.shape) == 3:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            gray = frame
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
            
        height, width = gray.shape
        
        x_min = max(0, int(xm - window_radius))
        x_max = min(width, int(xm + window_radius))
        y_min = max(0, int(ym - window_radius))
        y_max = min(height, int(ym + window_radius))
        
        sub_img = gray[y_min:y_max, x_min:x_max]
        
        if sub_img.size > 0:
            max_val = np.max(sub_img)
            y_indices, x_indices = np.where(sub_img >= (max_val - sb))
            
            x_global = x_indices + x_min
            y_global = y_indices + y_min
            
            xm_mean = np.mean(x_global)
            ym_mean = np.mean(y_global)
            x_std = np.std(x_global)
            y_std = np.std(y_global)
            
            valid = (x_global >= (xm_mean - x_std)) & (x_global <= (xm_mean + x_std)) & \
                    (y_global >= (ym_mean - y_std)) & (y_global <= (ym_mean + y_std))
            
            x_filtered = x_global[valid]
            y_filtered = y_global[valid]
            
            if len(x_filtered) > 0:
                xm = np.mean(x_filtered)
                ym = np.mean(y_filtered)
                x_err = np.std(x_filtered)
                y_err = np.std(y_filtered)
            else:
                xm, ym = xm_mean, ym_mean
                x_err, y_err = x_std, y_std
        else:
            x_err, y_err = 0.0, 0.0
            
        xpos[ii] = xm
        ypos[ii] = ym
        xerro[ii] = x_err
        yerro[ii] = y_err
        
        if ii % 100 == 0 or ii == N - 1:
            print(f"Processing frame {ii + 1}/{N} - Coordinates: ({xm:.2f}, {ym:.2f})")
            
        if GUI_SUPPORTED:
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
            cv2.circle(frame, (int(xm), int(ym)), 4, (0, 0, 255), -1)
            
            try:
                cv2.imshow("Trajectory Tracking (Press 'q' to abort)", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("Tracking aborted by user.")
                    break
            except cv2.error:
                GUI_SUPPORTED = False
            
    if GUI_SUPPORTED:
        try:
            cv2.destroyAllWindows()
        except cv2.error:
            pass
    
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    
    output_dir = os.path.normpath(os.path.join(script_dir, "../../data/raw"))
    txt_path = os.path.join(output_dir, f"trajectory-{timestamp}.txt")
    mat_path = os.path.join(output_dir, f"trajectory-{timestamp}.mat")
    
    data = np.column_stack((xpos, ypos, xerro, yerro))
    
    np.savetxt(txt_path, data, fmt="%.6f")
    sio.savemat(mat_path, {"data": data})
    
    print(f"\nTracking complete!")
    print(f"Results saved to:")
    print(f" - TXT: {txt_path}")
    print(f" - MAT: {mat_path}")

if __name__ == "__main__":
    main()
