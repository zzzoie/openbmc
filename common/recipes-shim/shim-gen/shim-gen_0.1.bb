SUMMARY = "Shim Layer Generator"
DESCRIPTION = "Shim Layer Generator"
SECTION = "base"
PR = "r1"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/GPL-2.0;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI = "file://config_parser.py \
           file://config.json \
           file://handler_mapper.py \
           file://bmc_manager.py \
           file://bmc_sensor.py \
           file://device_item.py \
           file://pal_generator.py \
           file://shim_list.h \
           file://Makefile \
          "
#S = "${WORKDIR}/${BPN}-${PV}"
S = "${WORKDIR}"

inherit python3-dir

binfiles = "redfishroutes.py \
            redfish_setup_routes.py \
            redfish_endpoint.py \
           "

pkgdir = "rest-api"

do_configure() {
 python3 ${WORKDIR}/config_parser.py
}

SOURCES = "${WORKDIR}/shim_list.c"
HEADERS = "shim_list.h"

CFLAGS += "-Wall -Werror -fPIC"

do_compile() {
  make SOURCES="${SOURCES}" HEADERS="${HEADERS}"
}

do_install() {
 dst="${D}/usr/local/fbpackages/${pkgdir}"
 bin="${D}/usr/local/bin"
 install -d $dst
 install -d $bin
 for f in ${binfiles}; do
   install -m 755 ${WORKDIR}/$f ${dst}/$f
   ln -snf ../fbpackages/${pkgdir}/$f ${bin}/$f
 done
}

do_install_append() {
  install -d ${D}${libdir}
  install -m 0644 libshim-list.so ${D}${libdir}/libshim-list.so
  ln -s libshim-list.so ${D}${libdir}/libshim-list.so.0

  install -d ${D}${includedir}/openbmc
  for f in ${HEADERS}; do
    install -m 0644 ${S}/$f ${D}${includedir}/openbmc/$f
  done
}

FBPACKAGEDIR = "${prefix}/local/fbpackages"

FILES_${PN} = "${libdir}/libshim-list.so* ${FBPACKAGEDIR}/rest-api ${prefix}/local/bin "
FILES_${PN}-dev = "${includedir}/openbmc"
BBCLASSEXTEND += "native nativesdk"