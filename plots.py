import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.optimize import curve_fit
import os

def exp_func(x, a, b):
    return a * np.exp(b * x)

lines = []
ks = [2,10]
for k in ks:
    df = pd.read_csv(f"results/{k}/MO.csv")
    x = df["n"].values
    y = df["time"].values

    params, _ = curve_fit(exp_func, x, y, p0=(1e-3, 0.0001))  # initial guess
    a, b = params
    y_fit = exp_func(x, a, b)

    # Compute r squared
    ss_res = np.sum((y - y_fit)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    r2 = 1 - ss_res/ss_tot

    # smooth curve
    x_smooth = np.linspace(min(x), max(x), 200)
    y_smooth = exp_func(x_smooth, a, b)
    lines.append((k, x, y, x_smooth, y_smooth, a, b, r2))

plt.figure(figsize=(10, 6))
for line in lines:
    k, x, y, x_smooth, y_smooth, a, b, r2 = line
    # Plot
    plt.scatter(x, y)
    plt.plot(x_smooth, y_smooth, label=f"(k={k}) Fit: y = {a:.2E} * e^({b:.2E}x)\n$R^2$ = {math.trunc(r2*100)/100}")

plt.xlabel(f"n")
plt.ylabel("Runtime (s)")
plt.title("MO Runtime Growth (kn pigeons, n holes)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# # Save

plt.savefig(f"plots/heuristic/MO.png", dpi=300, bbox_inches="tight")
plt.show()

# used for generating plots combining heuristics
# result_dirs = [2,10]
# for result_dir in result_dirs:
#     heuristics = []
#     for result in os.listdir(f"results/{result_dir}"):
#         df = pd.read_csv(f"results/{result_dir}/{result}")
#         x = df["n"].values
#         y = df["time"].values

#         params, _ = curve_fit(exp_func, x, y, p0=(1e-3, 0.0001))  # initial guess
#         a, b = params
#         y_fit = exp_func(x, a, b)

#         # Compute r squared
#         ss_res = np.sum((y - y_fit)**2)
#         ss_tot = np.sum((y - np.mean(y))**2)
#         r2 = 1 - ss_res/ss_tot

#         # smooth curve
#         x_smooth = np.linspace(min(x), max(x), 200)
#         y_smooth = exp_func(x_smooth, a, b)
#         heuristics.append((result[:-4], x, y, x_smooth, y_smooth, a, b, r2))

#     plt.figure(figsize=(10, 6))
#     for heuristic in heuristics:
#         name, x, y, x_smooth, y_smooth, a, b, r2 = heuristic
#         # Plot
#         plt.scatter(x, y)
#         plt.plot(x_smooth, y_smooth, label=f"{name} Fit: y = {a:.2E} * e^({b:.2E}x)\n$R^2$ = {math.trunc(r2*100)/100}")

#     plt.xlabel("n")
#     plt.ylabel("Runtime (s)")
#     plt.title(f"Runtime Growth ({result_dir}n pigeons, n holes)")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()

#     # # Save
    
#     plt.savefig(f"plots/combined/{result_dir}.png", dpi=300, bbox_inches="tight")
#     plt.show()