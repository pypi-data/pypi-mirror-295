# dutch_flag

`dutch_flag` is a simple Python library that provides a function to sort an array of three distinct values (representing different colors) in linear time using the Dutch National Flag problem algorithm.

## Installation

You can install the package using `pip`:

```bash
pip install dutch_flag
```

## Usage

Once installed, you can use the `sort` function to sort an array of three distinct values. By default, the function sorts an array containing the values 0, 1, and 2, but you can customize the values if needed.

### Example

```python
from dutch_flag import sort

# Example with default values (0 = red, 1 = white, 2 = blue)
arr = [2, 0, 1, 2, 1, 0]
sorted_arr = sort(arr)
print(sorted_arr)  # Output: [0, 0, 1, 1, 2, 2]
```

You can also customize the values that represent the colors:

```python
### Example with custom values (r = 'r', w = 'w', b = 'b')

```python
arr = ['w', 'b', 'r', 'w', 'r', 'b']
sorted_arr = sort(arr, r='r', w='w', b='b')
print(sorted_arr)  # Output: ['r', 'r', 'w', 'w', 'b', 'b']
```

```
### Function Definition

```python
def sort(arr, r=0, w=1, b=2):
    """
    Sorts an array of three distinct values (default: r=0, w=1, b=2) in place.

    Args:
        arr (list): The array to sort.
        r (int, optional): The value representing the 'red' color. Default is 0.
        w (int, optional): The value representing the 'white' color. Default is 1.
        b (int, optional): The value representing the 'blue' color. Default is 2.

    Returns:
        list: The sorted array.
    
    Raises:
        ValueError: If the array contains a value other than r, w, or b.
    """
```

### Edge Cases

- **Empty array**: The function will return an empty array without raising an error.
- **Invalid values**: If the array contains values other than `r`, `w`, or `b`, the function will raise a `ValueError`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
