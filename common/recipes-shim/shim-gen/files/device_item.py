I2C_DRIVER_DIR = "/sys/bus/i2c/drivers/"
GPIO_SHADOW_DIR = "/tmp/gpionames/"
SYS_PLATFORM_DIR = "/sys/devices/platform/"

class DevItem:
    def __init__(self, device_dict):
        if device_dict != None:
            self.address = device_dict.get('addr', -1)
            self.driver_name = device_dict.get('driver', -1)
            if self.address == -1 or self.driver_name == -1:
                self.property = None
            else:
                del device_dict['addr']
                del device_dict['driver']
                self.property = self.get_property(device_dict)
        else:
            self.property = None

    def get_property(self, device_dict):
        proper = {}
        for key, value in device_dict.items():
            proper[key] = f"{I2C_DRIVER_DIR}{self.driver_name}/{self.address}/{value}"
        return proper

class CpldItem:
    def __init__(self, device_dict):
        if device_dict != None:
            self.address = device_dict.get('addr', -1)
            self.driver_name = device_dict.get('driver', -1)
            if self.address == -1 or self.driver_name == -1:
                self.property = None
            else:
                del device_dict['addr']
                del device_dict['driver']
                self.property = self.get_property(device_dict)
        else:
            self.property = None

    def get_property(self, device_dict):
        proper = {}
        for key, value in device_dict.items():
            if key.find('mask') != -1:
                proper[key] = value
            else:
                proper[key] = f"{I2C_DRIVER_DIR}{self.driver_name}/{self.address}/{value}"
        return proper

class GpioItem:
    def __init__(self, device_dict):
        if device_dict != None:
            self.property = self.get_property(device_dict)
        else:
            self.property = None

    def get_property(self, device_dict):
        proper = {}
        for key, value in device_dict.items():
            if key.find('mask') != -1:
                proper[key] = value
            else:
                proper[key] = f"{GPIO_SHADOW_DIR}{value}/value"
        return proper

class PlatItem:
    def __init__(self, device_dict):
        if device_dict != None:
            self.driver_name = device_dict.get('driver', -1)
            if self.driver_name == -1:
                self.property = None
            else:
                del device_dict['driver']
                self.property = self.get_property(device_dict)
        else:
            self.property = None

    def get_property(self, device_dict):
        proper = {}
        for key, value in device_dict.items():
            if key.find('mask') != -1:
                proper[key] = value
            else:
                proper[key] = f"{SYS_PLATFORM_DIR}{self.driver_name}/{value}"
        return proper