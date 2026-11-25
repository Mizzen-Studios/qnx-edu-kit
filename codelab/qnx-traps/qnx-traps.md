id: qnx-traps
title: Catch five QNX traps before the native lab
summary: Diagnose message, pulse, resource-manager and ability mistakes using a bounded HOST worksheet.
categories: Operating System, Debugging
tags: intermediate
platforms: Host
status: draft
authors: Mizzen Studios

# Catch five QNX traps before the native lab

## Overview — HOST only
Duration: 2:00

[Open the interactive worksheet](index.html). It runs locally, including offline. No installation, account, SDK or QEMU is required. Python 3 is needed only for the CLI checker. Browser JavaScript is needed only for interactive feedback. This is original Apache-2.0 teaching material, not an official QNX codelab or a submission to qnx/codelabs.

You will predict a result, select a diagnosis, inspect per-step feedback, and explain the correction. All observations below are **expected scenario observations**, not newly captured QNX output. The worksheet checks your selected reasoning only: HOST_STATIC_REASONING. Native validation is **NOT_RUN**. No compiler, actual process blocking, permissions or hardware behavior is tested.

The structure follows the public [QNX codelabs template](https://github.com/qnx/codelabs/blob/eaddbfbcb271db18645fc760ee411c0293a30d6a/markdown/markdown-template.md): metadata, overview/prerequisites, ordered H2 steps and Duration estimates. Reviewed 25 November 2026 alongside its README and cross-compile example. No upstream prose, SDK code, headers or binaries copied. Status stays draft: no upstream publication, featured flag or published date is implied. Local rendering is our deterministic renderer, not claat.

## 1. Separate messages, pulses and errors
Duration: 3:00

Wrong design: treat every MsgReceive result <= 0 as failure.

Expected observation: a pulse returns 0 and is dropped. Diagnosis: -1 is error, 0 is pulse, positive is a received message ID. Fix: use three distinct branches. Process the pulse code without MsgReply; reserve reply/error paths for received messages. This is a plain MsgReceive-loop scenario, not a replacement for dispatch's registered pulse callbacks.

In the worksheet, answer “A pulse is not an error” and press Check this step. MISSING means choose an answer; RETRY explains the distinction; CORRECT means this selected answer matches, not that a binary ran.

Source: [QNX 8 MsgReceive](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/m/msgreceive.html).

## 2. Complete a synchronous request
Duration: 3:00

Wrong design: receive a message and log it, but never complete it.

Expected observation: this synchronous MsgSend client remains reply-blocked. Diagnosis: receiving alone does not reply. Fix: use MsgReply for the accepted request or MsgError for its failure, accounting separately for lifecycle events and deliberate deferred replies. A pulse is not a substitute completion. Choose an answer and check the reply step.

Source: [QNX 8 MsgReply](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/m/msgreply.html).

## 3. Finish a finite resource-manager read
Duration: 4:00

Wrong design: return the whole factorial result on every read, ignoring the per-open OCB offset.

Expected observation: cat repeats the result forever in this finite-result design. Diagnosis: payload slicing/EOF is the handler's responsibility; iofunc_read_verify validates access and message details, not your complete read implementation. Fix: validate, bound by requested bytes and remaining payload, advance the OCB offset, return zero bytes at EOF. Separate opens have separate OCBs; duplicated descriptors can share an OCB. A streaming device may deliberately use different semantics; this exercise is explicitly finite and seekable. Check the read step.

Source: [QNX 8 iofunc_read_verify](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/i/iofunc_read_verify.html). Compare the original repository [step6 handler](../../steps/step6/solution/main.c), without treating the reference as your learner execution.

## 4. Keep ability evidence distinct from path policy
Duration: 3:00

Wrong claim: a successful IO ability configuration proves all clients can access /dev/edu.

Expected observation: ability setup alone gives no path-access verdict. Diagnosis: procmgr_ability operates on process ability identifiers, operations, root/non-root domains and optional subranges. These are not a demonstration of pathname attach/connect policy. Fix: narrow only required operations, check results, and separately authorize/observe real deny/allow and actual loaded policy before any claim. Do not grant broad abilities to make a test green. Check the ability step.

Source: [QNX 8 procmgr_ability](https://www.qnx.com/developers/docs/8.0/com.qnx.doc.neutrino.lib_ref/topic/p/procmgr_ability.html). Existing [ability lesson](../../docs/ability-lesson.md) retains its bounded evidence and policy blocker.

## 5. Keep the oracle fixed
Duration: 3:00

Wrong design: accept exit0 even though write12345679/readedcba986 differs from the required write12345678/readedcba987.

Expected observation: FAIL the exercise's value oracle despite a consistent complement and app exit0. Fix the operand, not the required oracle. Check the final step, then Check all steps. The repository's [historical journey](../../docs/acceptance/coherent-stock-20261113/RESULT.md) is source-bound history, not this worksheet's native proof.

## Export and check one step on HOST
Duration: 2:00

Download answers for CLI from the worksheet. From the repository root:

~~~sh
python3 scripts/check_traps.py --answers qnx-trap-answers.json --step receive
python3 scripts/check_traps.py --answers qnx-trap-answers.json
~~~

Or print a fresh empty worksheet without a browser:

~~~sh
python3 scripts/check_traps.py --template
~~~

Save that JSON to your own file and add choices to answers using step IDs receive, reply, read, ability, oracle and the option keys in [the original catalog](catalog.json). The answer key is intentionally readable. Exit0 means all selected scope answers correct; exit1 means RETRY/MISSING; exit2 means invalid/missing/unsupported input. Single-step completion is not whole-lab completion. Unknown keys, unknown choices, duplicate JSON keys, stale/tampered catalog hash and inputs over16384bytes are rejected. No command strings, C source or native receipts are executed or accepted.

The catalog hash binds worksheet version/content, not authenticity or independent learning. Editing an answer to the known correct key can pass: this is formative feedback, not an anti-cheating system or attestation. The browser does not import arbitrary JSON. Downloads contain only your selections and the catalog digest; no uploads or tracking.

## Stop at the evidence boundary
Duration: 1:00

NativeLab validation **NOT_RUN**. Continue only under separate licensed setup and owner authority via [the native learner route](../../docs/learner-route.md). HOST/static answers do not validate your C, qcc output, real MsgSend blocking, pulse delivery, /dev permissions or ability policy. Preserve old FAIL tools, pins and receipts. C6 stays STOPPED; £0; no guest or lease operations belong to this lab.
