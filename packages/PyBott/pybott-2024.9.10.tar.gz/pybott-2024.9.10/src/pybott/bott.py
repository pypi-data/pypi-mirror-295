"""Code to compute the Bott index following the definition given by
T. A. Loring and M. B. Hastings in
https://iopscience.iop.org/article/10.1209/0295-5075/92/67004/meta
"""
import numpy as np

def compute_uv(lattice, eigenvectors, pos_omega, orb):
    """
    Compute Vx and Vy matrices.

    Parameters:
        lattice (ndarray): Array of shape (N_sites, 2) containing the coordinates
    of the lattice sites.
        eigenvectors (ndarray): Array of shape (orb * N_sites, orb * N_sites) containing
    the eigenvectors.
        pos_omega (int): position of the frequency in the ordered list of frequences.
        orb (int): number of orbitals.

    Returns:
        u_proj (ndarray): Array of shape (orb * N_sites, orb * N_sites) representing
                     the projected position operator on x.
        v_proj (ndarray): Array of shape (orb * N_sites, orb * N_sites) representing
                     the projected position operator on y.
    """
    n_sites = lattice.shape[0]
    x_lattice = lattice[:n_sites, 0]
    y_lattice = lattice[:n_sites, 1]
    lx, ly = np.max(x_lattice) - np.min(x_lattice), np.max(y_lattice) - np.min(
        y_lattice
    )
    u_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)
    v_proj = np.zeros((orb * n_sites, orb * n_sites), dtype=complex)

    x_lattice = np.repeat(x_lattice, orb)
    y_lattice = np.repeat(y_lattice, orb)

    w_stack = np.column_stack([eigenvectors[:, i] for i in range(pos_omega)])

    phase_x = np.diag(np.exp(2 * np.pi * 1j * x_lattice / lx))
    phase_y = np.diag(np.exp(2 * np.pi * 1j * y_lattice / ly))
    u_proj = np.conj(w_stack.T) @ phase_x @ w_stack
    v_proj = np.conj(w_stack.T) @ phase_y @ w_stack

    return u_proj, v_proj


def sorting_eigenvalues(eigv, eigvec, rev=False):
    """Sorting eigenvalues and eigenvectors accordingly"""
    if rev:
        eigv_ind = np.argsort(eigv)[::-1]
    else:
        eigv_ind = np.argsort(eigv)
    return eigv[eigv_ind], eigvec[:, eigv_ind]


def bott(
    lattice,
    eigvec,
    frequencies,
    omega,
    orb=1,
    dagger=False,
):
    """Compute the Bott index.

    Parameters:

    lattice (ndarray): Array of shape (N_sites, 2) containing the
    coordinates of the lattice sites.

    eigvec (ndarray): Array of shape (2 * N_sites, 2 * N_sites)
    containing the eigenvectors.

    frequencies (ndarray): Array of shape (2 * N_sites,) containing
    the frequencies.

    omega (float): Value of omega for computing the Bott index.

    pol (bool): indicates if polarisation have to be taken into account.

    dagger (bool): two methods to cumpute Bott index exist, one with
        dagger of the projected position operator, the other by
        computing the inverse of the said operator.
        

    Returns:
        float: The Bott index value.

    """
    k = np.searchsorted(frequencies, omega)
    if k == 0:
        return 0

    u_proj, v_proj = compute_uv(lattice, eigvec, k, orb)

    if dagger:
        ebott, _ = np.linalg.eig(u_proj @ v_proj @ np.conj(u_proj.T) @ np.conj(v_proj.T))
    else:
        ebott, _ = np.linalg.eig(u_proj @ v_proj @ np.linalg.inv(u_proj) @ np.linalg.inv(v_proj))
    cbott = np.sum(np.log(ebott)) / (2 * np.pi)

    return np.imag(cbott)


def all_bott(
    lattice,
    eigvec,
    frequencies,
    orb=1,
    dagger=False,
    stop=0,
):
    """Compute Bott Index for all the frequencies"""
    n_sites = np.size(lattice, 0)

    u_proj, v_proj = compute_uv(lattice, eigvec, n_sites, orb)

    botts = {}

    if stop != 0:
        n_sites = stop

    for k in range(n_sites):
        uk, vk = u_proj[0:k, 0:k], v_proj[0:k, 0:k]
        if dagger:
            ebott, _ = np.linalg.eig(uk @ vk @ np.conj(uk.T) @ np.conj(vk.T))
        else:
            ebott, _ = np.linalg.eig(
                uk @ vk @ np.linalg.inv(uk) @ np.linalg.inv(vk)
            )
        bott_value = np.imag(np.sum(np.log(ebott))) / (2 * np.pi)
        botts[frequencies[k]] = bott_value

    return botts
