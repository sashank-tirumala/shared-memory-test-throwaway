import time
from multiprocessing import shared_memory

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!

if __name__ == "__main__":
    n = np.ones(10000)
    _dummy_array_data = np.zeros(10000)
    shmseg_lidar_frame = shared_memory.SharedMemory(
                create=False, size=_dummy_array_data.nbytes, name="shared_test_memory"
            )
    i = 0
    start_time = time.time()
    while True:
        # numpy make sure all elements are same
        arr = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame.buf)
        all_same = (arr == arr[0]).all()
        print(all_same)
        if all_same == False:
            print(arr)
        if time.time() - start_time > 10:
            break
    print(arr)
    pass