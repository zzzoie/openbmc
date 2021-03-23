redfish_mapper = [
    ("/redfish/v1", "get_serviceroot"),
    ("/redfish/v1/Chassis", "get_chassis_collection"),
    ("/redfish/v1/Chassis/{ChassisId}", "get_chassis"),
    ("/redfish/v1/Chassis/{ChassisId}/Thermal", "get_thermal"),
    ("/redfish/v1/Chassis/{ChassisId}/Power", "get_power"),
    ("/redfish/v1/Managers", "rf_manager"),
    ("/redfish/v1/Managers/bmc", "rf_manager_bmc"),
    ("/redfish/v1/Managers/bmc/Actions", "rf_bmc_actions"),
    ("/redfish/v1/Managers/bmc/Actions/Manager.Reset", "rf_bmc_reset"),
    ("/redfish/v1/UpdateService", "rf_updateservice"),
    ("/redfish/v1/UpdateService/FirmwareInventory", "rf_fwinv"),
    ("/redfish/v1/UpdateService/FirmwareInventory/BMC" , "rf_fwinv_bmc")
]