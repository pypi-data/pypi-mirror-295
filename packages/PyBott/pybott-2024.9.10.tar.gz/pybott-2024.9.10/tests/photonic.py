import numpy as np

import bott

def break_symmetries(M, delta_B, delta_AB):
    N = M.shape[0] // 2
    for i in range(N):
        if i < N // 2:
            delta_AB = -delta_AB
        M[2 * i, 2 * i] = 2 * delta_B + 2 * delta_AB
        M[2 * i + 1, 2 * i + 1] = -2 * delta_B + 2 * delta_AB

    return M

# M = np.load('effective_hamiltonian_light_honeycomb_lattice.npy')
# M = break_symmetries(M, 4, 3.9)
# eigenvalues, eigenvectors = np.linalg.eig(M)
# grid = np.load('honeycomb_grid.npy')

# omega = 7


# eigenvalues, eigenvectors = bott.sorting_eigenvalues(eigenvalues, eigenvectors, True)
# frequencies = -np.real(eigenvalues)/2
# print(frequencies)
# b_pol = bott.bott(grid, eigenvectors, frequencies, omega, pol=True, dagger=True, projector=False, verbose=False, vl=None)

# print(b_pol)
