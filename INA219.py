from smbus2 import SMBus

class INA219:
    #----------------------Configuration registers configurations--------------------------#
    
    #-------bus voltage configuration---------#
    BUS_VOLTAGE_RANGE_16V = 0x00
    BUS_VOLTAGE_RANGE_32V = 0x20003
    
    #-------Shunt voltage only--------#
    SHUNT_GAIN_40MV  = 0x00
    SHUNT_GAIN_80MV  = 0x0800
    SHUNT_GAIN_160MV = 0x1000
    SHUNT_GAIN_320MV = 0x1800
    
    #--------Bus ADC Resolution-------#
    ADC_RESOLUTION_9BITS  = 0x00	# 84 us
    ADC_RESOLUTION_10BITS = 0x80	# 148 us
    ADC_RESOLUTION_11BITS = 0x100	# 276 us
    ADC_RESOLUTION_12BITS = 0x180	# 532 us
    
    #--------ADC resolution + num of samples averaged--------#
    ADC_12BITS_2_SAMPLES	= 0x0480
    ADC_12BITS_4_SAMPLES	= 0x0500
    ADC_12BITS_8_SAMPLES	= 0x0580
    ADC_12BITS_16_SAMPLES	= 0x0600
    ADC_12BITS_32_SAMPLES	= 0x0680
    ADC_12BITS_64_SAMPLES	= 0x0700
    ADC_12BITS_128_SAMPLES	= 0x0780
    
    #-------operating modes-------#
    POWER_DOWN 							= 0x00
    SHUNT_VOLTAGE_TRIGGERED 			= 0x01
    BUS_VOLTAGE_TIGGERED 				= 0x02
    SHUNT_AND_BUS_TRIGGERED 			= 0x03
    ADC_OFF 							= 0x04
    SHUNT_VOLTAGE_CONTINUOUS 			= 0x05
    BUS_VOLTAGE_CONTINUOUS 				= 0x06
    SHUNT_AND_BUS_VOLTAGE_CONTINUOUS 	= 0x07
        
    def __init__(self, _INA219_ADDRESS, _R_shunt, _Current_LSB):
        #-------parameters for configuration---------#
        self.INA219_ADDRESS = _INA219_ADDRESS 
        self.R_shunt = _R_shunt
        self.Current_LSB = _Current_LSB
        
        #--------Registers Addresses--------#
        self.CONFIG_REG = 0x00
        self.SHUNT_VOLTAGE_REG = 0X01
        self.BUS_VOLTAGE_REG = 0x02
        self.POWER_REG = 0X03
        self.CURRENT = 0X04
        self.CALIBRATION_REG = 0x05
    
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
    
    def Conf_INA219(self, Config_Reg):
        Reg_val = (
            Config_Reg.bus_voltage_range |
            Config_Reg.shunt_gain |
            Config_Reg. adc_resolution |
            Config_Reg. mode
        )
        
        self.Write_REG(self.CONFIG_REG, Reg_val)
        
class Conf_Reg_class:
    def __init__(self, bus_voltage_range, shunt_gain, adc_resolution, mode):
        self.bus_voltage_range = bus_voltage_range
        self.shunt_gain = shunt_gain
        self.adc_resolution = adc_resolution
        self.mode = mode
    
    
    
    
    
    
    
    
        
        
