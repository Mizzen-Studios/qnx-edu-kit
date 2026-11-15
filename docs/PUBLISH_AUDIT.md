# Publication audit — 15 November 2026

**HOLD for owner review; not a clean-publication certificate. Repository remains PRIVATE.** No history rewrite, public release, guest execution, SDK installation, contacts or spending were performed. Runtime sources and historical acceptance receipts are unchanged.

## Audited base and scope

Audited source/docs milestone: `9ceb5068787f6a24cd60f84a4c5f272f85b909f5`. After fetching every advertised remote ref (including tags/branches), the reachable inventory is **171 commits, 3321 objects, 1736 unique blobs, 99001867 blob bytes**. Six remote branches, no advertised tags; 19 local refs including duplicate tracking/audit aliases. Exact ref names/object IDs and classified findings are in `docs/PUBLISH_AUDIT_FINDINGS.json`. Blob aliases are enumerated across every reachable commit tree; each finding names a representative reachable commit, not necessarily its earliest introduction.

The inventory is a base snapshot, not a self-referential claim that this report commit audited itself. Final new-commit verification is recorded separately in the private completion evidence after committing the report. That scan includes newly reachable blobs/metadata and generated report/site changes; the frozen base inventory is not relabeled as a final-tip scan.

## Tools and commands

Existing Git, Python stdlib, repository redistribution guard and installed Gitleaks **8.30.0**, executable `/home/linuxbrew/.linuxbrew/bin/gitleaks`; no installation. Commands run from the repository root:

```sh
git fetch --all --tags
git fetch origin "+refs/*:refs/audit/origin/*"
git ls-remote --refs origin
git show-ref
git rev-list --objects --all
git cat-file --batch-check="%(objectname) %(objecttype) %(objectsize)"
git cat-file --batch
git log --all --format="%H%x09%an%x09%ae%x09%cn%x09%ce"
gitleaks git . --log-opts="--all --full-history" --redact=100 --ignore-gitleaks-allow --no-banner --report-format json --report-path PRIVATE_REPORT
# Separate Gitleaks stdin scan streams EVERY reachable unique blob, with blob-ID separators:
gitleaks stdin --redact=100 --no-banner --no-color --ignore-gitleaks-allow --report-format json --report-path PRIVATE_BLOB_REPORT
./scripts/check-no-sdk.sh
./verify.sh --host-only
```

Custom read-only scanners inspect all reachable blob contents, names and commit identities: ELF, QCOW, QNX filesystem signatures, VMDK/ISO/MBR/archive magic and suspicious SDK/image/object/ELF names; IPv4 including tailnet100.64/10, private/link-local IPv6, local/tailnet hostname patterns, absolute owner paths and email-shaped strings. All paths/aliases are mapped with `git ls-tree -rz --full-tree` over every reachable commit. Raw redacted reports, scripts and logs stay outside Git under workspace `.openclaw/tmp/qnx-publish-audit-20261115/edu/`. The committed JSON is a **classified location inventory**, not raw secret-scan output.

## Findings requiring review

- **Personal author email in historical commit metadata:** commit `6e6548539ae638294fcedb495677cf84ef494782`, author email `ollymcbride2@gmail.com`; committer GitHub `noreply@github.com`. Owner decision required before public release. No rewrite authorized or attempted. Other identities are `Claw <claw@local>` and GitHub public/noreply identity `OlsOls2 <262539821+OlsOls2@users.noreply.github.com>`. Exact per-commit author/committer metadata is inventoried.
- **Owner-lab absolute paths:** 1894 deduplicated per-blob/path-value observations. These expose layout/user names, not SDK payloads. Each exact value, source path, blob ID, line and representative commit is in the inventory. Historical receipts are preserved, not silently sanitized.
- **Email-shaped blob strings:** 164 observations, primarily systemd unit-name false positives and public kernel contacts (`dm-devel@redhat.com`, `giometti@linux.it`). Not automatically classified as leaked credentials or private user contacts.
- **IPv4 literals:** nine unique per-blob observations in this base: QEMU private networking `10.0.2.0`, `10.0.2.15`, `10.0.2.2`, `10.0.2.3`, loopback `127.0.0.1`, wildcard `0.0.0.0`, and masks/broadcast `255.0.0.0`, `255.255.255.0`, `255.255.255.255`. These are disclosed network/configuration metadata, not authentication secrets.
- **Private hostname/IPv6 inventory:** exact matched values/locations and classification are included in the JSON; pattern matches can include ordinary textual mentions rather than active host identities. No tailnet or IPv6 clean claim is inferred from an IPv4-only scan.
- **Licensed binary/artifact checks:** zero ELF/QCOW/QNX filesystem magic hits, zero suspicious artifact-name hits in the base; additional VMDK/ISO/MBR/archive checks found zero. This does not prove the absence of every possible licensed text fragment, renamed/encrypted payload or licence restriction. Existing SDK diagnostic/build transcript text is historical evidence, not a redistributed SDK installation.

Gitleaks full-history scan (base before the two submission-prep commits): **6 generic-api-key findings**, all manually inspected as **false positives: public Linux autogenerated X.509 kernel certificate identifiers**, not private keys or API credentials. Exact file/blob/commit/line classifications are in the inventory; matched values are deliberately omitted. Gitleaks reported163 diff-bearing commits and167962115 scanned bytes; Git object inventory separately counts171 reachable commits at the milestone. The independent all-blob scan at9ceb506 scanned all1736 unique blobs/99001867 content bytes and found the same6 public-certificate false positives, individually rebound to blob/path/line/representative commit; commit metadata is inventoried separately. This is not a claim that Gitleaks alone counted every Git object. No credential values are copied into this report.

## Limitations and release decision

Only objects reachable through fetched/local refs were examined: unreachable objects/reflogs, remote hidden/unadvertised refs, external LFS/submodule payloads, ignored external lab assets and another repository are excluded. Secret and private-identifier detection is heuristic, not a universal proof; default Gitleaks decoding limits apply. Filename/magic checks cannot decide every licence issue. No public availability, human-learning, SDK/native rerun or platform-health claim follows from these host checks.

**Keep private and STOP for owner review.** Decide whether the existing personal identity, owner paths and hostname/network disclosures are acceptable before any separately authorized publication. Do not rewrite history or remove evidence on the strength of this report.
