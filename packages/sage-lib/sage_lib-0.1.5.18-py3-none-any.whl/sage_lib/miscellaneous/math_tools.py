import numpy as np

def normalize_matrix_to_doubly_stochastic(matrix: np.ndarray, tol: float = 1e-9, max_iter: int = 1000) -> np.ndarray:
    """
    Normalize a matrix so that each row and column sums to 1 using the Sinkhorn-Knopp algorithm.

    Args:
        matrix (np.ndarray): The input non-negative matrix to be normalized.
        tol (float): Tolerance for convergence.

    Returns:
        np.ndarray: The normalized doubly stochastic matrix.
    """

    # Ensure matrix is non-negative
    if np.any(matrix < 0):
        raise ValueError(" Sinkhorn-Knopp algorithm : Matrix must have non-negative elements for normalization.")

    # Convert the matrix to float for division operations
    mat = matrix.astype(np.float64)

    # Iteratively scale rows and columns
    for _ in range(max_iter):
        # Normalize rows
        mat /= mat.sum(axis=1, keepdims=True)

        # Normalize columns
        mat /= mat.sum(axis=0, keepdims=True)

        # Check for convergence
        if np.all(np.abs(mat.sum(axis=1) - 1) < tol) and np.all(np.abs(mat.sum(axis=0) - 1) < tol):
            break

    return mat
