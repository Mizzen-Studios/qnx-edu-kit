/* Step 6: readable E1-derived snapshot; regenerate with tools/step_sources.py. */
/* Original experimental QNX 8 application; no SDK implementation vendored.
 * Cross-build and actual target acceptance are still required. */
#include <sys/iofunc.h>
#include <sys/resmgr.h>
#include <sys/dispatch.h>
#include <sys/mman.h>
#include <sys/neutrino.h>
#include <sys/slog2.h>
#include <pci/pci.h>
#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAP_BYTES 0x1000U
#define INPUT_MAX 3U
#define RESULT_MAX 16U
#define EDU_PULSE_CODE (_PULSE_CODE_MINAVAIL + 1)
#define EDU_LOG_LIMIT 8U
#define DEADLINE_NS UINT64_C(1000000000)

/* Only main's dispatch thread accesses PCI, registers or these objects. */
static volatile uint32_t *regs = MAP_FAILED;
static char latest[RESULT_MAX];
static size_t latest_len;
static int failed;
static int irq_id = -1;
static unsigned irq_completions;
static int pulse_chid = -1, pulse_coid = -1;
static slog2_buffer_t event_buffer;
static unsigned event_count;

/* One page and at most eight writes for the entire process, never a log loop.
 * Logging failure is an observation failure, not evidence of completed I/O. */
static int edu_event(uint16_t code, const char *text)
{
    if (event_count >= EDU_LOG_LIMIT) return EOK;
    if (slog2c(event_buffer, code, SLOG2_INFO, text) < 0) return EIO;
    ++event_count;
    return EOK;
}

static int setup_events(void)
{
    slog2_buffer_set_config_t config = {0};
    config.buffer_set_name = "edu_learner";
    config.num_buffers = 1;
    config.verbosity_level = SLOG2_INFO;
    config.buffer_config[0].buffer_name = "events";
    config.buffer_config[0].num_pages = 1;
    config.max_retries = 3;
    if (slog2_register(&config, &event_buffer, SLOG2_LIMIT_RETRIES) < 0) return EIO;
    pulse_chid = ChannelCreate(_NTO_CHF_PRIVATE);
    if (pulse_chid < 0) return errno;
    pulse_coid = ConnectAttach(0, 0, pulse_chid, _NTO_SIDE_CHANNEL, 0);
    if (pulse_coid < 0) return errno;
    puts("EDU RESMGR SLOG2 configured pages=1 limit=8");
    return edu_event(1, "EDU_EVENT ready channel=private budget=8 pages=1");
}

/* Explicit, intra-process teaching handoff. The SAME dispatch/IAT owner sends
 * and receives one pulse after the real own-bit IRQ/ack. This is not a second
 * IST, asynchronous resmgr worker, timing proof or a replacement for IRQ ack. */
static int irq_to_dispatch(unsigned sequence, unsigned input, uint32_t result)
{
    struct _pulse pulse;
    uint64_t receive_limit = DEADLINE_NS;
    char text[128];
    if (MsgSendPulse(pulse_coid, -1, EDU_PULSE_CODE, (int)sequence) < 0)
        return errno;
    if (TimerTimeout(CLOCK_MONOTONIC, _NTO_TIMEOUT_RECEIVE, NULL,
                     &receive_limit, NULL) < 0) return errno;
    if (MsgReceivePulse(pulse_chid, &pulse, sizeof(pulse), NULL) < 0)
        return errno;
    if (pulse.code != EDU_PULSE_CODE || pulse.value.sival_int != (int)sequence)
        return EBADMSG;
    snprintf(text, sizeof(text),
             "EDU_EVENT pulse sequence=%u input=%u result=%" PRIu32,
             sequence, input, result);
    if (edu_event(3, text) != EOK) return EIO;
    printf("EDU RESMGR PULSE sequence=%u input=%u result=%" PRIu32
           " sent=1 received=1 owner=same-thread\n", sequence, input, result);
    return EOK;
}

typedef struct {
    iofunc_ocb_t base; /* Must be first: library uses the standard OCB. */
    char result[RESULT_MAX];
    size_t length;
    int snapshot;
} edu_ocb_t;

