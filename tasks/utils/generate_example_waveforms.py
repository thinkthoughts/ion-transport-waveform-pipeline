import numpy as np

def save_csv(name, t, x):
    data = np.column_stack((t, x))
    header = "time,position"
    np.savetxt(name, data, delimiter=",", header=header, comments="")
    print(f"saved {name}")

T = 20e-6
t = np.linspace(0, T, 500)
x0, x1 = -80e-6, 80e-6

# Linear
x_linear = x0 + (x1 - x0) * (t / T)
save_csv("input_waveform_linear.csv", t, x_linear)

# Minimum jerk
u = t / T
s = 10*u**3 - 15*u**4 + 6*u**5
x_mj = x0 + (x1 - x0) * s
save_csv("input_waveform_minimum_jerk.csv", t, x_mj)

# Bad spike
x_spike = x_linear.copy()
x_spike[200:210] += 10e-6
save_csv("input_waveform_bad_spike.csv", t, x_spike)

# Fast transport
T_fast = 5e-6
t_fast = np.linspace(0, T_fast, 500)
u_fast = t_fast / T_fast
s_fast = 10*u_fast**3 - 15*u_fast**4 + 6*u_fast**5
x_fast = x0 + (x1 - x0) * s_fast
save_csv("input_waveform_fast_transport.csv", t_fast, x_fast)
