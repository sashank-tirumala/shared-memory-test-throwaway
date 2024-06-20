import time
from multiprocessing import shared_memory

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!

if __name__ == "__main__":
    shmseg_lidar_frame = None
    _dummy_array_data = np.zeros(10000)
    n = np.ones(10000)
    i = 0
    shmseg_lidar_idx = shared_memory.SharedMemory(
                    create=True, size=4, name="shared_test_memory_idx"
                )
    while True:
        idx = i % 2
        if idx == 0:
            shmseg_lidar_frame_0 = shared_memory.SharedMemory(
                    create=True, size=_dummy_array_data.nbytes, name="shared_test_memory_2"
                )
            shared_memory_array = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame_0.buf)
            shared_memory_array[:] = (n * i)[:]
            shmseg_lidar_idx.buf[:] = idx.to_bytes(4, byteorder='little')
            try:
                shmseg_lidar_frame_1.unlink()
            except:
                pass
        else:
            shmseg_lidar_frame_1 = shared_memory.SharedMemory(
                    create=True, size=_dummy_array_data.nbytes, name="shared_test_memory_3"
                )
            shared_memory_array = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame_0.buf)
            shared_memory_array[:] = (n * i)[:]
            shmseg_lidar_idx.buf[:] = idx.to_bytes(4, byteorder='little')
            try:
                shmseg_lidar_frame_0.unlink()
            except:
                pass
        i += 1
        if i > 10001:
            i = 0