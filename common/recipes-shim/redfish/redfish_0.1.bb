SUMMARY = "Redfish API"
DESCRIPTION = "Redfish API"
SECTION = "base"
PR = "r1"
LICENSE = "GPLv2"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/GPL-2.0;md5=801f80980d171dd6425610833a22dbe6"

SRC_URI = "file://redfish_feature.py \
           file://shim_pal.py \
          "

DEPENDS_append += "shim-lib-native"
RDEPENDS_${PN} += "shim-lib"
S = "${WORKDIR}/${BPN}-${PV}"

inherit python3-dir


dst="${PYTHON_SITEPACKAGES_DIR}/redfish"

do_install() {
 install -d ${D}${dst}
 install -m 755 ${WORKDIR}/redfish_feature.py ${D}${dst}/redfish_feature.py
 install -m 755 ${WORKDIR}/shim_pal.py ${D}${dst}/shim_pal.py
}

FILES_${PN} = "${dst}"
BBCLASSEXTEND += "native nativesdk"