import time
from multiprocessing import shared_memory

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!

if __name__ == "__main__":
    shmseg_lidar_frame = None
    _dummy_array_data = np.zeros(10000)
    n = np.ones(10000)
    i = 0
    shmseg_lidar_frame = shared_memory.SharedMemory(
                    create=True, size=_dummy_array_data.nbytes, name="shared_test_memory"
                )
    shared_memory_array = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame.buf)
    time_to_unlink = 10
    start_time = time.time()
    while True:
        shared_memory_array[:] = (n * i)[:]
        i += 1
        if i > 1000:
            i = 0
        if time.time() - start_time > time_to_unlink:
            print("Unlinking shared memory")
            print(shared_memory_array)
            shmseg_lidar_frame.close()
            shmseg_lidar_frame.unlink()
            break
    pass