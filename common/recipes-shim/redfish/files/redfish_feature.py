from enum import IntEnum
from redfish import shim_pal

class SnrType(IntEnum):
    FAN = 1
    THERMAL = 2
    VOLTAGE = 3
    POWERCTRL = 4
    POWERSUPPLY = 5

class SnrEdge(IntEnum):
    MIN_EDGE = 0
    MAX_EDGE = 1

class SnrThreshold(IntEnum):
    LCR_THR = 1
    LNR_THR = 2
    LNC_THR = 3
    UCR_THR = 4
    UNR_THR = 5
    UNC_THR = 6

class Samples(IntEnum):
    MIN = 0
    MAX = 1
    AVG = 2

class Info(IntEnum):
    FW_VER = 0
    MFR = 1
    MODEL = 2
    SERIAL = 3

def get_serviceroot():
    #TODO service root
    pass

def get_chassis_collection():
    chassis_count = shim_pal.shim_get_chassis_size()
    chassis_set = []
    for i in range(chassis_count):
        chassis_set.append({"@odata.id": f"/redfish/v1/Chassis/{shim_pal.shim_get_chassis_name(i)}"})

    res = {
        "@odata.type": "#ChassisCollection.ChassisCollection",
        "@odata.id": "/redfish/v1/Chassis",
        "Name": "Chassis Collection",
        "Members@odata.count": chassis_count,
        "Members": chassis_set
    }
    return res

def get_chassis(chassisName):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    if chassisId is None:
        return {}
    else:
        #TODO chassis_info
        res =  {
            "@odata.type": "#Chassis.v1_11_0.Chassis",
            "@odata.id": f"/redfish/v1/Chassis/{chassisName}",
            "Id": chassisName,
            "Name": chassisName,
            "ChassisType": "",
            "Manufacturer": "",
            "Model": "",
            "SerialNumber": "",
            "PartNumber": "",
            "PowerState": "",
            "Status":{} ,
            "Thermal": {"@odata.id": f"/redfish/v1/Chassis/{chassisName}/Thermal"},
            "Power": {"@odata.id": f"/redfish/v1/Chassis/{chassisName}/Power"}
        }
        return res

def get_objs(chassisName, snrType):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    result = []
    for item in range(shim_pal.shim_get_snr_size(chassisId, snrType)):
        if snrType is SnrType.FAN:
            result.append(get_thermal_fan(chassisName, item))
        if snrType is SnrType.THERMAL:
            result.append(get_thermal_temperature(chassisName, item))
        if snrType is SnrType.VOLTAGE:
            result.append(get_power_volt(chassisName, item))
        if snrType is SnrType.POWERCTRL:
            result.append(get_power_ctrl(chassisName, item))
        if snrType is SnrType.POWERSUPPLY:
            result.append(get_power_supl(chassisName, item))
    return result

def get_thermal(chassisName):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    if chassisId is None:
        return {}
    else:
        res =  {
            "@odata.id": f"/redfish/v1/Chassis/{chassisName}/Thermal",
            "@odata.type": "#Thermal.v1_6_0.Thermal",
            "Id": "Thermal",
            "Name": "Thermal",
            "Fans": get_objs(chassisName, SnrType.FAN),
            "Temperature": get_objs(chassisName, SnrType.THERMAL)
        }
        return res

