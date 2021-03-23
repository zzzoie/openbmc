FILESEXTRAPATHS_prepend := "${THISDIR}/files:"
DEPENDS_append += "shim-gen-native redfish-native"
RDEPENDS_${PN} += "shim-gen redfish"

SRC_URI += " \
    file://rest-api-1/setup_plat_routes.py \
"

binfiles1 += " \
    setup_plat_routes.py \
"
