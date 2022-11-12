SHELL:=/bin/bash

.PHONY: client server install freeze

client:
	pushd client && npm run dev && popd

server:
	pushd server && \
	source env/bin/activate && \
	python -m flask --app app --debug run -h localhost -p 8080 && \
	popd

docker-build:
	pushd server && \
	docker build -t midtermr-server . && \
	popd

docker-run:
	docker run midtermr-server

client-deploy:
	pushd client && \
	npm run deploy && \
	popd

server-deploy:
	pushd server && \
	gcloud builds submit --config cloudbuild.yaml . && \
	popd

deactivate:
	deactivate

install:
	pushd client && npm i && popd \
	pushd server && pip install -r requirements.txt && popd

freeze:
	pushd server && pip freeze > requirements.txt && popd
