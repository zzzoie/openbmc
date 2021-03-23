import ctypes

try:
	libshim = ctypes.cdll.LoadLibrary("libshim.so.0")
except OSError:
	libshim = None

MAX_NAME_STR = 32
MAX_STR_LEN = 128
print(libshim != None)

def shim_get_chassis_size():
	chassis_size = ctypes.c_int.in_dll(libshim, "chassis_size")
	return chassis_size.value

def shim_get_chassis_name(chassisId):
	libshim.shim_get_chassis_name.restype = ctypes.c_int
	libshim.shim_get_chassis_name.argstype = (ctypes.c_int, ctypes.POINTER(ctypes.c_char))
	chassisName = ctypes.create_string_buffer(MAX_NAME_STR)
	ret = libshim.shim_get_chassis_name(chassisId, chassisName)
	if ret == -1:
		return None
	else:
		name = chassisName.value.decode().replace("\u00a0", " ")
		return name

def shim_get_chassis_id(chassisName):
	libshim.shim_get_chassis_id.restype = ctypes.c_int
	libshim.shim_get_chassis_id.argstype = ctypes.POINTER(ctypes.c_char)
	ret = libshim.shim_get_chassis_id(chassisName)
	if ret == -1:
		return None
	else:
		return ret

def shim_get_snr_size(chassisName, snrType):
	libshim.shim_get_snr_size.restype = ctypes.c_int
	libshim.shim_get_snr_size.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	size = ctypes.c_int()
	p_size =  ctypes.pointer(size)
	ret = libshim.shim_get_snr_size(chassisName, snrType, p_size)
	if ret == -1:
		return None
	else:
		return size.value

def shim_get_snr_id(chassisId, snrType, memberId):
	libshim.shim_get_snr_id.restype = ctypes.c_int
	libshim.shim_get_snr_id.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char))
	uid = ctypes.c_int()
	p_uid =  ctypes.pointer(uid)
	ret = libshim.shim_get_snr_id(chassisId, snrType, memberId, p_uid)
	if ret == -1:
		return None
	else:
		return uid.value

def shim_get_snr_name(chassisId, snrType, memberId):
	libshim.shim_get_snr_name.restype = ctypes.c_int
	libshim.shim_get_snr_name.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char))
	snrName = ctypes.create_string_buffer(MAX_NAME_STR)
	ret = libshim.shim_get_snr_name(chassisId, snrType, memberId, snrName)
	if ret == -1:
		return None
	else:
		name = snrName.value.decode().replace("\u00a0", " ")
		return name

def shim_get_snr_edge(chassisId, snrType, memberId, edgeType):
	libshim.shim_get_snr_edge.restype = ctypes.c_int
	libshim.shim_get_snr_edge.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	edge = ctypes.c_float()
	p_edge = ctypes.pointer(edge)
	ret = libshim.shim_get_snr_edge(chassisId, snrType, memberId, edgeType, p_edge)
	if ret == -1:
		return None
	else:
		return edge.value

def shim_get_snr_threshold(chassisId, snrType, memberId, thrType):
	libshim.shim_get_snr_threshold.restype = ctypes.c_int
	libshim.shim_get_snr_threshold.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	thr_val = ctypes.c_float()
	p_thr = ctypes.pointer(thr_val)
	ret = libshim.shim_get_snr_threshold(chassisId, snrType, memberId, thrType, p_thr)
	if ret == -1:
		return None
	else:
		return thr_val.value

def shim_get_fan_pwm(chassisId, memberId):
	libshim.shim_get_fan_pwm.restype = ctypes.c_int
	libshim.shim_get_fan_pwm.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	pwm = ctypes.c_int()
	p_pwm = ctypes.pointer(pwm)
	ret = libshim.shim_get_fan_pwm(chassisId, memberId, p_pwm)
	if ret == -1:
		return None
	else:
		return pwm.value

