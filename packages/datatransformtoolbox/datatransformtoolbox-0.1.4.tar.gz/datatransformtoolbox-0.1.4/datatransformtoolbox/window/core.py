"""
Conversions between inches and 
larger imperial length units
"""

import numpy as np
from typing import List, Union

def window1d(input_array: Union[List[float], np.ndarray], size: int, shift: int = 1, stride: int = 1) -> List[np.ndarray]:
    """
    Parameters
    ----------
    input_array: Union[List[float] :
        
    np.ndarray] :
        
    size: int :
        
    shift: int :
         (Default value = 1)
    stride: int :
         (Default value = 1)

    Returns
    -------
    numpy.ndarray
        The time_series as output

    """
    if isinstance(input_array, list):
        input_array = np.array(input_array)

    if size <= 0 or shift <= 0 or stride <= 0:
        raise ValueError("Size, shift, and stride must be positive integers.")
    if len(input_array) < size:
        raise ValueError("Size of the window must be less than or equal to the length of the input array.")

    windows = []
    for start in range(0, len(input_array) - size + 1, shift):
        window = input_array[start:start + size:stride]
        windows.append(window)

    return windows




