SHELL:=/bin/bash

.PHONY: server

server:
	pushd server && python -m flask --app app --debug run && popd

install:
	pushd server && pip install -r requirements.txt && popd

freeze:
	pushd server && pip freeze > requirements.txt && popd
