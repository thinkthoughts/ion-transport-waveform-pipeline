import numpy as np
import pandas as pd

def save_csv(name, t, x):
    df = pd.DataFrame({"time": t, "position": x})
    df.to_csv(name, index=False)
    print(f"saved {name}")

# base parameters
T = 20e-6
t = np.linspace(0, T, 500)
x0, x1 = -80e-6, 80e-6

# ----------------------------
# 1. Linear (bad)
# ----------------------------
x_linear = x0 + (x1 - x0) * (t / T)
save_csv("input_waveform_linear.csv", t, x_linear)

# ----------------------------
# 2. Minimum jerk (good)
# ----------------------------
u = t / T
s = 10*u**3 - 15*u**4 + 6*u**5
x_mj = x0 + (x1 - x0) * s
save_csv("input_waveform_minimum_jerk.csv", t, x_mj)

# ----------------------------
# 3. Bad spike (debug case)
# ----------------------------
x_spike = x_linear.copy()
x_spike[200:210] += 10e-6  # inject discontinuity
save_csv("input_waveform_bad_spike.csv", t, x_spike)

# ----------------------------
# 4. Fast transport (tradeoff)
# ----------------------------
T_fast = 5e-6
t_fast = np.linspace(0, T_fast, 500)
u_fast = t_fast / T_fast
s_fast = 10*u_fast**3 - 15*u_fast**4 + 6*u_fast**5
x_fast = x0 + (x1 - x0) * s_fast
save_csv("input_waveform_fast_transport.csv", t_fast, x_fast)
