check:
	@./arxiv-mail-checker.sh

lint:
	@autoflake -iv --remove-all-unused-imports . && isort . && black .

clean:
	@rm results-*.txt


