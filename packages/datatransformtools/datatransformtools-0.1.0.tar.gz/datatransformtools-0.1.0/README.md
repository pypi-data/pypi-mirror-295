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
or with Poetry
poetry add data-transformation-library
```
# Usage
Here is a simple example of how to use the library:

```sh

from data_transformation_library.transpose import transpose

matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

transposed_matrix = transpose(matrix)
print(transposed_matrix)
# Output: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]
```

# License
This project is licensed under the MIT License. See the LICENSE file for more details.

# Authors
Johnny Lazo johnny.lazoq@gmail.com