def get_thermal_fan(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    state = shim_pal.shim_get_fan_present(chassisId, memberId)
    if state == 1:
        status = {"State": "Enabled", "Health":"OK"}
    else:
        status = {"State": "Absent", "Health":"Warning"}

    return {
        "@odata.id": f"/redfish/v1/Chassis/{chassisName}/Thermal#/Fans/{memberId}",
        "@odata.type": "#Thermal.v1_6_0.Thermal",
        "MemberId": str(memberId),
        "Name": shim_pal.shim_get_snr_name(chassisId, SnrType.FAN, memberId),
        "Reading": shim_pal.shim_get_fan_rpm(chassisId, memberId),
        "ReadingUnits": "rpm",
        "Status": status,
        "MaxReadingRange": shim_pal.shim_get_snr_edge(chassisId, SnrType.FAN, memberId, SnrEdge.MAX_EDGE),
        "MinReadingRange": shim_pal.shim_get_snr_edge(chassisId, SnrType.FAN, memberId, SnrEdge.MIN_EDGE),
        "LowerThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.LCR_THR),
        "LowerThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.LNR_THR),
        "LowerThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.LNC_THR),
        "UpperThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.UCR_THR),
        "UpperThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.UNC_THR),
        "UpperThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.FAN, memberId, SnrThreshold.UNR_THR)
    }

def get_thermal_temperature(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    return {
        "@odata.id":f"/redfish/v1/Chassis/{chassisName}/Thermal#/Temperatures/{memberId}",
        "@odata.type": "#Thermal.v1_6_0.Thermal",
        "MemberId": str(memberId),
        "SensorNumber": shim_pal.shim_get_snr_id(chassisId, SnrType.THERMAL, memberId),
        "Name": shim_pal.shim_get_snr_name(chassisId, SnrType.THERMAL, memberId),
        "ReadingCelsius": shim_pal.shim_get_thermal_celsius(chassisId, memberId),
        "MaxReadingRangeTemp": shim_pal.shim_get_snr_edge(chassisId, SnrType.THERMAL, memberId, SnrEdge.MAX_EDGE),
        "MinReadingRangeTemp": shim_pal.shim_get_snr_edge(chassisId, SnrType.THERMAL, memberId, SnrEdge.MIN_EDGE),
        "LowerThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.LCR_THR),
        "LowerThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.LNR_THR),
        "LowerThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.LNC_THR),
        "UpperThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.UCR_THR),
        "UpperThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.UNC_THR),
        "UpperThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.THERMAL, memberId, SnrThreshold.UNR_THR)
    }

def get_power(chassisName):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    if chassisId is None:
        return {}
    else:
        res =  {
            "@odata.id": f"/redfish/v1/Chassis/{chassisName}/Power",
            "@odata.type":"#Power.v1_6_0.Power",
            "Id":"Power",
            "Name":"Power",
            "PowerControl":get_objs(chassisName, SnrType.POWERCTRL),
            "PowerControl@odata.count": shim_pal.shim_get_snr_size(chassisId, SnrType.POWERCTRL),
            "PowerSupplies":get_objs(chassisName, SnrType.POWERSUPPLY),
            "PowerSupplies@odata.count": shim_pal.shim_get_snr_size(chassisId, SnrType.POWERSUPPLY),
            "Voltages":get_objs(chassisName, SnrType.VOLTAGE),
            "Voltages@odata.count": shim_pal.shim_get_snr_size(chassisId, SnrType.VOLTAGE)
        }
        return res

def get_power_ctrl(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    return {
        "@odata.id":f"/redfish/v1/Chassis/{chassisName}/Power#/PowerControl/{memberId}",
        "@odata.type": "#Power.v1_6_0.Power",
        "MemberId": str(memberId),
        "Name": shim_pal.shim_get_snr_name(chassisId, SnrType.POWERCTRL, memberId),
        "PowerConsumptedWatts": shim_pal.shim_get_pwr_watt(chassisId, memberId)
        # "PowerMetrics":get_power_metrix(memberId)
    }

def get_power_supl(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    powerOk = shim_pal.shim_get_pwr_state(chassisId, memberId)
    if powerOk is 1 :
        status = {"State": "Enabled"}
    else:
        status = {"State": "Absent", "debug": powerOk}
    return {
        "@odata.id":f"/redfish/v1/Chassis/{chassisName}/Power#/PowerSupplies/{memberId}",
        "@odata.type": "#Power.v1_6_0.Power",
        "MemberId": str(memberId),
        "Name": shim_pal.shim_get_snr_name(chassisId, SnrType.POWERSUPPLY, memberId),
        "LineInputVoltage": shim_pal.shim_get_pwr_volt(chassisId, SnrType.POWERSUPPLY, memberId),
        "Manufacturer": shim_pal.shim_get_info(chassisId, SnrType.POWERSUPPLY, memberId, Info.MFR),
        "Model": shim_pal.shim_get_info(chassisId, SnrType.POWERSUPPLY, memberId, Info.MODEL),
        "SerialNumber": shim_pal.shim_get_info(chassisId, SnrType.POWERSUPPLY, memberId, Info.SERIAL),
        "Status": status,
        "PartNumber":0
    }

def get_power_volt(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    return {
        "@odata.id": f"/redfish/v1/Chassis/{chassisName}/Power#/Voltage/{memberId}",
        "@odata.type": "#Power.v1_6_0.Power",
        "MemberId": str(memberId),
        "Name": shim_pal.shim_get_snr_name(chassisId, SnrType.VOLTAGE, memberId),
        "ReadingVolts": shim_pal.shim_get_pwr_volt(chassisId, SnrType.VOLTAGE, memberId),
        "LowerThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.LCR_THR),
        "LowerThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.LNR_THR),
        "LowerThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.LNC_THR),
        "UpperThresholdCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.UCR_THR),
        "UpperThresholdFatal": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.UNC_THR),
        "UpperThresholdNonCritical": shim_pal.shim_get_snr_threshold(chassisId, SnrType.VOLTAGE, memberId, SnrThreshold.UNR_THR)
    }


"""
# LE_TODO
def get_power_metrix(chassisName, memberId):
    chassisId = shim_pal.shim_get_chassis_id(chassisName)
    metrix = shim_pal.shim_get_pwr_sample(chassisId, SnrType.POWERCTRL, memberId)
    if len(metrix) < 3:
        res = {
            "IntervalInMin": shim_pal.shim_get_pwr_sample_intvl(chassisId, SnrType.POWERCTRL, memberId),
            "AverageConsumedWatts": 0,
            "MaxConsumedWatts": 0,
            "MinConsumedWatts": 0
        }
    else:
        res = {
            "IntervalInMin": shim_pal.shim_get_pwr_sample_intvl(chassisId, SnrType.POWERCTRL, memberId),
            "AverageConsumedWatts": metrix[Samples.AVG],
            "MaxConsumedWatts": metrix[Samples.MAX],
            "MinConsumedWatts": metrix[Samples.MIN]
        }

    return res
"""