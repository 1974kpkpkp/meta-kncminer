DESCRIPTION = "Cgminer bitcoin miner SW"
LICENSE = "GPLv3"
LIC_FILES_CHKSUM = "file://COPYING;md5=d32239bcb673463ab874e80d47fae504"

DEPENDS = "ncurses curl"

SRCREV = "bf8a5416ba2876c849ea732f670e6fb4499f866d"
PV = "3.3.1+git${SRCPV}"

SRC_URI = "git://git@orsoc.no-ip.biz/projects/kncminer/cgminer;protocol=ssh;branch=spi-fpga"

S = "${WORKDIR}/git"

EXTRA_OECONF = " \
	     --enable-knc \
	     --disable-adl \
	     --disable-opencl \
	     "
 
inherit autotools pkgconfig
