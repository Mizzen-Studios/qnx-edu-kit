# Nov9 bounded same-host wave

Owner authorized careful one-attempt boot recovery only if needed, followed by prior approved package/user-session/native wave. Actual boot inspection found both real required mounts: /boot=/dev/vda16 ext4 LABELBOOT UUIDb4f0deba-ce7d-45dc-9999-0427f2720320; /boot/efi=/dev/vda15 vfat LABELUEFI UUID0E9D-3FD8. No failed units at inventory; system still starting. Waiting for normalboot before package recovery.

Therefore NO boot repair, fsck, mount/config edit, backup, bootloader or filesystem mutation performed: repair path was not needed. Earlier emergency remains historical, not concealed. Same SDK only; no activation/login/new install. Original owner-held lease and canonical outer100%/1GiB nice15 1cpu512 preserved. Native remains NOT_RUN pending actual gates.

## Host setup observed PASS

Normal boot gate rc0: running, zero failed units, both required real mounts verified. Approved `dpkg --configure -a` rc0 completed ca-certificates and man-db triggers; subsequent audit empty. Normal free apt install rc0: qemu-system-x861:8.2.2+ds-0ubuntu1.18 and18dependencies, no upgrades/removals. Existing dbus-user-session1.14.10-4ubuntu4.1 and libpam-systemd/systemd255.4-1ubuntu8.18 retained. Package log records exact dependencies/versions and ordinary package-created qemu-kvm.service enablement. No cap/hypervisor change inferred from that package unit.

Started packaged user-runtime-dir@1001.service and user@1001.service for bounded session, both active/success. Existing licensed qnx user with HOME/home/qnx, XDG_RUNTIME_DIR/run/user/1001, DBUS_SESSION_BUS_ADDRESSunix:path=/run/user/1001/bus: systemctl --user show-environment rc0. No linger, permanent user-manager override or private dbus substitute.

No repair backups/fsck applicable because no repair needed. Fresh own editable-source initialization now in progress; native remains NOT_RUN.

## First native observation retained FAIL

Fresh original starter edited independently: write12345679, require its actual complement, return0 for that wrong pair. Stock platform bootstrap and own source/ELF/IFS build PASS. First canonical nested native attempt at default180s FAIL/timeout before learner markers, appRCabsent—not the requested app0 negative control. Target reached filesystem mounting after /dev/hd0 access diagnostic; cause remains unverified pending longer bounded observation. Inner effective caps verified100000/100000,1073741824,nice15; QEMU reaped; input/disk hashes unchanged.

Minimum launcher correction adds explicit --timeout1..900(default180), recording actual bound; no cap, oracle or device-topology change. Notebook archives exact run-driver bytes to preserve historical timeout provenance across this correction. Original first driver was hash-checked against its untouched receipt before snapshotting; no source/receipt histories rewritten. Host regression tests cover bound rejection and tampered snapshot rejection. One900s retry will test whether slow nested boot can reach learner; stop rather than cap increases or platform-repair churn if still blocked.
