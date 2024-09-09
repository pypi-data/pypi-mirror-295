"""
Module: transpose2d.py
Description: This module provides a function to transpose a 2D input matrix.

"""
import numpy as np
from typing import List

def transpose2d(input_matrix: List[List[float]]) -> List:
    """
    Perform a transpose operation on a 2D input matrix.

    Parameters
    ----------
    input_matrix : List[List[float]]
        The input matrix that is going to be transposed. It should be a list of lists where each inner list represents a row of the matrix.

    Returns
    -------
    np.ndarray
        The transposed matrix as a NumPy ndarray.

    Examples
    --------
    >>> input_matrix = [[1, 2, 3], [4, 5, 6]]
    >>> transpose2d(input_matrix)
    array([[1, 4],
           [2, 5],
           [3, 6]])
    """
    
    if not input_matrix or any(len(row) != len(input_matrix[0]) for row in input_matrix):
        raise ValueError("Input matrix must be non-empty and rectangular.")

    np_matrix = np.asarray(input_matrix)
    transposed = np.transpose(np_matrix)

    return transposed