static iofunc_ocb_t *edu_ocb_alloc(resmgr_context_t *ctp, iofunc_attr_t *attr)
{
    edu_ocb_t *ocb;
    (void)ctp;
    (void)attr;
    ocb = calloc(1, sizeof(*ocb));
    return ocb == NULL ? NULL : &ocb->base;
}

static void edu_ocb_free(iofunc_ocb_t *ocb)
{
    free(ocb);
}

static int monotonic_ns(uint64_t *value)
{
    struct timespec now;
    if (clock_gettime(CLOCK_MONOTONIC, &now) < 0)
        return errno;
    *value = (uint64_t)now.tv_sec * UINT64_C(1000000000) +
             (uint64_t)now.tv_nsec;
    return EOK;
}

/* Same dispatch thread owns IAT and MMIO. Every successful write must wake
 * through InterruptWait and acknowledge our device's completion bit. No poll
 * fallback: timeout or a foreign/shared interrupt cannot publish a result. */
static int factorial(unsigned value, uint32_t *result)
{
    uint64_t start, now;
    if (failed) return EIO;
    if (regs[8] & 1U) return EBUSY;
    if (monotonic_ns(&start) != EOK) return errno;
    regs[0x64/4] = 0xffffffffU;
    regs[8] = 0x80U;
    regs[2] = value;
    for (;;) {
        if (monotonic_ns(&now) != EOK || now - start >= DEADLINE_NS) {
            failed = 1; return ETIMEDOUT;
        }
        uint64_t remaining = DEADLINE_NS - (now - start);
        if (TimerTimeout(CLOCK_MONOTONIC, _NTO_TIMEOUT_INTR, NULL,
                         &remaining, NULL) < 0 || InterruptWait(0, NULL) < 0) {
            failed = 1; return errno;
        }
        uint32_t pending = regs[0x24/4];
        int complete = (pending & 1U) && !(regs[8] & 1U);
        if (pending) regs[0x64/4] = pending;
        if (InterruptUnmask(0, irq_id) < 0) {
            failed = 1; return errno;
        }
        if (complete) {
            *result = regs[2];
            char text[128];
            snprintf(text, sizeof(text),
                     "EDU_EVENT irq sequence=%u input=%u result=%" PRIu32 " ack=%08" PRIx32,
                     irq_completions + 1U, value, *result, regs[0x24/4]);
            int handoff_error = edu_event(2, text);
            if (handoff_error == EOK)
                handoff_error = irq_to_dispatch(irq_completions + 1U, value, *result);
            if (handoff_error != EOK) { failed = 1; return handoff_error; }
            printf("EDU RESMGR IRQ completion=%u input=%u result=%" PRIu32 " ack=%08" PRIx32 "\n",
                   ++irq_completions, value, *result, regs[0x24/4]);
            return EOK;
        }
    }
}

/* Exactly one complete command per write: 1-2 ASCII digits, optional LF.
 * Split commands are not buffered; each write is an independent transaction. */
static int parse_command(const char *input, size_t length, unsigned *value)
{
    unsigned n = 0;
    if (length != 0 && input[length - 1] == '\n')
        --length;
    if (length == 0 || length > 2)
        return EINVAL;
    for (size_t i = 0; i < length; ++i) {
        if (input[i] < '0' || input[i] > '9')
            return EINVAL;
        n = n * 10U + (unsigned)(input[i] - '0');
    }
    if (n > 12)
        return ERANGE;
    *value = n;
    return EOK;
}

