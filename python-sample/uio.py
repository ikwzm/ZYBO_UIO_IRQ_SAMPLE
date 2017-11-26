import numpy as np
import mmap
import os

class Uio:
    """A simple uio class"""

    def __init__(self, name, length=0x1000):
        self.name        = name
        self.device_name = '/dev/%s' % self.name
        self.device_file = os.open(self.device_name, os.O_RDWR | os.O_SYNC)
        self.length      = length
        self.memmap      = mmap.mmap(self.device_file,
                                     self.length,
                                     mmap.MAP_SHARED,
                                     mmap.PROT_READ | mmap.PROT_WRITE,
                                     offset=0)
    def irq_on(self):
        os.write(self.device_file, bytes([1, 0, 0, 0]))

    def irq_off(self):
        os.write(self.device_file, bytes([0, 0, 0, 0]))
        
    def wait_irq(self):
        os.read(self.device_file, 4)

    def regs(self, offset=0, length=None):
        if length == None:
            length = self.length
        if offset+length > self.length:
            raise ValueError("region range error")
        return Uio.Regs(self.memmap, offset, length)

    class Regs:
        
        def __init__(self, memmap, offset, length):
            self.memmap     = memmap
            self.offset     = offset
            self.length     = length
            self.word_array = np.frombuffer(self.memmap, np.uint32, self.length>>2, self.offset)
            self.byte_array = np.frombuffer(self.memmap, np.uint8 , self.length>>0, self.offset)
            
        def read_word(self, offset):
            return int(self.word_array[offset>>2])

        def read_byte(self, offset):
            return int(self.byte_array[offset>>0])

        def write_word(self, offset, data):
            self.word_array[offset>>2] = np.uint32(data)

        def write_byte(self, offset, data):
            self.byte_array[offset>>0] = np.uint8(data)

