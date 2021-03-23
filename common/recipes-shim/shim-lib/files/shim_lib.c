#include <ctype.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#include <pthread.h>
#include <math.h>
#include "shim_lib.h"

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

static int read_device(const char *device, int *value);
static int get_current_dir(const char *device, char *dir_name);

int shim_get_chassis_id(char *str) {
    for (int i = 0; i < chassis_size; i++) {
        if (strncmp(chassis_name[i], str, strlen(chassis_name[i])) == 0) {
            return i;
        }
    }
    return -1;
}

int shim_get_chassis_name(int chassisId, char *chassisName) {
    size_t len = 1;
    if (chassis_size == 0) {
        return -1;
    }

    if (chassisId >= chassis_size) {
        return -1;
    }
    if (chassis_name[chassisId] != NULL) {
       len = strlen(chassis_name[chassisId]);
    }
    strncpy(chassisName, chassis_name[chassisId], len);
    return 0;
}

int shim_get_snr_size(int chassisId, int snrType, int *size) {
    int temp = 0;

    switch (snrType) {
        case SNR_FAN:
            temp = fan_size[chassisId];
            break;
        case SNR_THERMAL:
            temp = thermal_size[chassisId];
            break;
        case SNR_VOLTAGE:
            temp = voltage_size[chassisId];
            break;
        case SNR_POWERCTRL:
            temp = powerctrl_size[chassisId];
            break;
        case SNR_POWERSUPPLY:
            temp = powersupply_size[chassisId];
            break;
        default:
            return -1;
    }
    *size = temp;
    return 0;
}

snr_data_st* shim_get_dev_list(int chassisId, int snrType, int memberId) {
    snr_data_st* snrPtr = NULL;

    switch (snrType) {
        case SNR_FAN:
            snrPtr = &dev_fan_list[chassisId][memberId];
            break;
        case SNR_THERMAL:
            snrPtr = &dev_thermal_list[chassisId][memberId];
            break;
        case SNR_VOLTAGE:
            snrPtr = &dev_voltage_list[chassisId][memberId];
            break;
        case SNR_POWERCTRL:
            snrPtr = &dev_powerctrl_list[chassisId][memberId];
            break;
        case SNR_POWERSUPPLY:
            snrPtr = &dev_powersupply_list[chassisId][memberId];
            break;
        default:
            break;
    }
    return snrPtr;
}

int shim_check_snr_exist(int chassisId, int snrType, int memberId) {
    int size = 0;
    int rc = 0;

    rc = shim_get_snr_size(chassisId, snrType, &size);
    if (rc == -1) {
        return -1;
    }

    if (size == 0) {
        return -1;
    }

    if (memberId >= size) {
        return -1;
    }
    return 0;
}

int shim_get_snr_id(int chassisId, int snrType, int memberId, int *snrId) {
    snr_data_st* snrPtr = NULL;

    if (shim_check_snr_exist(chassisId, snrType, memberId) != 0) {
        return -1;
    }

    snrPtr = shim_get_dev_list(chassisId, snrType, memberId);
    if (snrPtr == NULL) {
        return -1;
    }
    *snrId = snrPtr->sensor_id;
    return 0;
}

int shim_get_snr_name(int chassisId, int snrType, int memberId, char *chassisName) {
    snr_data_st* snrPtr = NULL;
    size_t len = 1;
    if (shim_check_snr_exist(chassisId, snrType, memberId) != 0) {
        return -1;
    }

    snrPtr = shim_get_dev_list(chassisId, snrType, memberId);
    if (snrPtr == NULL) {
        return -1;
    }
    if (snrPtr->name != NULL) {
        len = MIN(strlen(snrPtr->name), strlen(chassisName));
    }
    
    strncpy(chassisName, snrPtr->name, len);
    return 0;
}

