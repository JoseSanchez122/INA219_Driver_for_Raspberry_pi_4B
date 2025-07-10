from INA219 import INA219
from INA219 import INA219_CONFIG

INA219_Device = INA219(
    _INA219_ADDRESS=0x40, # 1000000 (A0+A1=GND)
    _R_shunt=41.2,
    _Current_LSB=60.1e-9
    )

if INA219_Device.Test_Connection():
    print("conected")
else:
    print("disconected")
    
print(f"CONFIG_REG: {bin(INA219_Device.Read_REG(INA219_Device.CONFIG_REG))}")
print(f"CALIBRATION_REG: {INA219_Device.Read_REG(INA219_Device.CALIBRATION_REG)}")

configuration = INA219_CONFIG(
    bus_voltage_range = INA219.BUS_VOLTAGE_RANGE_16V,
    shunt_gain = INA219.SHUNT_GAIN_80MV,
    bus_adc_conf = INA219.BUS_ADC_RES_12BITS,
    shunt_adc_conf = INA219.SHUNT_ADC_RES_12BITS,
    mode = INA219.SHUNT_VOLTAGE_CONTINUOUS,
    Cal_value = 0X409E
)

INA219_Device.CONFIG_INA219(configuration)

print(f"CONFIG_REG: {bin(INA219_Device.Read_REG(INA219_Device.CONFIG_REG))}")
print(f"CALIBRATION_REG: {INA219_Device.Read_REG(INA219_Device.CALIBRATION_REG)}")

print(INA219_Device.Get_Current_uA())






