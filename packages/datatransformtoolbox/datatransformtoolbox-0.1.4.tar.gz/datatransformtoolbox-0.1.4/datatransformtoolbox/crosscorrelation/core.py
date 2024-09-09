"""
Conversions between inches and 
larger imperial length units
"""


import numpy as np

def convolution2d(input_matrix: np.ndarray, kernel: np.ndarray, stride: int = 1) -> np.ndarray:
    input_height, input_width = input_matrix.shape
    kernel_height, kernel_width = kernel.shape

    output_height = (input_height - kernel_height) // stride + 1
    output_width = (input_width - kernel_width) // stride + 1

    output_matrix = np.zeros((output_height, output_width))

    for i in range(output_height):
        for j in range(output_width):
            sub_matrix = input_matrix[i * stride:i * stride + kernel_height, j * stride:j * stride + kernel_width]
            result = np.sum(sub_matrix * kernel)
            output_matrix[i, j] = result

    return output_matrix