#ifndef __SHIM_LIB_H__
#define __SHIM_LIB_H__
#include <openbmc/shim_list.h>

#define MAX_DIR_NAME 128
#define MAX_FILE_NAME 32
#define MAX_CMD_LEN 150

snr_data_st* shim_get_dev_list(int chassisId, int snrType, int memberId);
hw_info_st* shim_get_info_list(int chassisId, int type, int memberId, int infoType);
int shim_check_snr_exist(int chassisId, int snrType, int memberId);
int shim_get_chassis_id(char *str);
int shim_get_chassis_name(int chassisId, char *chassisName);
int shim_get_snr_size(int chassisId, int snrType, int *size);
int shim_get_snr_id(int chassisId, int snrType, int memberId, int *snrId);
int shim_get_snr_name(int chassisId, int snrType, int memberId, char *chassisName);
int shim_get_snr_edge(int chassisId, int snrType, int memberId, int edgeType, float *edgeVal);
int shim_get_snr_threshold(int chassisId, int snrType, int memberId, int thrType, float *thrVal);
/*fan*/
int shim_get_fan_pwm(int chassisId, int memberId, int *pwmVal);
int shim_get_fan_rpm(int chassisId, int memberId, int *rpmVal);
int shim_get_fan_present(int chassisId, int memberId, int *present);
/*thermal*/
int shim_get_thermal_celsius(int chassisId, int memberId, float *celsius);
/*power: powersupply & powerctrl*/
int shim_get_pwr_watt(int chassisId, int memberId, float *watt);
int shim_get_pwr_volt(int chassisId, int snrType, int memberId, float *volt);
int shim_get_pwr_present(int chassisId, int memberId, int *present);
int shim_get_pwr_state(int chassisId, int memberId, int *state);
/*general*/
int shim_get_info(int chassisId, int type, int memberId, int infoType, char *info);
#endif /*__SHIM_LIB_H__*/