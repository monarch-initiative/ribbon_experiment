import pandas as pd
import rdflib
from collections import defaultdict

zfin = pd.read_csv('zfin_gene_to_phenotype_edges.tsv', sep='\t')
alliance = pd.read_csv('alliance_gene_to_phenotype_edges.tsv', sep='\t')
xenbase = pd.read_csv('xenbase_gene_to_phenotype_edges.tsv', sep='\t')
rt = pd.read_csv('ribbon.csv')

df = pd.concat([alliance, xenbase, zfin], ignore_index=True, sort=False)

df = df.rename(columns={"subject": "gene", "object": "phenotypic_feature"})
df = df.drop(['predicate', 'category', 'relation', 'provided_by'], axis=1)
df.to_json('out.json', orient='records', lines=True)

# get the ribbon terms
ribbon_terms = pd.unique(rt[["Top level", "Sub level"]].values.ravel()).tolist()


# map all upheno terms to ribbon terms
g = rdflib.Graph()

g.load('upheno_all_with_relations.owl', format='xml')
upheno = rdflib.Namespace("http://purl.obolibrary.org/obo/upheno.owl")
g.bind('upheno', upheno)

closure_sparql = f"""
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX HP: <http://purl.obolibrary.org/obo/HP_>
PREFIX ZP: <http://purl.obolibrary.org/obo/ZP_>
PREFIX UPHENO: <http://purl.obolibrary.org/obo/UPHENO_>

SELECT distinct ?child ?ribbon_term  WHERE {{
  VALUES ?ribbon_term {{ { " ".join(ribbon_terms)} }}
  ?child rdfs:subClassOf+  ?ribbon_term.    
}} 
"""

closure_query = g.query(closure_sparql)

closure = defaultdict(list)


def uri_to_term(uri):
    return uri.replace('http://purl.obolibrary.org/obo/', '').replace('_', ':')


for res in closure_query:
    closure[uri_to_term(res.child)].append(uri_to_term(res.ribbon_term))

df["ribbon_terms"] = df["phenotypic_feature"].map(closure)

df.to_json('solr_documents.json', orient='records', lines=True)
