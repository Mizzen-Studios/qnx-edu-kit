# Existing licensed Linux x86_64 host prerequisites

This is not an SDK installer. Use your existing licensed SDP8 and compatible
Generic x86_64 BSP. Do not log in, activate, copy another SDK or substitute an
owner image to evade a missing-input gate.

On Ubuntu24.04, the free distro package is `qemu-system-x86`; its executable is
`qemu-system-x86_64`. A normal systemd user manager and real session bus are
required, supplied by `dbus-user-session` and `libpam-systemd`. An authorized
administrator can inspect the package plan and install these packages using the
normal host package workflow. If this needs ungranted privileges/approval, stop.
Do not use sudo workarounds or a private dbus daemon instead of the user manager.

```sh
apt-get -s install --no-install-recommends qemu-system-x86 dbus-user-session libpam-systemd
# Authorized administrator only, normal host approval:
apt-get install --no-install-recommends qemu-system-x86 dbus-user-session libpam-systemd
```

An ordinary login through PAM normally establishes `/run/user/$(id -u)` and the
user manager; log out/in after installing session prerequisites if necessary.
On an already authorized headless host, an administrator may start the packaged
`user-runtime-dir@UID.service` and `user@UID.service` for a bounded session. This
is not a persistent linger requirement and does not change SDK licensing.
Run learner commands as the existing licensed non-root user, with its real HOME.
If using an administrator-started user manager, set `XDG_RUNTIME_DIR=/run/user/UID`
and `DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/UID/bus` for that user.

```sh
qemu-system-x86_64 --version
command -v flock systemd-run
systemctl --user show-environment >/dev/null
```

The last command must succeed; variables alone are not proof of a running bus.
Continue at [the canonical route](learner-route.md). The launcher verifies actual
inner QEMU cpu.max<=100%, memory.max<=1GiB and nice>=15 and uses1vCPU/512MiB.
Keep a real exclusive lock across the wave. On a single host no SDK VM needs
stopping between build and native; stop/reap only the inner native VM after each
attempt. In the constrained existing lab, the outer SDK VM stays capped and
owned until the entire single-host attempt ends. No cap increase is permitted.

A512MiB SDK host may require its already authorized1GiB disk swap for stock
linking; inspect existing swap before reactivation, never create/resize silently.
A package/session readiness PASS is HOST only. Wrong-edit FAIL/app0, corrected
native PASS and source/ELF/IFS/disk-bound own export require fresh observations.
One automated existing-SDK passage does not prove human acceptance, a second SDK,
physical-host portability, timing, lifecycle or complete platform/SSH health.
