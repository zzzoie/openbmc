import json
import sys
import re
import os

import bmc_sensor
import bmc_manager
from handler_mapper import redfish_mapper

CONFIG_FILE = "config.json"
REDFISH_PATH = "redfish/v1"

ROUTES_FILE = "redfishroutes.py"
SETUP_ROUTES_FILE = "redfish_setup_routes.py"
ENDPOINT_FILE = "redfish_endpoint.py"
FEATURE_FILE = "redfish_feature.py"
PAL_FILE = "shim_list.c"
PAL_HEAD_FILE = "shim_list.h"

ROUTE_NAME = "redfish_routes"
HANDLER_CLASS = "redfishApp_Handler"


class ConfigParser:

    def __init__(self, config=CONFIG_FILE):
        self.config_location = os.path.dirname(os.path.realpath(__file__)) + '/' + config
        self.config = self.get_config(self.config_location)
        self.resource_variable_set = set()
        self.url_list = []
        self.parameter_list = []
        self.action_handler_list = [] # tuple(action, path, handler)
        self.chassis_list = []
        self.fan_list = []
        self.thermal_list = []
        self.voltage_list = []
        self.power_ctrl_list = []
        self.power_supply_list = []

    def get_config(self, file):
        """Load json file and convert it to python structure."""
        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            #TODO Use Log
            print("Unable to open file: " + file)

    def redfish_mapper_parser(self):
        """Analyze if url has resource variable and collect."""
        for tp in redfish_mapper:
            url = tp[0]
            path_variable_list = []
            while url != None:
                if url.find('{') != -1 and url.find('}') != -1:
                    res_name = url.split("{")[0].split("/")[-2]
                    res_var  = url.split("{")[1].split("}")[0]
                    self.resource_variable_set.add((res_name, res_var))
                    path_variable_list.append(res_var)
                    url = url.split("{")[1].split("}")[1]
                else:
                    break
            self.parameter_list.append(path_variable_list)

    def find_serviceroot_link(self, json):
        """Use config to constitude url path and collect sensors information."""
        redfish_dict = json[REDFISH_PATH]
        redfish_path = self.add_url_path(REDFISH_PATH)
        for key, value in redfish_dict.items():
            if isinstance(value, dict):
                if key == 'Chassis':
                    cur_path = self.add_url_path(key, redfish_path)
                    self.find_chassis_resource(value, cur_path)
                # elif key == 'Managers':
                #     cur_path = self.add_url_path(key, redfish_path)
                #     self.find_path(value, redfish_path)
                #elif key == 'UpdateService':
                #    self.find_path(value, redfish_path)
                #else:
                #    cur_path = self.add_url_path(key, redfish_path)
                #    self.find_path(value, cur_path)
            else:
                #TODO Service Root others information
                pass

    def find_chassis_resource(self, json, parent_path):
        for key, value in json.items():
            if isinstance(value, dict):
                cur_path = self.add_url_path(key, parent_path)
                self.find_chassis_path(value, cur_path, key)

    def find_chassis_path(self, json, parent_path, chassis_id):
        """Use config to constitude url path and collect sensors information."""
        for child in json:
            if isinstance(json[child],dict):
                cur_path = self.add_url_path(child, parent_path)
                self.find_chassis_path(json[child], cur_path, chassis_id)
            else:
                if child == "Fans":
                    self.fan_list.append((chassis_id, json[child]))
                elif child == "Temperatures":
                    self.thermal_list.append((chassis_id, json[child]))
                elif child == "PowerControl":
                    self.power_ctrl_list.append((chassis_id, json[child]))
                elif child == "Voltage":
                    self.voltage_list.append((chassis_id, json[child]))
                elif child == "PowerSupplies":
                    self.power_supply_list.append((chassis_id, json[child]))
                else:
                    continue
        return

    def find_path(self, json, parent_path=""):
        """Use config to constitude url path and collect sensors information."""
        for child in json:
            if isinstance(json[child],dict):
                cur_path = self.add_url_path(child, parent_path)
                self.find_path(json[child], cur_path)
            else:
                continue
        return

    def add_url_path(self, node, parent=""):
        """Constitude a URL path and replace the path if it contains variable."""
        action = 'get' # default action is get
        primitive_path = parent + '/' + node
        new_path = primitive_path

        if (node[0] == '#'): # Node has '#' means it is a post action
            action = 'post'
            node = node[1:] #Remove '#'
        for res in self.resource_variable_set:
            key_position = primitive_path.find(res[0])
            if key_position != -1:
                key_list = primitive_path[key_position:].split('/')
                if key_list != None and len(key_list) > 1:
                    new_path = primitive_path[0:key_position] + primitive_path[key_position:].replace(key_list[1], "{" + res[1] + "}", 1)

        if new_path not in self.url_list:
            handler = self.create_redfish_handler(new_path)
            self.url_list.append(new_path)
            self.action_handler_list.append((action, new_path, handler))

        return primitive_path

    def create_redfish_handler(self, path):
        """Create Redfish handler name."""
        handler_function_header = "redfish"
        handler_function_name = ""
        no_symbol_path = re.split('\\/|#|\\.|{|}', path) #path remove symbol

        if len(no_symbol_path) <= 2:
            return handler_function_header
        for i in range(len(no_symbol_path)):
            if i > 2 and len(no_symbol_path[i]) > 0:
                handler_function_name += f"_{no_symbol_path[i].lower()}"
        handler_function_name = f"{handler_function_header}{handler_function_name}"
        return handler_function_name

    def create_routes_file(self):
        """Create redfish_setup_routes.py file."""
        with open(ROUTES_FILE, 'w+') as src:
            src.write(f"{ROUTE_NAME} = [\n")
            for path in self.url_list:
                src.write(f'"{path}",\n')
            src.write("]\n")

    def create_setup_routes_file(self):
        """Create redfish_setup_routes.py file."""
        setup_function_name = "setup_redfish_routes"
        setup_handler_name = "rhandler"
        app = 'app'
        import_list = [(ENDPOINT_FILE[:-3], HANDLER_CLASS),
                    (ROUTES_FILE[:-3], '*')]

        with open(SETUP_ROUTES_FILE, 'w+') as src:
            src.write(f"{self.compose_import_str(import_list)}\n")
            src.write(f"def {setup_function_name}({app}):\n")
            src.write(f"\t{setup_handler_name} = {HANDLER_CLASS}()\n")
            for i in range(len(self.action_handler_list)):
                src.write(self.compose_app_action_str(app, f"{ROUTE_NAME}[{i}]", setup_handler_name, self.action_handler_list[i][0], self.action_handler_list[i][2]))

    def create_endpoint_file(self):
        """Create redfish_endpoint.py file."""
        import_list = [("aiohttp", "web"),
                       ("rest_utils", "dumps_bytestr"),
                       ("redfish", FEATURE_FILE[:-3])]

        with open(ENDPOINT_FILE, 'w+') as src:
            src.write(f"{self.compose_import_str(import_list)}\n")
            src.write(f"class {HANDLER_CLASS}:\n")
            for i in range(len(redfish_mapper)):
                url = redfish_mapper[i][0]
                feature_api_name = redfish_mapper[i][1]
                handler_api_name = self.create_redfish_handler(url)
                endpoint_function = self.compose_resource_endpoint(handler_api_name, feature_api_name, self.parameter_list[i])
                src.write(endpoint_function)

    def compose_import_str(self, import_list):
        """Compose import string in list.

        Example:
        from x1 import y1
        from x2 import y2
        """
        import_str = ''
        for file , item in import_list:
            import_str += f"from {file} import {item}\n"

        return import_str

    def compose_app_action_str(self, app_name, route_item, handler_name, action, handler_function):
        """Compose application action string.

        Example:
        app.router.add_get(redfish_routes[2], rhandler.redfish_chassis_chassisid)
        """
        app_action_str = ""
        if action == 'get':
            action_name='add_get'
        else:
            action_name='add_post'
        app_action_str = (f"\t{app_name}.router.{action_name}({route_item}, {handler_name}.{handler_function})\n")

        return app_action_str

    def compose_resource_endpoint(self, handler, endpoint, parameter_list):
        """Compose handler api string.

        Example:
            async def redfish_chassis_chassisid(self, request):
                return web.json_response(
                    redfish_feature.rf_chassis(request.match_info['ChassisId']), dumps=dumps_bytestr)
        """
        function_name = f"\tasync def {handler}(self, request):\n"
        parameter = ""
        for item in parameter_list:
            parameter += f",request.match_info['{item}']"

        response = f"\t\treturn web.json_response(\n\t\t\t{FEATURE_FILE[:-3]}.{endpoint}({parameter[1:]}), dumps=dumps_bytestr)\n\n"
        output = function_name + response

        return output

    def run(self):
        self.redfish_mapper_parser()
        self.find_serviceroot_link(self.config)
        self.create_routes_file()
        self.create_setup_routes_file()
        self.create_endpoint_file()

        manager = bmc_manager.SensorManager()
        for chassis_id, snr_list in self.fan_list:
            for num, fan in enumerate(snr_list): #start=0
                print(f"{chassis_id}-{num}")
                manager.store_sensor(chassis_id, bmc_sensor.Fan(chassis_id, num, fan))
        for chassis_id, snr_list in self.thermal_list:
            for num, thermal in enumerate(snr_list): #start=0
                print(f"{chassis_id}-{num}")
                manager.store_sensor(chassis_id, bmc_sensor.Temperature(chassis_id, num, thermal))
        for chassis_id, snr_list in self.voltage_list:
            for num, voltage in enumerate(snr_list): #start=0
                manager.store_sensor(chassis_id, bmc_sensor.Voltage(chassis_id, num, voltage))
        # TODO power control object
        for chassis_id, snr_list in self.power_ctrl_list:
            for num, power_ctrl in enumerate(snr_list): #start=0 or 1
                manager.store_sensor(chassis_id, bmc_sensor.PowerCtrl(chassis_id, num, power_ctrl))
        # TODO power supply object
        for chassis_id, snr_list in self.power_supply_list:
            for num, power_supply in enumerate(snr_list): #start=0 or 1
                manager.store_sensor(chassis_id, bmc_sensor.PowerSupply(chassis_id, num, power_supply))

        manager.create_shim_pal(PAL_FILE, PAL_HEAD_FILE)


if __name__ == "__main__":
    try:
        parser = ConfigParser(CONFIG_FILE)
        parser.run()

    except:
        #TODO Use Log
        print(sys.exc_info())
