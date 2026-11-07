#!/usr/bin/env python3
"""Derive readable incremental teaching snapshots from unchanged E1 native source.
--check is host-only: no SDK, compiler, guest or target PASS is simulated.
"""
import argparse
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]


def snapshots():
    probe = (ROOT / 'native/edu_probe.c').read_text()
    resmgr = (ROOT / 'native/edu_resmgr.c').read_text()
    markers = [
        'puts("EDU STEP1 PASS QNX target process");',
        'puts("EDU STEP2 PASS PCI server attach");',
        'puts("EDU STEP3 PASS BAR ID and complement");',
        'puts("EDU STEP4 PASS factorial polling");',
    ]
    cleanup = probe[probe.index('done:\n'):]
    out = {}
    for n in range(1, 7):
        header = '/* Step %d: readable E1-derived snapshot; regenerate with tools/step_sources.py. */\n' % n
        if n <= 4:
            end = probe.index(markers[n-1]) + len(markers[n-1])
            body = probe[:end] + '\n'
            if n == 1:
                body += '    return 0;\n}\n'
            elif n == 2:
                body += '    pci_device_detach(h);\n    return ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_NONE)<0;\n}\n'
            else:
                body += '    rc=0;\n    goto done;\n' + cleanup
        else:
            body = probe if n == 5 else resmgr
        # Each file is independently compilable at its repository path.
        body = body.replace('#include "edu_dma.h"', '#include "../../../native/edu_dma.h"')
        if n < 5:
            body = body.replace('#include "../../../native/edu_dma.h"\n', '')
        if n == 1:
            begin = body.index('/* Diagnostic-only:')
            body = body[:begin] + body[body.index('int main(void) {', begin):]
        if n in (3, 4):
            body = body.replace('; pci_irq_t irq=-1;', ';')
        out['steps/step%d/solution/main.c' % n] = header + body
        # Keep completed earlier work, but refuse the next boundary explicitly.
        if n == 1:
            starter = '#include <stdio.h>\n#include <sys/utsname.h>\n#include <string.h>\nint main(void) {\n    /* TODO: use uname, require QNX 8.0, print target identity.\n     * Do not report acceptance until the actual target is checked. */\n    fputs("BLOCKED: step1 target identity TODO\\n",stderr);\n    return 2;\n}\n'
        elif n == 2:
            cut = body.index('    pci_err_t error=')
            starter = body[:cut] + '    /* TODO: find 1234:11e8, attach EXCLUSIVE, then detach. */\n    fputs("BLOCKED: step2 PCI ownership TODO\\n",stderr);\n    (void)ThreadCtl(_NTO_TCTL_IO_LEVEL,(void *)(uintptr_t)_NTO_IO_LEVEL_NONE);\n    return 2;\n}\n'
        elif n in (3,4):
            begin = body.index('    puts("EDU read_ba BEGIN");') if n == 3 else body.index('    r[8]=0; r[2]=10;')
            todo = 'validate BAR0 type/extent, map, check ID/complement' if n == 3 else 'start 10!, bounded busy wait, require 3628800'
            starter = body[:begin] + '    /* TODO: '+todo+'. */\n    fputs("BLOCKED: step%d implementation TODO\\n",stderr);\n    rc=2; goto done;\n' % n + cleanup
        elif n == 5:
            begin = body.index('    n=1; error=pci_device_read_irq')
            starter = body[:begin] + '    /* TODO: read IRQ route; IAT, bounded wait, own-bit ack;\n     * then call edu_dma_roundtrip and require byte-exact success. */\n    fputs("BLOCKED: step5 IAT and polled DMA TODO\\n",stderr);\n    rc=2; goto done;\n' + cleanup
            starter = starter.replace('#include "../../../native/edu_dma.h"\n','')
        else:
            begin = body.index('    dispatch = dispatch_create();')
            end = body.index('pci_error:\n', begin)
            starter = body[:begin] + '    /* TODO: dispatch/iofunc setup; bounded edu_write/edu_read;\n     * publish /dev/edu last and allocate per-open snapshots.\n     * Handlers above are the reference scaffolding, not proof of readiness. */\n    fputs("BLOCKED: step6 resource-manager registration TODO\\n",stderr);\n    goto done;\n' + body[end:]
        out['steps/step%d/starter/main.c' % n] = header + starter
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    for name, source in snapshots().items():
        path = ROOT / name
        if args.check:
            if not path.is_file() or path.read_text() != source:
                raise SystemExit('BLOCKED: E1-derived source contract differs: '+name+'; learner edits require a separate rebuilt target bundle, not reference acceptance')
        else:
            path.write_text(source)
    print('CHECKED: twelve E1-derived source snapshots current (host contract only)')

if __name__ == '__main__':
    main()
