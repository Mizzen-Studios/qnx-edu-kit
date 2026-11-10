#!/bin/bash
# Original stock-platform integration only. Run INSIDE an existing licensed SDK host.
set -eo pipefail
: "${EDU_SDP_ENV:?}" "${EDU_PLATFORM:?}" "${EDU_ACTIVE:?}" "${EDU_SOURCE:?}" "${EDU_SNIPPET:?}"
for path in "$EDU_PLATFORM" "$EDU_ACTIVE"; do
 case "$path" in /*) ;; *) echo 'absolute external paths required' >&2; exit 2;; esac
 case "$path" in *' '*) echo 'paths must not contain spaces' >&2; exit 2;; esac
done
if test -e "$EDU_PLATFORM"; then echo 'fresh platform path already exists; refusing reuse' >&2; exit 2; fi
source "$EDU_SDP_ENV"
mkdir -p "$EDU_ACTIVE"
qcc -Vgcc_ntox86_64 -std=gnu11 -O0 -g3 -Wall -Wextra -Wno-unused-variable -o "$EDU_ACTIVE/learner_bin" "$EDU_SOURCE" -lpci -lslog2
printf '#!/bin/sh
exit 2
' > "$EDU_ACTIVE/learner-start.sh"
mkdir "$EDU_PLATFORM"
cd "$EDU_PLATFORM"
mkqnximage --type=qemu --arch=x86_64 --build --ssh-ident=none
mkdir -p local/snippets
sed "s|@OUT@|$EDU_ACTIVE|g" "$EDU_SNIPPET" > local/snippets/ifs_files.learner
printf 'waitfor /dev/pci/server_id_1 30
sh /proc/boot/learner-start.sh
' > local/snippets/post_start.learner
mkqnximage --build
sha256sum output/build/ifs.build output/build/startup.sh local/snippets/*.learner output/disk-qemu