static int edu_write(resmgr_context_t *ctp, io_write_t *msg, iofunc_ocb_t *base)
{
    edu_ocb_t *ocb = (edu_ocb_t *)base;
    char input[INPUT_MAX];
    uint64_t requested;
    uint32_t result;
    unsigned value;
    ssize_t received;
    int nonblock, error, length;
    error = iofunc_write_verify(ctp, msg, base, &nonblock);
    if (error != EOK)
        return error;
    if ((msg->i.xtype & _IO_XTYPE_MASK) != _IO_XTYPE_NONE)
        return ENOSYS;
    requested = _IO_WRITE_GET_NBYTES(msg);
    if (requested == 0) {
        _IO_SET_WRITE_NBYTES(ctp, 0);
        return _RESMGR_NPARTS(0);
    }
    if (requested > INPUT_MAX)
        return EMSGSIZE;
    received = resmgr_msgread(ctp, input, (size_t)requested, sizeof(msg->i));
    if (received < 0)
        return errno;
    if ((uint64_t)received != requested)
        return EBADMSG;
    error = parse_command(input, (size_t)requested, &value);
    if (error != EOK)
        return error;
    if (nonblock)
        return EAGAIN; /* Synchronous commands require bounded waiting. */
    if (failed)
        return EIO;
    if (regs[8] & 1U)
        return EBUSY;
    latest_len = 0;
    ocb->snapshot = 0;
    error = factorial(value, &result);
    if (error != EOK)
        return error;
    length = snprintf(latest, sizeof(latest), "%" PRIu32 "\n", result);
    if (length < 0 || (size_t)length >= sizeof(latest))
        return EIO;
    latest_len = (size_t)length;
    memcpy(ocb->result, latest, latest_len);
    ocb->length = latest_len;
    ocb->snapshot = 1;
    base->offset = 0; /* Same O_RDWR descriptor may immediately read result. */
    base->attr->flags |= IOFUNC_ATTR_MTIME | IOFUNC_ATTR_CTIME;
    _IO_SET_WRITE_NBYTES(ctp, (size_t)requested);
    return _RESMGR_NPARTS(0);
}

static int edu_read(resmgr_context_t *ctp, io_read_t *msg, iofunc_ocb_t *base)
{
    edu_ocb_t *ocb = (edu_ocb_t *)base;
    uint64_t requested;
    size_t offset, count;
    int error = iofunc_read_verify(ctp, msg, base, NULL);
    if (error != EOK)
        return error;
    if ((msg->i.xtype & _IO_XTYPE_MASK) != _IO_XTYPE_NONE)
        return ENOSYS;
    requested = _IO_READ_GET_NBYTES(msg);
    _IO_SET_READ_NBYTES(ctp, 0);
    if (requested == 0)
        return _RESMGR_NPARTS(0);
    if (!ocb->snapshot) {
        if (failed)
            return EIO;
        if (latest_len == 0)
            return EAGAIN;
        memcpy(ocb->result, latest, latest_len);
        ocb->length = latest_len;
        ocb->snapshot = 1;
    }
    if (base->offset < 0)
        return EINVAL;
    if ((uint64_t)base->offset >= ocb->length)
        return _RESMGR_NPARTS(0);
    offset = (size_t)base->offset;
    count = ocb->length - offset;
    if (requested < count)
        count = (size_t)requested;
    SETIOV(ctp->iov, ocb->result + offset, count);
    _IO_SET_READ_NBYTES(ctp, count);
    base->offset += (off_t)count;
    base->attr->flags |= IOFUNC_ATTR_ATIME;
    return _RESMGR_NPARTS(1);
}

