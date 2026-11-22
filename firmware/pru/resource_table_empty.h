/*
 * resource_table_empty.h - minimal remoteproc resource table.
 *
 * The remoteproc loader expects every PRU firmware ELF to carry a resource
 * table. This firmware needs no shared carveouts, interrupts, or vrings, so the
 * table is empty. This mirrors the empty resource table shipped with TI's
 * pru-software-support-package; if you already have that package on the build
 * machine, include its copy instead of this one.
 */

#ifndef RESOURCE_TABLE_EMPTY_H
#define RESOURCE_TABLE_EMPTY_H

#include <stddef.h>

struct my_resource_table {
    uint32_t base;        /* resource table version      */
    uint32_t num;         /* number of entries (none)    */
    uint32_t reserved[2];
};

#pragma DATA_SECTION(resourceTable, ".resource_table")
#pragma RETAIN(resourceTable)
struct my_resource_table resourceTable = {
    1u,   /* version */
    0u,   /* no entries */
    { 0u, 0u },
};

#endif /* RESOURCE_TABLE_EMPTY_H */
