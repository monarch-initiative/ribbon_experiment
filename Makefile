MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules
MAKEFLAGS += --no-builtin-variables

.DEFAULT_GOAL := all
SHELL := bash

.PHONY: all
all: install-requirements create-solr-docker download set-solr-schema generate-solr-docs index-solr-docs 

.PHONY: install-poetry
install-poetry:
	pip install poetry

install-requirements: install-poetry
	poetry install

.PHONY: download
download:
	curl -OJ "https://storage.googleapis.com/monarch-ingest/output/zfin_gene_to_phenotype_edges.tsv"
	curl -OJ "https://storage.googleapis.com/monarch-ingest/output/alliance_gene_to_phenotype_edges.tsv"
	curl -OJ "https://storage.googleapis.com/monarch-ingest/output/xenbase_gene_to_phenotype_edges.tsv"
	curl -OJ "https://bbop-ontologies.s3.amazonaws.com/upheno/current/upheno-release/all/upheno_all_with_relations.owl"
	wget "https://docs.google.com/spreadsheets/d/12LhMC-814rtaEWYrt96KgFXpS9yrdRzj4H3wrMMyboc/export?format=csv&gid=0" -O ribbon.csv --no-check-certificate

.PHONY: create-solr-docker
create-solr-docker:
	docker run --name phenotype_ribbon_solr -d -p 8983:8983 -t solr solr-precreate phenotype_annotations

.PHONY: delete-solr-docker
delete-solr-docker:
	docker stop phenotype_ribbon_solr
	docker rm phenotype_ribbon_solr

.PHONY: set-solr-schema
set-solr-schema:
	./set-solr-schema.sh

.PHONY: generate-solr-docs
generate-solr-docs:
	poetry run python generate-solr-docs.py

.PHONY: index-solr-docs
index-solr-docs:
	./index-solr-docs.sh

.PHONY: run-api
run-api:
	./run-api.sh


