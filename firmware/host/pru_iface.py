"""
pru_iface.py - talk to the PRU trigger firmware from Linux on the BeagleBone.

Maps the PRU data RAM and reads/writes the control block defined in
../pru/glitch_trigger.c. Keep the field layout here in sync with that struct.

The firmware must already be loaded and running on the chosen PRU core (see
../README.md for loading it through remoteproc).

UNTESTED starting point. The physical addresses below are for the AM335x on a
BeagleBone Black; confirm them for your board and kernel.
"""

import mmap
import os
import struct
import time

# AM335x PRU-ICSS data RAM physical base addresses.
PRU0_DRAM = 0x4A300000
PRU1_DRAM = 0x4A302000
DRAM_SIZE = 0x2000  # 8 KB per PRU data RAM

# Control block layout: 5 x uint32, little-endian. Matches struct ctrl.
_FIELDS = ("state", "offset", "width", "count", "magic")
_FMT = "<5I"
_SIZE = struct.calcsize(_FMT)

STATE_IDLE = 0
STATE_ARM = 1
STATE_BUSY = 2
STATE_DONE = 3

MAGIC = 0x6730424C  # must match MAGIC in the firmware


class PruCtrl:
    def __init__(self, core=0):
        base = PRU0_DRAM if core == 0 else PRU1_DRAM
        self._fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        self._map = mmap.mmap(
            self._fd, mmap.PAGESIZE, mmap.MAP_SHARED,
            mmap.PROT_READ | mmap.PROT_WRITE, offset=base,
        )

    def close(self):
        self._map.close()
        os.close(self._fd)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # --- raw field access ---
    def _get(self, name):
        i = _FIELDS.index(name)
        (val,) = struct.unpack_from("<I", self._map, i * 4)
        return val

    def _set(self, name, value):
        i = _FIELDS.index(name)
        struct.pack_into("<I", self._map, i * 4, value & 0xFFFFFFFF)

    # --- convenience ---
    def check_magic(self):
        m = self._get("magic")
        if m != MAGIC:
            raise RuntimeError(
                f"PRU control block magic is 0x{m:08X}, expected 0x{MAGIC:08X}. "
                "Is the firmware loaded and running, and is the core correct?"
            )

    def fire(self, offset, width, timeout_s=1.0):
        """Arm one attempt with the given offset/width (in firmware delay units)
        and wait for it to complete. Returns the firmware's attempt counter."""
        self._set("offset", offset)
        self._set("width", width)
        self._set("state", STATE_ARM)
        deadline = time.time() + timeout_s
        while self._get("state") != STATE_DONE:
            if time.time() > deadline:
                raise TimeoutError("PRU did not report done; is it running?")
        count = self._get("count")
        self._set("state", STATE_IDLE)  # release for the next arm
        return count