int shim_get_snr_edge(int chassisId, int snrType, int memberId, int edgeType, float *edgeVal) {
    snr_data_st* snrPtr = NULL;

    if (shim_check_snr_exist(chassisId, snrType, memberId) != 0) {
        return -1;
    }

    snrPtr = shim_get_dev_list(chassisId, snrType, memberId);
    if (snrPtr == NULL) {
        return -1;
    }
    if (edgeType == MAX_EDGE) {
        *edgeVal = snrPtr->max_value;
    } else if (edgeType == MIN_EDGE) {
        *edgeVal = snrPtr->min_value;
    } else {
        return -1;
    }
    return 0;
}

int shim_get_snr_threshold(int chassisId, int snrType, int memberId, int thrType, float *thrVal) {
    snr_data_st* snrPtr = NULL;

    if (shim_check_snr_exist(chassisId, snrType, memberId) != 0) {
        return -1;
    }

    snrPtr = shim_get_dev_list(chassisId, snrType, memberId);
    if (snrPtr == NULL) {
        return -1;
    }
    if (thrType == UCR_THR) {
        *thrVal = snrPtr->ucr;
    } else if (thrType == UNC_THR) {
        *thrVal = snrPtr->unc;
    } else if (thrType == UNR_THR) {
        *thrVal = snrPtr->unr;
    } else if (thrType == LCR_THR) {
        *thrVal = snrPtr->lcr;
    } else if (thrType == LNC_THR) {
        *thrVal = snrPtr->lnc;
    } else if (thrType == LNR_THR) {
        *thrVal = snrPtr->lnr;
    } else {
        return -1;
    }
    return 0;
}

int shim_get_fan_present(int chassisId, int memberId, int *present) {
    snr_cap_m_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_FAN, memberId) != 0) {
        return -1;
    }

    capPtr = &fan_present[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        *present = 0;
        return -1;
    }
    tmp = tmp & capPtr->mask;
    if (tmp == capPtr->match) {
        *present = 1;
    } else {
        *present = 0;
    }
    return 0;
}

int shim_get_fan_pwm(int chassisId, int memberId, int *pwmVal) {
    snr_cap_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_FAN, memberId) != 0) {
        return -1;
    }

    capPtr = &fan_pwm[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *pwmVal = tmp;
    return 0;
}

int shim_get_fan_rpm(int chassisId, int memberId, int *rpmVal) {
    snr_cap_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_FAN, memberId) != 0) {
        return -1;
    }

    capPtr = &fan_rpm[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *rpmVal = tmp;
    return 0;
}

int shim_get_thermal_celsius(int chassisId, int memberId, float *celsius) {
    snr_cap_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_THERMAL, memberId) != 0) {
        return -1;
    }

    capPtr = &thermal_celsius[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *celsius = tmp / 1000;
    return 0;
}

hw_info_st* shim_get_info_list(int chassisId, int type, int memberId, int infoType) {
    hw_info_st* infoPtr = NULL;

    if (shim_check_snr_exist(chassisId, type, memberId) != 0) {
        return NULL;
    }

    if (type == SNR_POWERSUPPLY)
    {
        switch (infoType) {
            case FW_VER:
                infoPtr = &powersupply_fw_ver[chassisId][memberId];
                break;
            case MFR:
                infoPtr = &powersupply_mfr[chassisId][memberId];
                break;
            case MODEL:
                infoPtr = &powersupply_model[chassisId][memberId];
                break;
            case SERIAL:
                infoPtr = &powersupply_serial[chassisId][memberId];
                break;
            default:
                break;
        }
    }

    return infoPtr;
}

int shim_get_pwr_watt(int chassisId, int memberId, float *watt) {
    snr_cap_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_POWERCTRL, memberId) != 0) {
        return -1;
    }

    capPtr = &powerctrl_comsumpt[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *watt = (float) tmp / 1000;
    return 0;
}

