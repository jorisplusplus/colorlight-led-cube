//--------------------------------------------------------------------------------
// Auto-generated by Migen (--------) & LiteX (42d8fc22) on 2021-06-05 19:40:16
//--------------------------------------------------------------------------------
#ifndef __GENERATED_SOC_H
#define __GENERATED_SOC_H
#define CONFIG_CLOCK_FREQUENCY 125000000
static inline int config_clock_frequency_read(void) {
	return 125000000;
}
#define CONFIG_CPU_TYPE_NONE
#define CONFIG_CPU_VARIANT_STANDARD
#define CONFIG_CPU_HUMAN_NAME "Unknown"
static inline const char * config_cpu_human_name_read(void) {
	return "Unknown";
}
#define CONFIG_CSR_DATA_WIDTH 8
static inline int config_csr_data_width_read(void) {
	return 8;
}
#define CONFIG_CSR_ALIGNMENT 32
static inline int config_csr_alignment_read(void) {
	return 32;
}
#define CONFIG_BUS_STANDARD "WISHBONE"
static inline const char * config_bus_standard_read(void) {
	return "WISHBONE";
}
#define CONFIG_BUS_DATA_WIDTH 32
static inline int config_bus_data_width_read(void) {
	return 32;
}
#define CONFIG_BUS_ADDRESS_WIDTH 32
static inline int config_bus_address_width_read(void) {
	return 32;
}

#endif
