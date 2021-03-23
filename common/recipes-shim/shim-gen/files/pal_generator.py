import bmc_sensor

MAX_SNR = 20

class PalGenerator:
    def __init__(self, manager, file_name, header_name):
        self.manager = manager
        self.file_name = file_name
        self.header_name = header_name
        self.chassis_enum_name_set = self.compose_chassis_enum_set()

    def get_chassis_sensor_obj_list(self, chassis_id, sensor_type):
        return self.manager.get_chassis_sensor_list(chassis_id, sensor_type)

    def compose_chassis_enum_set(self):
        """Create chassis enumerate name

        Example:
        chassis name : "1"
        enumerate name : "CHASSIS_1"
        """
        enum_set = set()
        for chassis in self.manager.chassis_set:
            enum_set.add(f"CHASSIS_{chassis.upper()}")
        return enum_set

    def create_chassis_enum(self):
        """Create chassis enumerate
        Example:
        enum {
           CHASSIS_1,
           CHASSIS_2
        }
        """
        enum_str = "enum {\n"
        for chassis_enum_id in self.chassis_enum_name_set:
            enum_str += f"\t{chassis_enum_id},\n"
        enum_str += "};\n"
        #enum_str = enum_str[:-2] + "\n};\n"
        return enum_str

    def create_chassis_string_list(self):
        """Create chassis name array
        Example:
        const char* chassis_name[] = {
            "1",
            "2"
        }
        """
        const_str = "const char* chassis_name[] = {\n"
        for chassis_name in self.manager.chassis_set:
            const_str += f'\t"{chassis_name}",\n'
        const_str += "};\n"
        return const_str

    def create_chassis_size_variable(self):
        """Create chassis size variable
        Example:
        int chassis_size = 1;
        """
        chassis_var = f"int chassis_size = {len(self.manager.chassis_set)};\n"
        return chassis_var

    def create_sensor_dev_size(self, sensor_type):
        """ Create sensor size array
        The size of array is determined by chassis numbers.
        Example:
        int fan_size [] = {10,8,3};
        """
        type_name = bmc_sensor.SensorTypeName[sensor_type.name].value
        var_name = f"{type_name}_size"
        size_arr = f"int {var_name}[] = {{"
        for chassis_id in self.manager.chassis_set:
            num = self.manager.get_chassis_sensor_numbers(chassis_id, sensor_type)
            size_arr += f"{num},"
        size_arr += f"}};\n"
        return size_arr

    def create_sensor_dev_list(self, sensor_type):
        """ Create sensor size array
        The size of array is determined by chassis numbers.
        Example:
        int fan_size [] = {10,8,3};
        """
        type_name = bmc_sensor.SensorTypeName[sensor_type.name].value
        func_type = f"snr_data_st"
        func_name = f"dev_{type_name}_list"
        dev_arr = f"{func_type} {func_name}[][{MAX_SNR}] = {{\n"
        for chassis_id in self.manager.chassis_set:
            obj_list = self.get_chassis_sensor_obj_list(chassis_id, sensor_type)
            dev_arr += "{"
            for snr in obj_list:
                dev_arr += f'\t{{{snr.uid}, {snr.id}, "{snr.name}", {snr.min}, {snr.max}'
                for item in snr.threshold:
                    dev_arr += f", {item}"
                dev_arr += f"}},\n"
            dev_arr += "},\n"
        dev_arr += f"}};\n"
        return dev_arr

    def create_property_act_list(self, sensor_type):
        """ Create sensor property array
        action_name_list in bmc_sensor.py determines how many kinds of property to generate.
        Example:
        snr_cap_st fan_rpm[][20] = {
        {	{0, "/sys/bus/i2c/drivers/emc2305/3-002e/fan1_input"},
            ...
        }
        """
        property_str = ""
        type_name = bmc_sensor.SensorTypeName[sensor_type.name].value
        action = bmc_sensor.cls_name[sensor_type].action_name_list
        mask_list = bmc_sensor.cls_name[sensor_type].mask_list

        for i in range(len(action)):
            if mask_list[i] == 0:
                func_type = "snr_cap_st"
            else:
                func_type = "snr_cap_m_st"
            func_name = f"{type_name}_{action[i]}"
            dev_arr = f"{func_type} {func_name}[][20] = {{\n"
            for chassis_id in self.manager.chassis_set:
                obj_list = self.get_chassis_sensor_obj_list(chassis_id, sensor_type)
                dev_arr += "{"
                for snr in obj_list:
                    if mask_list[i] == 0:
                        dev_arr += f'\t{{{snr.id}, "{snr.get_property_path(action[i])}"}},\n'
                    else:
                        mask = snr.get_property_mask(action[i])
                        dev_arr += f'\t{{{snr.id}, "{snr.get_property_path(action[i])}", {mask[0]}, {mask[1]}}},\n' #snr.run(action_list[i])
                dev_arr += "},\n"
            dev_arr += f"}};\n"
            property_str += dev_arr
        return property_str

    def create_property_info_list(self, sensor_type):
        """ Create sensor property array
        info_name_list in bmc_sensor.py determines how many kinds of property to generate.
        Example:
        hw_info powersupply_fw_info[][20] = {
        {	{0, "/sys/bus/i2c/drivers/dps_drivers/0-0058/mfr_rev"},
            ...
        }
        """
        property_str = ""
        type_name = bmc_sensor.SensorTypeName[sensor_type.name].value
        info = bmc_sensor.cls_name[sensor_type].info_name_list

        for i in range(len(info)):
            func_type = "hw_info_st"
            func_name = f"{type_name}_{info[i]}"
            dev_arr = f"{func_type} {func_name}[][20] = {{\n"
            for chassis_id in self.manager.chassis_set:
                obj_list = self.get_chassis_sensor_obj_list(chassis_id, sensor_type)
                dev_arr += "{"
                for snr in obj_list:
                    dev_arr += f'\t{{{snr.id}, "{snr.get_property_path(info[i])}"}},\n'
                dev_arr += "},\n"
            dev_arr += f"}};\n"
            property_str += dev_arr
        return property_str

    def run(self):
        """ Genearate shim library file """
        with open(self.file_name, 'w+', encoding="utf-8") as src:
            src.write(f'#include "{self.header_name}"\n\n')
            src.write(self.create_chassis_size_variable())
            src.write(self.create_chassis_enum())
            src.write(self.create_chassis_string_list())
            for snr_type in bmc_sensor.SensorTypeId:
                if snr_type > bmc_sensor.SensorTypeId.DEFAULT:
                    src.write(self.create_sensor_dev_size(snr_type))
                    src.write(self.create_sensor_dev_list(snr_type))
                    src.write(self.create_property_act_list(snr_type))
                    src.write(self.create_property_info_list(snr_type))
