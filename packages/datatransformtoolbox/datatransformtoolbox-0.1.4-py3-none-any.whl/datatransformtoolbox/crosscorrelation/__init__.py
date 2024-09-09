"""
datatransformtoolbox.crosscorrelation
===============
function that has this signature: convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride : int = 1) -> np.ndarray, 
where input_matrix is a 2D Numpy array of real numbers, kernel is a 2D Numpy array of real numbers, and stride is an integer that is greater than 0. 
Function should return a 2D Numpy array of real numbers.
"""
from .api import convolution2d