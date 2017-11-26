from uio import Uio

class Pump:

    OUTLET_ADDR_REGS = 0x0000
    OUTLET_RESV_REGS = 0x0004
    OUTLET_SIZE_REGS = 0x0008
    OUTLET_MODE_REGS = 0x000C
    OUTLET_STAT_REGS = 0x000E
    OUTLET_CTRL_REGS = 0x000F

    INTAKE_ADDR_REGS = 0x0010
    INTAKE_RESV_REGS = 0x0014
    INTAKE_SIZE_REGS = 0x0018
    INTAKE_MODE_REGS = 0x001C
    INTAKE_STAT_REGS = 0x001E
    INTAKE_CTRL_REGS = 0x001F

    MODE_IRQ_ENABLE  = 0x03 <<  0
    MODE_AXI_CACHE   = 0x0F <<  4
    MODE_AXI_USER    = 0x01 <<  8
    MODE_AXI_SPEC    = 1    << 14
    MODE_AXI_SAFE    = 1    << 15
    MODE_AXI_ATTR    = MODE_AXI_USER | MODE_AXI_CACHE

    CTRL_RESET       = 0x80
    CTRL_PAUSE       = 0x40
    CTRL_STOP        = 0x20
    CTRL_START       = 0x10
    CTRL_IRQ_ENABLE  = 0x04
    CTRL_FIRST       = 0x02
    CTRL_LAST        = 0x01

    def __init__(self, regs):
        self.regs = regs

    def intake_setup(self, buf_addr, xfer_size):
        self.regs.write_word(Pump.INTAKE_ADDR_REGS, buf_addr          )
        self.regs.write_word(Pump.INTAKE_RESV_REGS, 0x00000000        )
        self.regs.write_word(Pump.INTAKE_SIZE_REGS, xfer_size         )
        self.regs.write_word(Pump.INTAKE_MODE_REGS, Pump.MODE_AXI_ATTR)

    def outlet_setup(self, buf_addr, xfer_size):
        self.regs.write_word(Pump.OUTLET_ADDR_REGS, buf_addr          )
        self.regs.write_word(Pump.OUTLET_RESV_REGS, 0x00000000        )
        self.regs.write_word(Pump.OUTLET_SIZE_REGS, xfer_size         )
        self.regs.write_word(Pump.OUTLET_MODE_REGS, Pump.MODE_AXI_ATTR | Pump.MODE_IRQ_ENABLE)

    def intake_start(self):
        self.regs.write_byte(Pump.INTAKE_CTRL_REGS, Pump.CTRL_START | Pump.CTRL_FIRST | Pump.CTRL_LAST)

    def outlet_start(self):
        self.regs.write_byte(Pump.OUTLET_CTRL_REGS, Pump.CTRL_START | Pump.CTRL_FIRST | Pump.CTRL_LAST | Pump.CTRL_IRQ_ENABLE)

    def intake_clear_status(self):
        self.regs.write_byte(Pump.INTAKE_STAT_REGS, 0x00)
        
    def outlet_clear_status(self):
        self.regs.write_byte(Pump.OUTLET_STAT_REGS, 0x00)
        
    def setup(self, src_addr, dst_addr, xfer_size):
        self.outlet_setup(dst_addr, xfer_size)
        self.intake_setup(src_addr, xfer_size)
    
    def start(self):
        self.outlet_start()
        self.intake_start()

    def clear_status(self):
        self.outlet_clear_status()
        self.intake_clear_status()
        

