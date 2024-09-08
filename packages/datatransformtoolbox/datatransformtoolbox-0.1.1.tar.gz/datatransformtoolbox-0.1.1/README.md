# Data Transformation Library

The Data Transformation Library is a Python library that provides a set of functions for common data transformation tasks. It contains simple function to make their every day coding easier. 

## Features

1. **Transpose a Matrix (2D Tensor)**
   - Function: `transpose2d`
   - Transposes the axes of a 2D list.

2. **Time Series Windowing**
   - Function: `window1d`
   - Creates sliding windows over a 1D list or NumPy array.

3. **2D Convolution**
   - Function: `convolution2d`
   - Applies 2D cross-correlation to an input matrix using a kernel.

## Installation

You can install the package using pip:

```sh
pip install data-transformation-library
 
with Poetry
poetry add datatransformtools
```
# Usage
Here is a simple example of how to use transpose library:

```sh

import numpy as np
from datatransformationtools.transpose import transpose2d


matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transposed_matrix = transpose2d(matrix)
print(transposed_matrix)
# Output: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

```

Another simple example of how to use time serie nwindowing library:

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Authors
Johnny Lazo johnny.lazoq@gmail.com

