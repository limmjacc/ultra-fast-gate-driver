# Makefile for the PRU trigger firmware (TI PRU Code Generation Tools, clpru).
#
# Build on the BeagleBone (or a cross host with the PRU CGT installed). This
# targets TI's clpru compiler and the pru-software-support-package. A GCC for
# PRU (gnupru) build is also possible but uses different flags; see README.
#
# Usage:
#   make                # build glitch_trigger.out (an ELF for remoteproc)
#   make install        # copy it to /lib/firmware (needs root)
#   make clean
#
# Override these if your install differs:
#   PRU_CGT   - path to the PRU Code Generation Tools
#   PRU_SSP   - path to the pru-software-support-package
#   CORE      - which PRU core (0 or 1); sets the linker memory map used
#   FWNAME    - installed firmware name the remoteproc node points at

PRU_CGT ?= /usr/share/ti/cgt-pru
PRU_SSP ?= /usr/lib/ti/pru-software-support-package
CORE    ?= 0
FWNAME  ?= am335x-pru$(CORE)-fw

TARGET  := glitch_trigger
SRCS    := glitch_trigger.c

CFLAGS  := -v3 -O2 --c99 --display_error_number --endian=little \
           --hardware_mac=on --obj_directory=build --pp_directory=build \
           -I$(PRU_CGT)/include -I$(PRU_SSP)/include -I$(PRU_SSP)/include/am335x -I.
LDFLAGS := --reread_libs --warn_sections --stack_size=0x100 --heap_size=0x100 \
           -m $(TARGET).map -i$(PRU_CGT)/lib -i$(PRU_CGT)/include \
           --library=libc.a --library=$(PRU_SSP)/lib/rpmsg_lib.lib

# Linker command file: use the one from the support package for this core.
LDCMD   := $(PRU_SSP)/labs/lab_5/AM335x_PRU.cmd

CLPRU   := $(PRU_CGT)/bin/clpru

all: build $(TARGET).out

build:
	@mkdir -p build

$(TARGET).out: $(SRCS) $(LDCMD)
	$(CLPRU) $(CFLAGS) $(SRCS) $(LDFLAGS) $(LDCMD) -o $@

install: $(TARGET).out
	cp $(TARGET).out /lib/firmware/$(FWNAME)
	@echo "Installed as /lib/firmware/$(FWNAME)"
	@echo "Point the remoteproc node at it and start; see ../README.md"

clean:
	rm -rf build $(TARGET).out $(TARGET).map

.PHONY: all build install clean
