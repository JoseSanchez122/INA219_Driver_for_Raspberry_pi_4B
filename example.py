from INA219 import INA219
from INA219 import Conf_Reg_class

INA219_Device = INA219(
    _INA219_ADDRESS=0x40, # 1000000 (A0+A1=GND)
    _R_shunt=41.2,
    _Current_LSB=16542
    )

if INA219_Device.Test_Connection():
    print("conected")
else:
    print("disconected")
    
print(f"CONFIG_REG: {bin(INA219_Device.Read_REG(INA219_Device.CONFIG_REG))}")

conf_Reg = Conf_Reg_class(
    bus_voltage_range = INA219.BUS_VOLTAGE_RANGE_32V,
    shunt_gain = INA219.SHUNT_GAIN_80MV,
    adc_resolution = INA219.ADC_RESOLUTION_12BITS,
    mode = INA219.SHUNT_VOLTAGE_CONTINUOUS
)

INA219_Device.Conf_INA219(Config_Reg=conf_Reg)

print(f"CONFIG_REG: {bin(INA219_Device.Read_REG(INA219_Device.CONFIG_REG))}")




