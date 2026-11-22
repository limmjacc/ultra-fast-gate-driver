#!/usr/bin/env python3
"""
sweep.py - glitch sweep orchestrator for the crowbar fault-injection fixture.

Runs on the BeagleBone. For each point in a glitch-offset range it:
  1. brings the target to a known state (power or reset cycle),
  2. fires the PRU trigger at that offset (via pru_iface),
  3. checks what the target did (success / crash / no effect),
  4. logs the outcome to CSV.

This is the time-offset sweep. The other two axes, glitch WIDTH and DEPTH, are
set in hardware (the RC delay footprint and the Rs value); change those between
sweeps and re-run. See ../../docs/design for the hardware side.

Two things depend on YOUR setup and are deliberately left as hooks to adapt:
  - TargetControl.cycle(): how you reset or power-cycle the target each attempt.
  - ResultChecker.check(): how you tell success from a crash or no effect.
Defaults are provided (a reset GPIO pulsed via the gpiod CLI, and a UART token
match), but treat them as examples, not finished glue.

UNTESTED starting point. Bring it up a few attempts at a time, with a scope on
the target node, before running long unattended sweeps.
"""

import argparse
import csv
import subprocess
import sys
import time

from pru_iface import PruCtrl

# Outcome labels used in the CSV and on screen.
OK = "success"       # target did the thing a glitch was meant to cause
CRASH = "crash"      # target hung or reset (over-glitched)
NONE = "no_effect"   # target behaved normally (under-glitched or missed)
ERROR = "error"      # harness problem (timeout, read failure)


class TargetControl:
    """Bring the target to a known state before each attempt.

    Default: pulse a reset line low then high using the gpiod CLI (gpioset).
    Replace cycle() with whatever your target needs (power switch, button, etc.).
    """

    def __init__(self, gpiochip=None, line=None, active_low=True, settle_s=0.05):
        self.gpiochip = gpiochip
        self.line = line
        self.active_low = active_low
        self.settle_s = settle_s

    def cycle(self):
        if self.gpiochip is None or self.line is None:
            # No reset wired up: just wait. Replace with your own method.
            time.sleep(self.settle_s)
            return
        asserted = 0 if self.active_low else 1
        released = 1 - asserted
        self._set(asserted)
        time.sleep(self.settle_s)
        self._set(released)
        time.sleep(self.settle_s)

    def _set(self, value):
        subprocess.run(
            ["gpioset", self.gpiochip, f"{self.line}={value}"],
            check=True,
        )


class ResultChecker:
    """Decide what the target did after a glitch.

    Default: read a serial port briefly and look for a success token. Adapt to
    your target: it might be a UART banner, a changed boot message, a debug
    probe query (OpenOCD), or a GPIO the target raises on success.
    """

    def __init__(self, port=None, baud=115200, success_token=b"UNLOCKED",
                 crash_silence_s=0.3, read_s=0.5):
        self.port = port
        self.baud = baud
        self.success_token = success_token
        self.crash_silence_s = crash_silence_s
        self.read_s = read_s
        self._ser = None
        if port:
            try:
                import serial  # pyserial
            except ImportError:
                sys.exit("pyserial not installed: pip3 install pyserial, "
                         "or replace ResultChecker with your own method.")
            self._ser = serial.Serial(port, baud, timeout=0.05)

    def check(self):
        if self._ser is None:
            # No detector wired up. Replace with your own success test.
            time.sleep(self.read_s)
            return NONE, ""
        self._ser.reset_input_buffer()
        end = time.time() + self.read_s
        buf = b""
        last = time.time()
        while time.time() < end:
            chunk = self._ser.read(256)
            if chunk:
                buf += chunk
                last = time.time()
                if self.success_token in buf:
                    return OK, buf[-80:].decode("ascii", "replace")
        detail = buf[-80:].decode("ascii", "replace")
        if not buf or (time.time() - last) > self.crash_silence_s:
            # Nothing, or it went silent: likely a crash/hang.
            return (CRASH if not buf else NONE), detail
        return NONE, detail


def main():
    ap = argparse.ArgumentParser(description="Glitch offset sweep")
    ap.add_argument("--core", type=int, default=0, help="PRU core (0 or 1)")
    ap.add_argument("--start", type=int, required=True, help="offset start (units)")
    ap.add_argument("--stop", type=int, required=True, help="offset stop (units, inclusive)")
    ap.add_argument("--step", type=int, default=1, help="offset step (units)")
    ap.add_argument("--width", type=int, default=20, help="trigger high time (units)")
    ap.add_argument("--repeats", type=int, default=5, help="attempts per offset")
    ap.add_argument("--ns-per-unit", type=float, default=10.0,
                    help="measured ns per delay unit (confirm on a scope)")
    ap.add_argument("--reset-chip", default=None, help="gpiod chip for target reset, e.g. gpiochip1")
    ap.add_argument("--reset-line", type=int, default=None, help="gpiod line number for reset")
    ap.add_argument("--uart", default=None, help="serial port for result, e.g. /dev/ttyUSB0")
    ap.add_argument("--token", default="UNLOCKED", help="success token on the UART")
    ap.add_argument("--out", default="sweep.csv", help="output CSV path")
    args = ap.parse_args()

    target = TargetControl(gpiochip=args.reset_chip, line=args.reset_line)
    checker = ResultChecker(port=args.uart, success_token=args.token.encode())

    hits = 0
    with PruCtrl(core=args.core) as pru, open(args.out, "w", newline="") as f:
        pru.check_magic()
        w = csv.writer(f)
        w.writerow(["offset_units", "offset_ns", "width_units", "attempt",
                    "outcome", "detail"])
        for offset in range(args.start, args.stop + 1, args.step):
            offset_ns = offset * args.ns_per_unit
            for attempt in range(args.repeats):
                try:
                    target.cycle()
                    pru.fire(offset, args.width)
                    outcome, detail = checker.check()
                except (TimeoutError, RuntimeError) as e:
                    outcome, detail = ERROR, str(e)
                w.writerow([offset, f"{offset_ns:.1f}", args.width, attempt,
                            outcome, detail.replace("\n", " ")])
                f.flush()
                if outcome == OK:
                    hits += 1
                    print(f"[HIT] offset={offset} ({offset_ns:.0f} ns) "
                          f"attempt={attempt}: {detail!r}")
            print(f"offset {offset:6d} ({offset_ns:8.0f} ns) done")
    print(f"sweep complete: {hits} success hit(s). log: {args.out}")


if __name__ == "__main__":
    main()
