import time
import numpy as np
import matplotlib.pyplot as plt
import inu
import r3f
import itrm


def get_path(T):
    # Define time.
    t_dur = 3600.0
    K = round(t_dur/T) + 1
    t = np.arange(K)*T

    # Define a figure eight.
    R = 0.016 # lat-long radius (rad)
    theta = np.linspace(0, 2*np.pi, K)
    lat = (R/4)*np.sin(2*theta)
    lon = R*(np.cos(theta) - 1)
    a = 0.06
    hae = 50.0*(1 + a - np.cos(theta) - a*np.cos(20*theta))
    llh_t = np.array((lat, lon, hae))

    vne_t = inu.llh_to_vne(llh_t, T)
    grav_t = inu.somigliana(llh_t)
    rpy_t = inu.vne_to_rpy(vne_t, grav_t[2, :], T)

    return t, llh_t, vne_t, rpy_t


def est(fbbi_t, wbbi_t, z_t, # specific forces, rotation rates, GPS positions
        llh, vne, Cnb, # initial states
        Qd, R, K, T): # samples and sampling period

    # Define the constant or semi-constant matrices.
    I = np.eye(9) # identity matrix
    H = np.zeros((3, 9)) # measurement matrix
    H[:3, :3] = np.eye(3)
    G = np.zeros((9, 6)) # noise mapping matrix

    # Initialize the state covariance matrix.
    Ph = np.eye(9) # "P hat"

    # Allocate storage.
    hllh_t = np.zeros((3, K))
    hvne_t = np.zeros((3, K))
    hrpy_t = np.zeros((3, K))

    tic = time.perf_counter()
    for k in range(K):
        # Inputs
        fbbi = fbbi_t[:, k] # specific forces (m/s^2)
        wbbi = wbbi_t[:, k] # rotation rates (rad/s)
        z = z_t[:, k] # GPS position (rad, rad, m)

        # Update
        S = H @ Ph @ H.T + R # innovation covariance (3, 3)
        Si = np.linalg.inv(S) # inverse (3, 3)
        Kg = Ph @ H.T @ Si # Kalman gain (9, 3)
        Ph -= Kg @ H @ Ph # update to state covariance (9, 9)
        r = z - llh # innovation (3,)
        dx = Kg @ r # changes to states (9,)
        llh += dx[:3] # add change in position
        vne += dx[3:6] # add change in velocity
        # matrix exponential of skew-symmetric matrix
        Psi = inu.rodrigues_rotation(dx[6:])
        Cnb = Psi.T @ Cnb

        # Save results.
        hllh_t[:, k] = llh
        hvne_t[:, k] = vne
        hrpy_t[:, k] = inu.dcm_to_rpy(Cnb.T)

        # Get the Jacobian and propagate the state covariance.
        F = inu.jacobian(fbbi, llh, vne, Cnb)
        Phi = I + (F*T)@(I + (F*T/2)) # 2nd-order expm(F T)
        G[3:6, 0:3] = Cnb
        G[6:9, 3:6] = Cnb
        Ph = Phi @ Ph @ Phi.T + G @ Qd @ G.T

        # Get the state derivatives.
        Dllh, Dvne, wbbn = inu.mech_step(fbbi, wbbi, llh, vne, Cnb)

        # Integrate (forward Euler).
        llh += Dllh * T # change applies linearly
        vne += Dvne * T # change applies linearly
        Cnb[:, :] = Cnb @ inu.rodrigues_rotation(wbbn * T)
        inu.orthonormalize_dcm(Cnb)

        # Update progress bar.
        inu.progress(k, K, tic)

    return hllh_t, hvne_t, hrpy_t


# Constants
T = 0.1
qf = T * (1e-6)**2 * np.eye(3) # accelerometer noise covariance
qw = T * (1e-8)**2 * np.eye(3) # gyroscope noise covariance
Z = np.zeros((3, 3))
Qd = np.block([[qf, Z], [Z, qw]])
R = np.diag([1.5e-5, 1.5e-5, 200.0])**2 # lat, lon, hae

# Get a fake path.
t, llh_t, vne_t, rpy_t = get_path(T)

# Get the "GPS" measurements by adding noise to the true position.
K = llh_t.shape[1]
z_t = llh_t + np.linalg.cholesky(R) @ np.random.randn(3, K)

# Inverse mechanize paths to get sensor values and add noise.
print("Inverse mechanization ...")
fbbi_t, wbbi_t = inu.inv_mech(llh_t, rpy_t, T)
fbbi_t += np.linalg.cholesky(qf) @ np.random.randn(3, K)
wbbi_t += np.linalg.cholesky(qw) @ np.random.randn(3, K)

# Run the Extended Kalman Filter (EKF).
print("Extended Kalman Filter ...")
llh = llh_t[:, 0].copy()
vne = vne_t[:, 0].copy()
Cnb = inu.rpy_to_dcm(rpy_t[:, 0].copy()).T
hllh_t, hvne_t, hrpy_t = est(fbbi_t, wbbi_t, z_t, llh, vne, Cnb, Qd, R, K, T)

# Convert the estimate and the truth to curvilinear coordinates.
[xc, yc, zc] = r3f.geodetic_to_curvilinear(llh_t)
[hxc, hyc, hzc] = r3f.geodetic_to_curvilinear(hllh_t)

# Show the comparison of true path and estimate.
itrm.plot([yc/1e3, hyc/1e3], [xc/1e3, hxc/1e3],
    ea=True, label=["true", "est"])

# Show the errors.
er = np.array([xc - hxc, yc - hyc, zc - hzc])
itrm.iplot(t/60, er, label="curvilinear errors (m)")

print(f"STD:", np.std(er, axis=1))

er = rpy_t - hrpy_t
itrm.iplot(t/60, er, label="attitude errors (rad)")

itrm.iplot(t/60, [rpy_t[0], hrpy_t[0]], label="true and est roll (rad)")
itrm.iplot(t/60, [rpy_t[1], hrpy_t[1]], label="true and est pitch (rad)")
itrm.iplot(t/60, [rpy_t[2], hrpy_t[2]], label="true and est yaw (rad)")
