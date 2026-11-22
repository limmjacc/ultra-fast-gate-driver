# Firmware

Control software for driving the crowbar fixture from a BeagleBone Black and
running a glitch sweep against a target board. This is the host and PRU side of
the hardware in [../hardware](../hardware); read [../docs/design](../docs/design)
for how the board itself works.

**Status: untested starting point.** It was written against the AM335x and the
BeagleBone ecosystem but has not been run on hardware yet. Bring it up a few
attempts at a time, with a scope on the target node, and confirm every
hardware-specific value (pin numbers, memory addresses, delay calibration)
before trusting a long sweep.

## Why a PRU

The glitch has to land in a nanosecond-scale window at a precise, repeatable
instant. A normal Linux process cannot do that: scheduling, interrupts, and
caches add microseconds of jitter. The AM335x has two Programmable Real-time
Units, bare 200 MHz cores with single-cycle deterministic GPIO. One PRU
produces the trigger edge; Linux just sets the parameters and reads the result.

## The three sweep axes

A glitch has three knobs. Only one is in firmware:

- **Offset (when):** the delay from a reference event to the trigger. Set in the
  PRU firmware, swept by the host. This is the firmware's whole job.
- **Width (how long):** set on the board by the RC delay footprint (the driver's
  delayed-AND method). Change it in hardware between sweeps.
- **Depth (how hard):** set on the board by the Rs value. Change it in hardware
  between sweeps.

So a full campaign is: pick a width and depth in hardware, sweep the offset in
software, change width or depth, sweep again.

## Layout

```
firmware/
├── pru/
│   ├── glitch_trigger.c        PRU firmware: make the trigger edge at an offset
│   ├── resource_table_empty.h  minimal remoteproc resource table
│   └── Makefile                build with the TI PRU compiler
└── host/
    ├── pru_iface.py            map the PRU control block, arm and read it
    └── sweep.py                offset sweep, target cycling, result logging
```

## Signal path

```
sweep.py (Linux) --writes offset--> PRU control block (data RAM)
PRU core --reads offset, waits, pulses--> R30 trigger pin --> fixture J1 (TRIG)
fixture --> glitch on the target rail
target --> result (UART token, debug probe, or a GPIO) --> sweep.py checks it
```

## Wiring

- **Trigger:** a PRU R30 output pin on the P9 header to the fixture's TRIG input
  (J1). Pick a real `pru_r30` pin, NOT one of the boot-strap pins, and set
  `TRIG_BIT` in `glitch_trigger.c` to that pin's R30 bit. Share ground.
- **Target reset (optional):** a GPIO to the target's reset so each attempt
  starts clean. Wire it to `TargetControl` in `sweep.py`.
- **Result (optional):** the target's UART to a USB-serial adapter, or a debug
  probe, or a success GPIO. Wire it to `ResultChecker` in `sweep.py`.

Set the pin mux on the host before running, for example with config-pin:

```
config-pin <trigger_pin> pruout
```

Confirm which header pin maps to which R30 bit for your image; it varies.

## Build

On the board (or a cross host) with the TI PRU Code Generation Tools and the
pru-software-support-package installed:

```
cd pru
make PRU_CGT=/path/to/cgt-pru PRU_SSP=/path/to/pru-software-support-package
sudo make install CORE=0        # copies the ELF into /lib/firmware
```

A GCC-for-PRU (gnupru) build also works but uses different flags and linker
files; adapt the Makefile if that is your toolchain.

## Load and run

Loading is through remoteproc. The exact sysfs path depends on the kernel; on a
recent image PRU0 is usually `remoteproc1` and PRU1 `remoteproc2`:

```
echo am335x-pru0-fw | sudo tee /sys/class/remoteproc/remoteproc1/firmware
echo start           | sudo tee /sys/class/remoteproc/remoteproc1/state
```

Then run a sweep (needs root for /dev/mem access, and pyserial if you use a UART
result check):

```
cd host
sudo python3 sweep.py --core 0 --start 0 --stop 2000 --step 2 \
    --width 20 --repeats 5 --ns-per-unit 10 \
    --reset-chip gpiochip1 --reset-line 28 \
    --uart /dev/ttyUSB0 --token UNLOCKED --out run1.csv
```

Each row of the CSV is one attempt: offset, offset in ns, width, attempt index,
outcome (success / crash / no_effect / error), and a detail snippet.

## Calibrate before trusting offsets

The firmware's delay loop is nominally a few nanoseconds per unit, but the exact
figure depends on the compiler. Put a scope on the trigger test point, fire with
a known offset, measure the real delay, and set `--ns-per-unit` to match. Do the
same for `--width` so the trigger stays high longer than the board's RC delay.

## Safety

This drives a fixture that intentionally shorts a rail. The board has an
independent hardware max-on-time one-shot, but keep the software honest too:
start with a conservative Rs (higher value), short widths, and a current-limited
supply, and watch the first attempts on a scope. See
[../docs/design/06-safety-and-protection.md](../docs/design/06-safety-and-protection.md).
