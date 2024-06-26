import time
from multiprocessing import shared_memory
from multiprocessing.resource_tracker import unregister
import posix_ipc
import time

import numpy as np  # not heavily used in v1.0 but future version will require it for sure!
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--reader', type=int, help='Reader number')
    args = parser.parse_args()
    reader = args.reader
    n = np.ones(10000)
    _dummy_array_data = np.zeros(10000)
    arr_size = _dummy_array_data.nbytes

    resource_lock = posix_ipc.Semaphore("/write_semaphore")
    read_lock = posix_ipc.Semaphore("/read_semaphore")
    shmseg_reader = shared_memory.SharedMemory(create=False, size=4, name="reader_count")
    val = shared_memory.SharedMemory(create=False, size=arr_size, name="shared_test_memory_2")
    unregister("/shared_test_memory_2", "shared_memory")
    unregister("/reader_count", "shared_memory")
    start_time = time.time()

    while True:
        read_lock.acquire()
        temp = int.from_bytes(shmseg_reader.buf[:4], byteorder='little')
        new_val = temp+1
        print(new_val)
        shmseg_reader.buf[:4] = new_val.to_bytes(4, byteorder='little')
        if new_val == 1:
            resource_lock.acquire()
        read_lock.release()
        arr = np.ndarray(_dummy_array_data.shape, dtype=np.float32, buffer=val.buf)
        all_same = np.all((arr == arr[0]))
        print(arr)
        print(all_same)
        if all_same == False:
            raise ValueError("Data is not the same")
        read_lock.acquire()
        temp = int.from_bytes(shmseg_reader.buf[:4], byteorder='little')
        new_val = temp-1
        shmseg_reader.buf[:4] = new_val.to_bytes(4, byteorder='little')
        if new_val == 0:
            resource_lock.release()
        read_lock.release()
        if time.time() - start_time > 10:
            break
    print(f"Reader {args.reader} completed successfully, no data corruption detected.")