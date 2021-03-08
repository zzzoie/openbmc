LINUX_VERSION_EXTENSION = "-agc032a"

COMPATIBLE_MACHINE = "agc032a"

KERNEL_MODULE_PROBECONF += " \
  i2c-mux-pca954x \
"

module_conf_i2c-mux-pca954x = "options i2c-mux-pca954x ignore_probe=1"
