import numpy as np
import os
from tooppy import solve, get_indices_on_face, visualize_3d_array

def get_fixed(resolution, ndof, coordinates):  # Constrains
    return []

def get_load(resolution, ndof, coordinates):  # Load
    f = np.zeros(ndof)
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([0, 8, 8])), axis=1))
    f[id * 3 + 0] = 1
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([16, 8, 8])), axis=1))
    f[id * 3 + 0] = -1
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([8, 0, 8])), axis=1))
    f[id * 3 + 1] = 1
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([8, 16, 8])), axis=1))
    f[id * 3 + 1] = -1
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([8, 8, 0])), axis=1))
    f[id * 3 + 2] = 1
    id = np.argmin(np.sum(np.square(coordinates.T - np.array([8, 8, 16])), axis=1))
    f[id * 3 + 2] = -1
    return f

# Default input parameters
resolution = [16, 16, 16]
volfrac = 0.02  # volume fraction 0.05
rmin = 1.5  # 1.5 4.5
penal = 3.0
ft = 1  # 0: sens, 1: dens

result = solve(get_fixed,
               get_load,
               resolution,
               volfrac,
               penal,
               rmin,
               ft,
               iterations=20,
            #    intermediate_results_saving_path='./intermediates/'
               )

# Save result
result_saving_path = './output/'
if not os.path.exists(result_saving_path):
    os.makedirs(result_saving_path)
np.save(result_saving_path + 'result_3d.npy', result)

visualize_3d_array(result)