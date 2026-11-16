.PHONY: host-check verify deploy check-step1 check-step2 check-step3 check-step4 check-step5 check-step6
host-check:
	PYTHONDONTWRITEBYTECODE=1 python3 tools/step_sources.py --check
	./scripts/check-no-sdk.sh
	PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
verify:
	./verify.sh
check-reference-step1 check-reference-step2 check-reference-step3 check-reference-step4 check-reference-step5 check-reference-step6:
	@./scripts/check-step.sh $(@:check-reference-step%=%)
check-step1 check-step2 check-step3 check-step4 check-step5 check-step6:
	@echo "REFERENCE ONLY: legacy alias; use make check-reference-step$(@:check-step%=%). NOT learner acceptance."
	@./scripts/check-step.sh $(@:check-step%=%)
deploy:
	@echo "BLOCKED: no verified QNX build or QSTI deployment path; nothing copied."; exit 2

.PHONY: live-edu-check
live-edu-check:
	EDU_LIVE_QTEST=1 PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_qtest_live.py -v

# Source prose -> HTML -> hash inventories -> copied inventories.
.PHONY: refresh-docs
refresh-docs:
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_site.py
	PYTHONDONTWRITEBYTECODE=1 python3 docs/review/build_packet.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_site.py
	PYTHONDONTWRITEBYTECODE=1 python3 scripts/render_site.py --check
	PYTHONDONTWRITEBYTECODE=1 python3 docs/review/build_packet.py --check
