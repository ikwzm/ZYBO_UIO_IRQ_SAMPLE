import numpy as np

class Udmabuf:
    """A simple udmabuf class"""

    def __init__(self, name):
        self.name        = name
        self.device_name = '/dev/%s'               % self.name
        self.class_path  = '/sys/class/udmabuf/%s' % self.name
        for line in open(self.class_path + '/size'):
            self.buf_size = int(line)
            break
        for line in open(self.class_path + '/phys_addr'):
            self.phys_addr = int(line, 16)
            break

    def memmap(self, dtype, shape):
        self.item_size = np.dtype(dtype).itemsize
        self.array     = np.memmap(self.device_name, dtype=dtype, mode='r+', shape=shape)
        return self.array

