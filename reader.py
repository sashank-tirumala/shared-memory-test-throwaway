import time
from multiprocessing import shared_memory
from multiprocessing.resource_tracker import unregister

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!

if __name__ == "__main__":
    n = np.ones(10000)
    _dummy_array_data = np.zeros(10000)
    shmseg_lidar_frame_idx = shared_memory.SharedMemory(
        create=False, size=4, name="shared_test_memory_idx"
    )
    unregister("/shared_test_memory_idx", "shared_memory")
    unregister("/shared_test_memory_2", "shared_memory")
    unregister("/shared_test_memory_3", "shared_memory")
    start_time = time.time()
    while True:
        # numpy make sure all elements are same
        idx = int.from_bytes(shmseg_lidar_frame_idx.buf[:], byteorder='little')
        name = f"shared_test_memory_{idx + 2}"
        try:
            shmseg_lidar_frame = shared_memory.SharedMemory(
            name=name, create=False
            )
        except:
            continue
        arr = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame.buf)
        all_same = (arr == arr[0]).all()
        print(all_same)