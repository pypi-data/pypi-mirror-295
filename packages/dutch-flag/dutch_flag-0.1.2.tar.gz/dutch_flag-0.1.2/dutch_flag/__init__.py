def sort(arr, r=0, w=1, b=2):
    low, mid, high = 0, 0, len(arr) - 1
    while mid <= high:
        if arr[mid] == r:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == w:
            mid += 1
        elif arr[mid] == b:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
        else:
            raise ValueError("Invalid color!")
    return arr
