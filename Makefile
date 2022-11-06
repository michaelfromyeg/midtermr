SHELL:=/bin/bash

.PHONY: client server install freeze

client:
	pushd client && npm run dev && popd

server:
	pushd server && python -m flask --app app --debug run && popd

install:
	pushd client && npm i && popd \
	pushd server && pip install -r requirements.txt && popd

freeze:
	pushd server && pip freeze > requirements.txt && popd
