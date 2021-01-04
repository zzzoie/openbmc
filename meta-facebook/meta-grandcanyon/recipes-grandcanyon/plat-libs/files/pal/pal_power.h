#ifndef __PAL_POWER_H__
#define __PAL_POWER_H__

#define SET_SERVER_PWR_DELAY 3
#define SERVER_AC_CYCLE_DELAY 2

enum {
  POWER_STATUS_ALREADY_OK = 1,
  POWER_STATUS_OK = 0,
  POWER_STATUS_ERR = -1,
  POWER_STATUS_FRU_ERR = -2,
};

int pal_set_server_power(uint8_t fru, uint8_t cmd);
int pal_get_server_power(uint8_t fru, uint8_t *status);
int pal_get_server_12v_power(uint8_t *status);
int pal_sled_cycle(void);
int pal_get_last_pwr_state(uint8_t fru, char *state);
int pal_set_last_pwr_state(uint8_t fru, char *state);
uint8_t pal_set_power_restore_policy(uint8_t slot, uint8_t *pwr_policy, uint8_t *res_data);
void pal_get_chassis_status(uint8_t fru, uint8_t *req_data, uint8_t *res_data, uint8_t *res_len);

#endif
