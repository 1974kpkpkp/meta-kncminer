FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-1.0:"

PRINC := "${@int(PRINC) + 1}"

do_install_append() {
	update-rc.d -r ${D} dropbear start 40 S .
}
