import bmc_sensor
import pal_generator

class SensorManager:
    def __init__(self):
        self.sensor_numbers = 0
        self.chassis_list = {}
        self.chassis_set = set()

    def store_sensor(self, chassis_id, sensor_obj):
        self.sensor_numbers = self.sensor_numbers + 1
        sensor_obj.set_uid(self.sensor_numbers)
        if (chassis_id not in self.chassis_set):
            self.chassis_set.add(chassis_id)
            self.chassis_list[chassis_id] = [[] for i in range(len(bmc_sensor.SensorTypeId))]
        self.chassis_list[chassis_id][sensor_obj.type].append(sensor_obj)

    def get_sensor_numbers(self):
        return self.sensor_numbers

    def get_chassis_object_list(self, chassis_id):
        return self.chassis_list[chassis_id]

    def get_chassis_sensor_list(self, chassis_id, sensor_type):
        return self.chassis_list[chassis_id][sensor_type]

    def get_chassis_sensor_numbers(self, chassis_id, sensor_type):
        return len(self.chassis_list[chassis_id][sensor_type])

    def create_shim_pal(self, file_name, header_name):
        pal = pal_generator.PalGenerator(self, file_name, header_name)
        pal.run()