from smbus2 import SMBus

class INA219_class:
    def __init__(self, _INA219_ADDRESS, _R_shunt, _Current_LSB):
        #-------parameters for configuration---------#
        self.INA219_ADDRESS = _INA219_ADDRESS 
        self.R_shunt = _R_shunt
        self.Current_LSB = _Current_LSB
        
        #--------Registers Addresses--------#
        CONFIG_REG = 0x00
        SHUNT_VOLTAGE_REG = 0X01
        BUS_VOLTAGE_REG = 0x02
        POWER_REG = 0X03
        CURRENT = 0X04
        CALIBRATION_REG = 0x05
        
        #----------------------Configuration registers configurations--------------------------#
        
        #-------bus voltage configuration---------#
        BUS_VOLTAGE_RANGE_16V = 0x00
        BUS_VOLTAGE_RANGE_32V = 0x2000
        
        #-------Shunt voltage only--------#
        SHUNT_GAIN_40MV  = 0x00
        SHUNT_GAIN_80MV  = 0x0800
        SHUNT_GAIN_160MV = 0x1000
        SHUNT_GAIN_320MV = 0x1800
        
        #--------Bus ADC Resolution-------#
        ADC_RESOLUTION_9BITS  = 0x00
        ADC_RESOLUTION_10BITS = 0x80
        ADC_RESOLUTION_11BITS = 0x100
        ADC_RESOLUTION_12BITS = 0x180
        
        #-------ADC resolution + 
    
    def Test_Connection(self):
            
        try:
            with SMBus(1) as bus:
                reg = bus.read_word_data(self.INA219_ADDRESS, 0x00)
                return True
        except Exception as e:
            print("Error:", e)
            return False

    #-----------Read registers values-----------#
    def Read_REG(self, Register):
        with SMBus(1) as bus:
            raw = bus.read_word_data(i2c_addr=self.INA219_ADDRESS, register=Register)
            # Invierte los bytes antes de leer 
            Reg_val = ((raw & 0xFF) << 8) | (raw >> 8)
            return Reg_val
        
    #-----------Write registers values-----------#
    def Write_REG(self, Register, value):
        # Invierte los bytes antes de escribir 
        value_swapped = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF)
        with SMBus(1) as bus:
            bus.write_word_data(self.INA219_ADDRESS, Register, value_swapped)
    
    def Conf(self,
             RST=0X00,
             bus_vol_range=):
        
    
    
    
    
    
    
    
    
    
    
    
    
    
        
        
