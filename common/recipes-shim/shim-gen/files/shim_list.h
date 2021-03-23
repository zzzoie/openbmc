#ifndef __SHIM_LIST_H__
#define __SHIM_LIST_H__

#define MAX_SNR 20
#define MAX_SNR_NAME 32
#define MAX_DEVICE_NAME 128
#define MAX_STR_LEN 128
typedef struct snr_data
{
    int sensor_id;
    int member_id;
    char name[MAX_SNR_NAME];
    float min_value;
    float max_value;
    float lcr;
    float lnr;
    float lnc;
    float ucr;
    float unr;
    float unc;
} snr_data_st;

typedef struct hw_info
{
    int member_id;
    char info[MAX_STR_LEN];
} hw_info_st;

typedef struct snr_cap
{
    int member_id;
    char dir[MAX_DEVICE_NAME];
} snr_cap_st;

typedef struct snr_cap_m
{
    int member_id;
    char dir[MAX_DEVICE_NAME];
    int mask;
    int match;
} snr_cap_m_st;


enum {
    SNR_FAN = 1,
    SNR_THERMAL,
    SNR_VOLTAGE,
    SNR_POWERCTRL,
    SNR_POWERSUPPLY
};

enum {
    MIN = 0,
    MAX,
    AVG
};

enum {
    FW_VER = 0,
    MFR,
    MODEL,
    SERIAL
};

enum {
    MIN_EDGE = 0,
    MAX_EDGE = 1
};

enum {
    LCR_THR = 0x01,
    LNR_THR,
    LNC_THR,
    UCR_THR,
    UNR_THR,
    UNC_THR,
};
extern snr_data_st dev_fan_list[][MAX_SNR];
extern snr_data_st dev_thermal_list[][MAX_SNR];
extern snr_data_st dev_voltage_list[][MAX_SNR];
extern snr_data_st dev_powerctrl_list[][MAX_SNR];
extern snr_data_st dev_powersupply_list[][MAX_SNR];
extern snr_cap_m_st fan_present[][MAX_SNR];
extern snr_cap_st fan_pwm[][MAX_SNR];
extern snr_cap_st fan_rpm[][MAX_SNR];
extern snr_cap_st thermal_celsius[][MAX_SNR];
extern snr_cap_st voltage_adc[][MAX_SNR];
extern snr_cap_st powerctrl_comsumpt[][MAX_SNR];
extern snr_cap_m_st powerctrl_present[][MAX_SNR];
extern snr_cap_st powersupply_vin[][MAX_SNR];
extern snr_cap_m_st powersupply_state[][MAX_SNR];

extern hw_info_st powersupply_fw_ver[][MAX_SNR];
extern hw_info_st powersupply_mfr[][MAX_SNR];
extern hw_info_st powersupply_model[][MAX_SNR];
extern hw_info_st powersupply_serial[][MAX_SNR];

extern const char *chassis_name[];
extern int chassis_size;
extern int fan_size[];
extern int thermal_size[];
extern int voltage_size[];
extern int powerctrl_size[];
extern int powersupply_size[];
#endif /*__SHIM_LIST_H__*/