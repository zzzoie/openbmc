SUMMARY = "Shim Layer"
DESCRIPTION = "Shim Layer"
SECTION = "base"
PR = "r1"
LICENSE = "LGPLv2"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/LGPL-2.1;md5=1a6d268fd218675ffea8be556788b780"


SRC_URI = "file://shim_lib.c \
           file://shim_lib.h \
           file://Makefile \
          "

DEPENDS += " shim-gen"
LDFLAGS += " -lshim-list"
SOURCES = "shim_lib.c"
HEADERS = "shim_lib.h"

CFLAGS += "-Wall -Werror -fPIC"

S = "${WORKDIR}"

do_compile() {
  make SOURCES="${SOURCES}" HEADERS="${HEADERS}"
}

do_install() {
  install -d ${D}${libdir}
  install -m 0644 libshim.so ${D}${libdir}/libshim.so
  ln -s libshim.so ${D}${libdir}/libshim.so.0

  install -d ${D}${includedir}/openbmc
  for f in ${HEADERS}; do
    install -m 0644 ${S}/$f ${D}${includedir}/openbmc/$f
  done
}

DEPENDS_append += "shim-gen-native"
RDEPENDS_${PN} += "shim-gen"
FILES_${PN} = "${libdir}/libshim.so*"
FILES_${PN}-dev = "${includedir}/openbmc"
BBCLASSEXTEND += "native nativesdk"