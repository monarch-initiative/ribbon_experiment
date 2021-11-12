import requests
import pandas as pd
import pprint
from collections import defaultdict

df = pd.read_csv('../ribbon.csv')
# get the ribbon terms
ribbon_terms = pd.unique(df[["Top level", "Sub level"]].values.ravel()).tolist()

# add escaping

# TODO: fix querying to find "others" and "all" instead of just returned "true"
# all across subgroups (ribbon categories = all, other)

escaped_ribbon_terms = [term.replace(":", "\\:") for term in ribbon_terms]
ribbon_term_facet_queries = {
        term: {
            "type": "query",
            "q": f"ribbon_terms:{term}",
            "facet": {
                "annotations": "unique(id)",
                "classes": "unique(phenotypic_feature)"
            }
        } for term in escaped_ribbon_terms}
url = 'http://localhost:8983/solr/phenotype_annotations/query' + '?'
print(url)

query = {
    "params": {
        "q": "*:*",
        "rows": "0",
        "wt": "json",
    },
    "facet": ribbon_term_facet_queries
}

print(url)
response = requests.post(url,
                         headers={"Content-Type": "application/json"},
                         json=query)

result = {}


# TODO: reformat this output to the schema requested by the ribbon.
# http://geneontology.org/docs/ribbon.html
# https://www.alliancegenome.org/api/gene/*/disease-ribbon-summary?geneID=HGNC:11998


for key, value in response.json()["facets"].items():
    if key != 'count':
        if len(value) >1:
            result[key] = {
                "annotations": value["annotations"],
                "classes": value["classes"]
            }
        else:
            result[key] = {
                "annotations": 0,
                "classes": 0
            }





# TODO: connect this to the ribbon frontend -- or have the ribbon frontend call this API
# TODO: where will this API run

pprint.pprint(result)
