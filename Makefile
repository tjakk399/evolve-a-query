.PHONY: test install

setup:
	pip install \
		--user \
		--requirement requirements.txt

test:
	clear \
		&& PYTHONPATH=src/python pytest -s -vv

run:
	./evolve_a_query.py \
		--es-host localhost \
		--es-port 9200 \
		--n-rounds 10 \
		--n-lines-from-file \
		language.txt

language.txt: src/prolog/grammar.pl
	$< > $@
