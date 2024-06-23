import time
from multiprocessing import shared_memory
# import _posixshmem
import posix_ipc

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!

if __name__ == "__main__":
    _dummy_array_data = np.zeros(10000)
    n = np.ones(10000)
    i = 0

    try:
        posix_ipc.unlink_semaphore("/write_semaphore")
    except posix_ipc.ExistentialError:
        print("Write Semaphore does not exist")
        pass

    try:
        posix_ipc.unlink_semaphore("/read_semaphore")
    except posix_ipc.ExistentialError:
        print("Read Semaphore does not exist")
        pass

    resource_lock = posix_ipc.Semaphore("/write_semaphore", posix_ipc.O_CREAT)
    read_lock = posix_ipc.Semaphore("/read_semaphore", posix_ipc.O_CREAT)
    read_lock.release()
    resource_lock.release()
    try:
        shmseg_lidar_frame_0 = shared_memory.SharedMemory(
                    create=True, size=_dummy_array_data.nbytes, name="shared_test_memory_2"
                )
    except FileExistsError:
        shared_memory.SharedMemory(
                    create=False, size=_dummy_array_data.nbytes, name="shared_test_memory_2"
                ).unlink()
        shmseg_lidar_frame_0 = shared_memory.SharedMemory(
                    create=True, size=_dummy_array_data.nbytes, name="shared_test_memory_2"
                )
    
    try:
        shmseg_reader = shared_memory.SharedMemory(create=True, size=4, name="reader_count")
    except FileExistsError:
        shared_memory.SharedMemory(create=False, size=4, name="reader_count").unlink()
        shmseg_reader = shared_memory.SharedMemory(create=True, size=4, name="reader_count")

    shmseg_reader.buf[:] = int(0).to_bytes(4, byteorder='little')
    while True:
        resource_lock.acquire()
        shared_memory_array = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=shmseg_lidar_frame_0.buf)
        shared_memory_array[:] = (n * i)[:]
        i = i + 1
        resource_lock.release()
        if i > 10001:
            i = 0