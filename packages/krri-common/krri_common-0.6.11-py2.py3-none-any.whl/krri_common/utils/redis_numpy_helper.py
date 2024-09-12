import struct
from timeit import timeit

import numpy as np


class RedisNumpyHelper:
    @staticmethod
    def to_redis_bytes(numpy_array: np.ndarray) -> bytes:
        """
        convert numpy array to redis bytes string
        :param numpy_array: numpy array
        :return: redis bytes
        """
        h, w = numpy_array.shape
        shape = struct.pack('>II', h, w)
        redis_bytes = shape + numpy_array.tobytes(order='F')
        return redis_bytes

    @staticmethod
    def from_redis_bytes(redis_bytes: bytes) -> np.ndarray:
        """
        convert redis bytes string to numpy array
        :param redis_bytes: redis bytes
        :return: numpy array
        """
        h, w = struct.unpack('>II', redis_bytes[:8])
        # Add slicing here, or else the array would differ from the original
        numpy_array = np.frombuffer(redis_bytes[8:]).reshape(h, w)
        return numpy_array


if __name__ == '__main__':
    fake_data = np.random.rand(2500, 10000)
    fake_data_bytes = RedisNumpyHelper.to_redis_bytes(fake_data)
    fake_data_bytes2 = fake_data.tobytes()
    print(timeit('RedisNumpyHelper.to_redis_bytes(fake_data)', globals=globals(), number=10))
    print(timeit('RedisNumpyHelper.from_redis_bytes(fake_data_bytes)',
                 globals=globals(), number=10))
    print(timeit('fake_data.tobytes()', globals=globals(), number=10))
    print(timeit('fake_data.tolist()', globals=globals(), number=10))
