from enum import IntEnum, Enum
import device_item

class SensorTypeId(IntEnum):
    DEFAULT = 0
    FAN = 1
    THERMAL = 2
    VOLTAGE = 3
    POWERCTRL = 4
    POWERSUPPLY = 5

class SensorTypeName(Enum):
    DEFAULT = 'unsupport'
    FAN = 'fan'
    THERMAL = 'thermal'
    VOLTAGE = 'voltage'
    POWERCTRL = 'powerctrl'
    POWERSUPPLY = 'powersupply'

class Sensor:
    def __init__(self, sensor_obj):
        self.uid = 0
        self.type = SensorTypeId.DEFAULT
        self.chassis_id = ""
        self.id = 0
        self.name = ""
        if (sensor_obj.get('dev') != None):
            self.dev = device_item.DevItem(sensor_obj.get('dev'))
        else:
            self.dev = None
        if (sensor_obj.get('cpld') != None):
            self.cpld = device_item.CpldItem(sensor_obj.get('cpld'))
        else:
            self.cpld = None
        if (sensor_obj.get('gpio') != None):
            self.gpio = device_item.GpioItem(sensor_obj.get('gpio'))
        else:
            self.gpio = None
        if (sensor_obj.get('plat') != None):
            self.platform = device_item.PlatItem(sensor_obj.get('plat'))
        else:
            self.platform = None
        self.property = self.get_sensor_property()

    def __str__(self):
        return 'ChassisID: {chassis_id}, UID: {uid}, Type: {type}, ID: {id}, Name: {name}, Property: {property}'.format(**vars(self))

    def set_uid(self, uid):
        self.uid = uid

    def get_sensor_property(self):
        sensor_property = {}
        for item in [self.dev, self.cpld, self.gpio, self.platform]:
            if item != None:
                if item.property != None:
                    sensor_property.update(item.property)
        return sensor_property

    def get_property_path(self, key):
        if key in self.property:
            return self.property[key]
        else:
            return None

    def get_property_mask(self, item):
        mask_str = f"{item}_mask"
        if mask_str in self.property:
            return self.property[mask_str]
        else:
            return None

class Fan(Sensor):
    action_name_list = ["rpm", "pwm", "present"]
    mask_list = [0, 0, 1]
    info_name_list = []

    def __init__(self, chassis_id, id, sensor_dict):
        super().__init__(sensor_dict)
        self.type = SensorTypeId.FAN
        self.chassis_id = chassis_id
        self.id = id
        self.name = sensor_dict.get('name', f"fan {self.id}")
        self.min = sensor_dict.get('min', 0)
        self.max = sensor_dict.get('max', 26500)
        self.threshold = sensor_dict.get('threshold', [0] * 6)

class Temperature(Sensor):
    action_name_list = ["celsius"]
    mask_list = [0]
    info_name_list = []

    def __init__(self, chassis_id, id, sensor_dict):
        super().__init__(sensor_dict)
        self.type = SensorTypeId.THERMAL
        self.chassis_id = chassis_id
        self.id = id
        self.name = sensor_dict.get('name', f"thermal {self.id}")
        self.min = sensor_dict.get('min', 0)
        self.max = sensor_dict.get('max', 70)
        self.threshold = sensor_dict.get('threshold', [0] * 6)

class Voltage(Sensor):
    action_name_list = ["adc"]
    mask_list = [0]
    info_name_list = []

    def __init__(self, chassis_id, id, sensor_dict):
        super().__init__(sensor_dict)
        self.type = SensorTypeId.VOLTAGE
        self.chassis_id = chassis_id
        self.id = id
        self.name = sensor_dict.get('name', f"voltage {self.id}")
        self.min = sensor_dict.get('min', 0)
        self.max = sensor_dict.get('max', 1500)
        self.threshold = sensor_dict.get('threshold', [0] * 6)

class PowerCtrl(Sensor):
    action_name_list = ["comsumpt", "present"]
    mask_list = [0, 1]
    info_name_list = []

    def __init__(self, chassis_id, id, sensor_dict):
        super().__init__(sensor_dict)
        self.type = SensorTypeId.POWERCTRL
        self.chassis_id = chassis_id
        self.id = id
        self.name = sensor_dict.get('name', f"powerctrl {self.id}")
        self.min = sensor_dict.get('min', 0)
        self.max = sensor_dict.get('max', 0)
        self.threshold = sensor_dict.get('threshold', [0] * 6)

class PowerSupply(Sensor):
    action_name_list = ["vin","state"]
    mask_list = [0, 1]
    info_name_list = ["fw_ver", "mfr", "model", "serial"]

    def __init__(self, chassis_id, id, sensor_dict):
        super().__init__(sensor_dict)
        self.type = SensorTypeId.POWERSUPPLY
        self.chassis_id = chassis_id
        self.id = id
        self.name = sensor_dict.get('name', f"powersupply {self.id}")
        self.min = sensor_dict.get('min', 0)
        self.max = sensor_dict.get('max', 0)
        self.threshold = sensor_dict.get('threshold', [0] * 6)


cls_name = [Sensor, Fan, Temperature, Voltage, PowerCtrl, PowerSupply]