int shim_get_pwr_volt(int chassisId, int snrType, int memberId, float *volt) {
    snr_cap_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, snrType, memberId) != 0) {
        return -1;
    }

    switch (snrType) {
        case SNR_VOLTAGE:
            capPtr = &voltage_adc[chassisId][memberId];
            break;
        case SNR_POWERSUPPLY:
            capPtr = &powersupply_vin[chassisId][memberId];
            break;
        default:
            return -1;
    }

    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *volt = (float) tmp / 1000;
    return 0;
}

int shim_get_info(int chassisId, int type, int memberId, int infoType, char *info) {
    hw_info_st* infoPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    infoPtr = shim_get_info_list(chassisId, type, memberId, infoType);
    if (infoPtr == NULL) {
        return -1;
    }
    dir_name = infoPtr->info;
    if (read_device(dir_name, &tmp)) {
        return -1;
    }
    *info = tmp;
    return 0;

}

int shim_get_pwr_present(int chassisId, int memberId, int *present) {
    snr_cap_m_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_POWERCTRL, memberId) != 0) {
        return -1;
    }

    // capPtr = &powerctrl_present[chassisId][memberId];
    capPtr = &powerctrl_present[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        *present = 0;
        return -1;
    }
    tmp = tmp & capPtr->mask;
    *present = (tmp == capPtr->match) ? 1 : 0;

    return 0;
}

int shim_get_pwr_state(int chassisId, int memberId, int *state) {
    snr_cap_m_st* capPtr = NULL;
    char* dir_name = NULL;
    int tmp = 0;

    if (shim_check_snr_exist(chassisId, SNR_POWERCTRL, memberId) != 0) {
        return -1;
    }

    // capPtr = &powerctrl_state[chassisId][memberId];
    capPtr = &powersupply_state[chassisId][memberId];
    dir_name = capPtr->dir;
    if (read_device(dir_name, &tmp)) {
        *state = 0;
        return -1;
    }
    tmp = tmp & capPtr->mask;
    *state = (tmp == capPtr->match) ? 1 : 0;

    return 0;
}

// Helper Functions
static int read_device(const char *device, int *value) {
    FILE *fp = NULL;
    char * pch = NULL;
    char pre_dir_name[MAX_DIR_NAME + 1] = {0};
    char cur_dir_name[MAX_DIR_NAME + 1] = {0};
    char file_name[MAX_FILE_NAME + 1] = {0};
    char full_name[MAX_DIR_NAME * 2] = {0};
    int pre_dir_len = 0;
    int rc = 0;
    size_t len = 1;
    pch=strrchr(device,'/');
    pre_dir_len = pch - device;
    strncpy(pre_dir_name, device, pre_dir_len);
    len = strlen(device) - pre_dir_len - 1;
    strncpy(file_name, pch + 1, len);
    if (get_current_dir(pre_dir_name, cur_dir_name)) {
        return -1;
    }

    snprintf(full_name, sizeof(full_name), "%s/%s", cur_dir_name, file_name);
    fp = fopen(full_name, "r");
    if (!fp) {
        return -1;
    }

    rc = fscanf(fp, "%i", value);
    fclose(fp);
    if (rc != 1) {
        return -1;
    } else {
        return 0;
    }
}

static int get_current_dir(const char *device, char *dir_name) {
    char cmd[MAX_CMD_LEN + 1] = {0};
    FILE *fp = NULL;
    int ret = -1;
    int size = 0;

    // Get current working directory
    snprintf(cmd, MAX_CMD_LEN, "cd %s;pwd", device);

    fp = popen(cmd, "r");
    if (NULL == fp) {
        return -1;
    }

    if (fgets(dir_name, MAX_DIR_NAME, fp) == NULL) {
        pclose(fp);
        return -1;
    }
    ret = pclose(fp);
    if (-1 == ret) {
        printf("%s pclose() fail ", __func__);
    }

    // Remove the newline character at the end
    size = strlen(dir_name);
    dir_name[size-1] = '\0';
    return 0;
}
