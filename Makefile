.PHONY: host-check verify deploy check-step1 check-step2 check-step3 check-step4 check-step5 check-step6
host-check:
	./scripts/check-no-sdk.sh
	python3 -m unittest discover -s tests -v
verify:
	./verify.sh
check-step1 check-step2 check-step3 check-step4 check-step5 check-step6:
	@./scripts/check-step.sh $(@:check-step%=%)
deploy:
	@echo "BLOCKED: no verified QNX build or QSTI deployment path; nothing copied."; exit 2
