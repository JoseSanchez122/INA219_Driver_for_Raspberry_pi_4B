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
    
    #--------SHUNT ADC resolution + num of samples averaged--------#
    SHUNT_ADC_RES_9BITS  = 0x00	# 84 us
    SHUNT_ADC_RES_10BITS = 0x08	# 148 us
    SHUNT_ADC_RES_11BITS = 0x10	# 276 us
    SHUNT_ADC_RES_12BITS = 0x18	# 532 us
    SHUNT_ADC_12BITS_2_SAMP   = 0x48
    SHUNT_ADC_12BITS_4_SAMP	= 0x50
    SHUNT_ADC_12BITS_8_SAMP	= 0x58
    SHUNT_ADC_12BITS_16_SAM	= 0x60
    SHUNT_ADC_12BITS_32_SAM	= 0x68
    SHUNT_ADC_12BITS_64_SAMP	= 0x70
    SHUNT_ADC_12BITS_128_SAMP	= 0x78

    
    #--------BUS ADC resolution + num of samples averaged--------#
    BUS_ADC_RES_9BITS  = 0x00	# 84 us
    BUS_ADC_RES_10BITS = 0x80	# 148 us
    BUS_ADC_RES_11BITS = 0x100	# 276 us
    BUS_ADC_RES_12BITS = 0x180	# 532 us
    BUS_ADC_12BITS_2_SAMP   = 0x0480
    BUS_ADC_12BITS_4_SAMP	= 0x0500
    BUS_ADC_12BITS_8_SAMP	= 0x0580
    BUS_ADC_12BITS_16_SAM	= 0x0600
    BUS_ADC_12BITS_32_SAM	= 0x0680
    BUS_ADC_12BITS_64_SAMP	= 0x0700
    BUS_ADC_12BITS_128_SAMP	= 0x0780
    
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
        self.CURRENT_REG = 0X04
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
            
    def Calculate_Cal_value(self, Config_Reg):
        Vshunt_max = 0
        
        if Config_Reg.shunt_gain == INA219.SHUNT_GAIN_40MV:
            Vshunt_max = 0.04
        elif Config_Reg.shunt_gain == INA219.SHUNT_GAIN_80MV:
            Vshunt_max = 0.08
        elif Config_Reg.shunt_gain == INA219.SHUNT_GAIN_160MV:
            Vshunt_max = 0.16
        elif Config_Reg.shunt_gain == INA219.SHUNT_GAIN_320MV:
            Vshunt_max = 0.32
        
    def CONFIG_INA219(self, configuration):
        Reg_val = (
            configuration.bus_voltage_range |
            configuration.shunt_gain |
            configuration.bus_adc_conf |
            configuration.shunt_adc_conf |
            configuration.mode
        )
        
        self.Write_REG(self.CONFIG_REG, Reg_val)
        self.Write_REG(self.CALIBRATION_REG, configuration.Cal_value)
    
    def Get_Raw_Current(self):
        raw_value = self.Read_REG(self.CURRENT_REG)
        uAmp_value = raw_value*self.Current_LSB
        return uAmp_value
        
    def Get_Current_nA(self):
        raw_value = self.Get_Raw_Current()
        uAmp_value = raw_value*1e9
        return uAmp_value
    
    def Get_Current_uA(self):
        raw_value = self.Get_Raw_Current()
        uAmp_value = raw_value*1e6
        return uAmp_value
    
    def Get_Current_mA(self):
        raw_value = self.Get_Raw_Current()
        uAmp_value = raw_value*1e3
        return uAmp_value
    
    def Get_Current_A(self):
        raw_value = self.Get_Raw_Current()
        return raw_value
        
        
class INA219_CONFIG:
    def __init__(self, bus_voltage_range, shunt_gain, bus_adc_conf, shunt_adc_conf, mode, Cal_value):
        self.bus_voltage_range = bus_voltage_range
        self.shunt_gain = shunt_gain
        self.bus_adc_conf = bus_adc_conf
        self.shunt_adc_conf = shunt_adc_conf
        self.mode = mode
        self.Cal_value = Cal_value
        

    
    
    
    
    
    
    
    
        
        