int main(void)
{
    pci_err_t error = PCI_ERR_OK;
    pci_devhdl_t device = NULL;
    pci_ba_t bars[6] = {0};
    int_t count = 6;
    int rc = EXIT_FAILURE, attach_id = -1;
    dispatch_t *dispatch = NULL;
    dispatch_context_t *context = NULL;
    resmgr_attr_t config = {0};
    resmgr_connect_funcs_t connect_funcs;
    resmgr_io_funcs_t io_funcs;
    iofunc_attr_t attr;
    iofunc_mount_t mount;
    iofunc_funcs_t mount_funcs = {
        .nfuncs = _IOFUNC_NFUNCS,
        .ocb_calloc = edu_ocb_alloc,
        .ocb_free = edu_ocb_free
    };
    setvbuf(stdout, NULL, _IONBF, 0);
    /* Essential on the tested x86 PCI path; no inheritance, no worker thread. */
    if (ThreadCtl(_NTO_TCTL_IO_LEVEL,
                  (void *)(uintptr_t)_NTO_IO_LEVEL_1) < 0) {
        perror("ThreadCtl(IO_LEVEL_1)");
        return rc;
    }
    pci_bdf_t bdf = pci_device_find(0, 0x1234, 0x11e8, PCI_CCODE_ANY);
    if (bdf == PCI_BDF_NONE) {
        fputs("EDU absent\n", stderr);
        goto done;
    }
    device = pci_device_attach(bdf, pci_attachFlags_e_EXCLUSIVE, &error);
    if (device == NULL)
        goto pci_error;
    error = pci_device_read_ba(device, &count, bars, pci_reqType_e_UNSPECIFIED);
    if (error != PCI_ERR_OK)
        goto pci_error;
    if (count < 0 || count > 6)
        goto done;
    for (int i = 0; i < count; ++i) {
        if (bars[i].bar_num == 0 && bars[i].type == pci_asType_e_MEM &&
            bars[i].size >= MAP_BYTES) {
            regs = mmap_device_memory(NULL, MAP_BYTES,
                       PROT_READ | PROT_WRITE | PROT_NOCACHE, 0, bars[i].addr);
            break;
        }
    }
    if (regs == MAP_FAILED) {
        perror("EDU BAR0 mapping");
        goto done;
    }
    if (regs[0] != UINT32_C(0x010000ed)) {
        fputs("Unexpected EDU identification\n", stderr);
        goto done;
    }
    pci_irq_t irq = -1;
    count = 1;
    error = pci_device_read_irq(device, &count, &irq);
    if (error != PCI_ERR_OK || count != 1 || irq < 0) goto pci_error;
    regs[0x64/4] = 0xffffffffU;
    irq_id = InterruptAttachThread(irq, _NTO_INTR_FLAGS_TRK_MSK);
    if (irq_id < 0) { perror("InterruptAttachThread"); goto done; }
    printf("EDU RESMGR IAT attached irq=%d id=%d\n", irq, irq_id);
    if (setup_events() != EOK) {
        fputs("EDU pulse/slog2 setup failed\n", stderr);
        goto done;
    }
    dispatch = dispatch_create();
    if (dispatch == NULL) {
        perror("dispatch_create");
        goto done;
    }
    iofunc_func_init(_RESMGR_CONNECT_NFUNCS, &connect_funcs,
                     _RESMGR_IO_NFUNCS, &io_funcs);
    io_funcs.read = edu_read;
    io_funcs.write = edu_write;
    iofunc_attr_init(&attr, S_IFCHR | 0660, NULL, NULL);
    attr.uid = geteuid();
    attr.gid = getegid();
    if (iofunc_mount_init(&mount, sizeof(mount)) < 0) {
        perror("iofunc_mount_init");
        goto done;
    }
    mount.funcs = &mount_funcs;
    attr.mount = &mount;
    config.nparts_max = 1;
    config.msg_max_size = 2048;
    attach_id = resmgr_attach(dispatch, &config, "/dev/edu", _FTYPE_ANY, 0,
                              &connect_funcs, &io_funcs, &attr);
    if (attach_id < 0) {
        perror("resmgr_attach");
        goto done;
    }
    context = dispatch_context_alloc(dispatch);
    if (context == NULL) {
        perror("dispatch_context_alloc");
        goto done;
    }
    puts("EDU /dev/edu ready mode=0660 (experimental, IAT IRQ completion required)");
    for (;;) {
        dispatch_context_t *next = dispatch_block(context);
        if (next == NULL) {
            if (errno == EINTR)
                continue;
            perror("dispatch_block");
            break;
        }
        context = next;
        dispatch_handler(context);
    }
    goto done;
pci_error:
    fprintf(stderr, "EDU PCI: %s\n", pci_strerror(error));
done:
    if (attach_id >= 0)
        resmgr_detach(dispatch, attach_id, _RESMGR_DETACH_ALL);
    if (context != NULL)
        dispatch_context_free(context);
    if (dispatch != NULL)
        dispatch_destroy(dispatch);
    if (irq_id >= 0) InterruptDetach(irq_id);
    if (pulse_coid >= 0) ConnectDetach(pulse_coid);
    if (pulse_chid >= 0) ChannelDestroy(pulse_chid);
    if (regs != MAP_FAILED) regs[0x64/4] = 0xffffffffU;
    if (regs != MAP_FAILED)
        munmap((void *)regs, MAP_BYTES);
    if (device != NULL)
        pci_device_detach(device);
    if (ThreadCtl(_NTO_TCTL_IO_LEVEL,
                  (void *)(uintptr_t)_NTO_IO_LEVEL_NONE) < 0)
        perror("ThreadCtl(IO_LEVEL_NONE)");
    return rc;
}
