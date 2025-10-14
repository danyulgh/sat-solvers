import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from scipy.optimize import curve_fit
import os

def exp_func(x, a, b):
    return a * np.exp(b * x)

result_dirs = [4]
for result_dir in result_dirs:
    for result in os.listdir(f"results/minus/{result_dir}"):
        df = pd.read_csv(f"results/minus/{result_dir}/{result}")
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

        # Plot
        plt.scatter(x, y, color="blue", label="Data")
        plt.plot(x_smooth, y_smooth, color="red",
                label=f"Exponential Fit: y = {a:.2E} * e^({b:.2E}x)\n$R^2$ = {math.trunc(r2*100)/100}")
        plt.xlabel("n (n pigeons, n-4 holes)")
        plt.ylabel("Runtime (s)")
        plt.title("Runtime Growth")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Save
        plt.savefig(f"plots/minus/{result_dir}/{result[:-4]}.png", dpi=300, bbox_inches="tight")
        plt.show()