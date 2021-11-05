#!/bin/sh
curl 'http://localhost:8983/solr/phenotype_annotations/update/json/docs?commit=true' -H 'Content-type:application/json' -d @solr_documents.json