def shim_get_fan_rpm(chassisId, memberId):
	libshim.shim_get_fan_rpm.restype = ctypes.c_int
	libshim.shim_get_fan_rpm.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	rpm = ctypes.c_int()
	p_rpm = ctypes.pointer(rpm)
	ret = libshim.shim_get_fan_rpm(chassisId, memberId, p_rpm)
	if ret == -1:
		return None
	else:
		return rpm.value

def shim_get_fan_present(chassisId, memberId):
	libshim.shim_get_fan_present.restype = ctypes.c_int
	libshim.shim_get_fan_present.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	present = ctypes.c_int()
	p_present = ctypes.pointer(present)
	ret = libshim.shim_get_fan_present(chassisId, memberId, p_present)
	if ret == -1:
		return None
	else:
		return present.value

def shim_get_thermal_celsius(chassisId, memberId):
	libshim.shim_get_thermal_celsius.restype = ctypes.c_int
	libshim.shim_get_thermal_celsius.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	celsius = ctypes.c_float()
	p_celsius = ctypes.pointer(celsius)
	ret = libshim.shim_get_thermal_celsius(chassisId, memberId, p_celsius)
	if ret == -1:
		return None
	else:
		return celsius.value

def shim_get_max_edge(chassisId, snrType, memberId):
	libshim.shim_get_max_edge.restype = ctypes.c_int
	libshim.shim_get_max_edge.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	edge = ctypes.c_float()
	p_edge = ctypes.pointer(edge)
	ret = libshim.shim_get_max_edge(chassisId, snrType, memberId, p_edge)
	if ret == -1:
		return None
	else:
		return edge.value

def shim_get_min_edge(chassisId, snrType, memberId):
	libshim.shim_get_min_edge.restype = ctypes.c_int
	libshim.shim_get_min_edge.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	edge = ctypes.c_float()
	p_edge = ctypes.pointer(edge)
	ret = libshim.shim_get_min_edge(chassisId, snrType, memberId, p_edge)
	if ret == -1:
		return None
	else:
		return edge.value

def shim_get_pwr_watt(chassisId, memberId):
	libshim.shim_get_pwr_watt.restype = ctypes.c_int
	libshim.shim_get_pwr_watt.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	watt = ctypes.c_float()
	p_watt = ctypes.pointer(watt)
	ret = libshim.shim_get_pwr_watt(chassisId, memberId, p_watt)
	if ret == -1:
		return None
	else:
		return watt.value

def shim_get_pwr_volt(chassisId, snrType, memberId):
	libshim.shim_get_pwr_volt.restype = ctypes.c_int
	libshim.shim_get_pwr_volt.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float))
	volt = ctypes.c_float()
	p_volt = ctypes.pointer(volt)
	ret = libshim.shim_get_pwr_volt(chassisId, snrType, memberId, p_volt)
	if ret == -1:
		return None
	else:
		return volt.value

def shim_get_info(chassisId, snrType, memberId, infoType):
	libshim.shim_get_info.restype = ctypes.c_int
	libshim.shim_get_info.argstype = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char))
	hwInfo = ctypes.create_string_buffer(MAX_STR_LEN)
	ret = libshim.shim_get_info(chassisId, snrType, memberId, infoType, hwInfo)
	if ret == -1:
		return None
	else:
		info = hwInfo.value.decode().replace("\u00a0", " ")
		return info

def shim_get_pwr_present(chassisId, memberId):
	libshim.shim_get_pwr_present.restype = ctypes.c_int
	libshim.shim_get_pwr_present.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	present = ctypes.c_int()
	p_present = ctypes.pointer(present)
	ret = libshim.shim_get_pwr_present(chassisId, memberId, p_present)
	if ret == -1:
		return None
	else:
		return present.value

def shim_get_pwr_state(chassisId, memberId):
	libshim.shim_get_pwr_state.restype = ctypes.c_int
	libshim.shim_get_pwr_state.argstype = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
	state = ctypes.c_int()
	p_state = ctypes.pointer(state)
	ret = libshim.shim_get_pwr_state(chassisId, memberId, p_state)
	if ret == -1:
		return None
	else:
		return state.value