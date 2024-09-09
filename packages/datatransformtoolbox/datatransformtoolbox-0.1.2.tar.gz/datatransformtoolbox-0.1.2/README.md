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
pip install datatransformtoolbox
 
with Poetry
poetry add datatransformtoolbox
```
# Usage
Here is a simple example of how to use transpose library:

```sh

import numpy as np
from datatransformtoolbox.transpose import transpose2d


matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transposed_matrix = transpose2d(matrix)
print(transposed_matrix)
# Output: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

```

Another simple example of how to use Time series Windowing library:

```
import numpy as np
from datatransformtoolbox.window import window1

input_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
size = 2
shift = 1
stride = 1

# Call the function
windows = window1d(input_array, size, shift, stride)

# Print the results
print("Generated windows:")
for i, window in enumerate(windows):
    print(f"Window {i+1}: {window}")

# Example output:
#Generated windows:
#Window 1: [1 2]
#Window 2: [2 3]
#Window 3: [3 4]
#Window 4: [4 5]
#Window 5: [5 6]
#Window 6: [6 7]
#Window 7: [7 8]
#Window 8: [8 9]
#Window 9: [ 9 10]
```
Another simple example of how to use Cross-Correlation library:

```
  Examples
    import numpy as np
    from datatransformtoolbox.crosscorrelation import crosscorrelation
    input_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    kernel = np.array([[1, 0], [0, -1]])
    convolution2d(input_matrix, kernel, stride=1)
    array([[ 1.,  2.],
           [ 4.,  5.]])
    """
```
# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Authors
Johnny Lazo johnny.lazoq@gmail.com

