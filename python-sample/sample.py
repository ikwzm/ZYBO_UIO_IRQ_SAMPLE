from udmabuf import Udmabuf
from uio     import Uio
from pump    import Pump
import numpy as np
import time

if __name__ == '__main__':
    uio0       = Uio('uio0')
    pump       = Pump(uio0.regs())
    udmabuf4   = Udmabuf('udmabuf4')
    udmabuf5   = Udmabuf('udmabuf5')
    test_dtype = np.uint8
    test_size  = min(int(udmabuf4.buf_size/(np.dtype(test_dtype).itemsize)),
                     int(udmabuf5.buf_size/(np.dtype(test_dtype).itemsize)))

    udmabuf4_array = udmabuf4.memmap(dtype=test_dtype, shape=(test_size))
    udmabuf5_array = udmabuf5.memmap(dtype=test_dtype, shape=(test_size))

    udmabuf4_array[:] = np.random.randint(0,255,(test_size))
    udmabuf5_array[:] = np.random.randint(0,255,(test_size))

    total_time = 0
    total_size = 0
    count      = 0
    for i in range (0,9):
        start = time.time()
        pump.setup(udmabuf4.phys_addr, udmabuf5.phys_addr, test_size)
        uio0.irq_on()
        pump.start()
        uio0.wait_irq()
        pump.clear_status
        elapsed_time = time.time() - start
        total_time   = total_time  + elapsed_time
        total_size   = total_size  + test_size
        count        = count       + 1
        print ("elapsed_time:{0}".format(round(elapsed_time*1000.0,3)) + "[msec]")

    print ("average_time:{0}".format(round((total_time/count)*1000.0,3)) + "[msec]")
    print ("thougput    :{0}".format(round(((total_size/total_time)/(1000*1000)),3)) + "[MByte/sec]")

    if np.array_equal(udmabuf4_array, udmabuf5_array):
         print("udmabuf4 == udmabuf5 : OK")
    else:
         print("udmabuf4 == udmabuf5 : NG")
    
