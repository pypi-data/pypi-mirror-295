"""
This script demonstrates the inherent instability of trapezoidal
differentiation. If the averaging weight, alpha, is exactly 0.5, there will be a
bounded oscillation. If it is less than 0.5, the oscillation will grow with
time.
"""

import numpy as np
import itrm


def dtrapz(x, T):
    alpha = 0.5
    K = len(x)
    x_ext = np.append(x, 3*x[-1] - 3*x[-2] + x[-3])
    Dx = (x_ext[1] - x_ext[0])/T
    Dx_t = np.zeros(K)
    for k in range(K):
        Dx_t[k] = Dx
        Dx = (x_ext[k+1] - x_ext[k])/(T*alpha) - (1 - alpha)/alpha*Dx
    return Dx_t


# Create a time array and sine wave.
t = np.linspace(0, 1, 100000)
T = t[1] - t[0]
w = 2*np.pi*10
x = np.sin(w*t)

# Calculate the true analytical derivative.
dx = w*np.cos(w*t)

# Calculate the numerical derivative.
Dx = dtrapz(x, T)

# Plot the difference.
itrm.iplot(t, (dx - Dx)/(2*w), label="normalized derivative error")
