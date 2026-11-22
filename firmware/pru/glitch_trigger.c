/*
 * glitch_trigger.c - PRU firmware for the crowbar fault-injection fixture.
 *
 * Runs on one PRU core of a BeagleBone Black (AM335x, 200 MHz, 5 ns/cycle).
 * Its only job is to produce the trigger edge that the fixture turns into a
 * nanosecond glitch, at a precise, repeatable offset after an arm or an
 * external reference edge. The glitch WIDTH is set on the board itself by the
 * RC delay and Rs, not here (see ../../docs/design/02-pulse-generation.md).
 *
 * Host interface: a small control block at the start of this PRU's data RAM.
 * The Linux host writes the offset and arms; the PRU fires and reports done.
 * See ../host/pru_iface.py for the matching memory layout.
 *
 * UNTESTED starting point. Build on the board with the PRU toolchain, and
 * verify the real nanoseconds-per-count on a scope at the trigger test point
 * before trusting any offset number (the delay loop is calibrated below but
 * depends on the compiler and must be confirmed).
 */

#include <stdint.h>
#include <pru_cfg.h>
#include "resource_table_empty.h"

/* PRU GPIO registers: R30 is the output word, R31 the input word. */
volatile register uint32_t __R30;
volatile register uint32_t __R31;

/*
 * Pin selection. Which R30 bit reaches which header pin is set by pinmux, not
 * here. Pick a genuine pru_r30 output pin (NOT a boot-strap pin) and config it
 * on the host (see ../README.md). TRIG_BIT must match that pin's R30 bit.
 * REF_BIT is an optional input used to start timing from an external edge
 * (for example the target's reset-release); set USE_REF to 1 to use it.
 */
#define TRIG_BIT   (5u)        /* __R30 bit driving the fixture trigger input */
#define REF_BIT    (16u)       /* __R31 bit for the external reference edge    */
#define USE_REF    (0u)        /* 1 = wait for a rising edge on REF before offset */

#define TRIG_MASK  (1u << TRIG_BIT)
#define REF_MASK   (1u << REF_BIT)

/*
 * Control block, placed at the base of this PRU's data RAM (0x0000 as seen by
 * the PRU core). The host maps the same memory and reads/writes these fields.
 * Keep this layout in sync with ../host/pru_iface.py.
 */
struct ctrl {
    volatile uint32_t state;   /* 0 idle, 1 arm (host sets), 2 busy, 3 done   */
    volatile uint32_t offset;  /* delay units before firing (see NS_PER_UNIT) */
    volatile uint32_t width;   /* units to hold trigger high (> board RC delay)*/
    volatile uint32_t count;   /* attempts completed, for the host to watch    */
    volatile uint32_t magic;   /* firmware/layout sanity value                 */
};

#define CTRL   ((volatile struct ctrl *)0x0)
#define MAGIC  (0x6730424Cu)   /* "LB0g" - identifies this layout to the host  */

/*
 * busy_delay(n): spin for n units. Written so the compiler keeps it and each
 * unit is a fixed, small number of PRU cycles. At 200 MHz one cycle is 5 ns.
 * A sub+branch loop is nominally 2 cycles per unit (~10 ns), but CONFIRM the
 * real figure on a scope and set NS_PER_UNIT in the host code to match.
 */
#pragma FUNC_CANNOT_INLINE(busy_delay)
static void busy_delay(uint32_t n)
{
    while (n != 0u) {
        n--;
        __asm__ __volatile__("");   /* keep the loop body, no optimisation away */
    }
}

void main(void)
{
    /* Start with the trigger de-asserted so the FET is off at power-up. */
    __R30 &= ~TRIG_MASK;

    CTRL->count = 0u;
    CTRL->magic = MAGIC;
    CTRL->state = 0u;              /* idle, ready for the host to arm */

    for (;;) {
        /* Wait for the host to arm (state = 1). */
        while (CTRL->state != 1u) {
        }

        uint32_t offset = CTRL->offset;
        uint32_t width  = CTRL->width;
        CTRL->state = 2u;         /* busy */

#if USE_REF
        /* Optionally align to an external rising edge before counting offset. */
        while ((__R31 & REF_MASK) != 0u) { }   /* wait for low  */
        while ((__R31 & REF_MASK) == 0u) { }   /* wait for rise */
#endif

        busy_delay(offset);       /* wait the programmed offset */

        __R30 |= TRIG_MASK;       /* fire: rising edge into the fixture        */
        busy_delay(width);        /* hold high long enough to form the glitch  */
        __R30 &= ~TRIG_MASK;      /* release                                   */

        CTRL->count++;
        CTRL->state = 3u;         /* done; host reads, then re-arms            */
    }
}
