#!/bin/bash

curl -X POST -H 'Content-type:application/json' --data-binary '{
  "add-field-type" : {
     "name":"keyword",
     "class":"solr.TextField",
     "analyzer" : {
        "tokenizer":{
           "class":"solr.KeywordTokenizerFactory" }}}  
}' http://localhost:8983/solr/phenotype_annotations/schema

for field in gene phenotypic_feature; do
curl -X POST -H 'Content-type:application/json' --data-binary "{
  'add-field':{
     'name':'"$field"', 'type':'keyword',
     'stored':true } 
}" http://localhost:8983/solr/phenotype_annotations/schema
done

for field in ribbon_terms publications; do
curl -X POST -H 'Content-type:application/json' --data-binary "{
  'add-field':{
     'name':'"$field"', 'type':'keyword',
     'stored':true,
     'multiValued':true }
}" http://localhost:8983/solr/phenotype_annotations/schema
done
