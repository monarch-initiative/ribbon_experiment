import requests
import simplejson as json
import pprint

ribbon_terms = ["ZP:0000043",
                "ZP:0018576",
                "ZP:0018546",
                "ZP:0000038",
                "ZP:0000054",
                "ZP:0000473",
                "ZP:0000212",
                "ZP:0000095",
                "ZP:0000115"]

# add escaping
escaped_ribbon_terms = [term.replace(":", "\\:") for term in ribbon_terms]
ribbon_term_facet_queries = {
        term: {
            "type": "query",
            "q": f"phenotypic_feature:{term}",
            "facet": {
                "annotations": "unique(id)",
                "classes": "unique(phenotypic_feature)"
            }
        } for term in escaped_ribbon_terms}
host = "localhost"
port = "8983"
collection = "phenotype_annotations"
qt = "query"
url = 'http://' + host + ':' + port + '/solr/' + collection + '/' + qt + '?'
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
for key, value in response.json()["facets"].items():
    if key != 'count':
        result[key] = {
            "annotations": value["annotations"],
            "classes": value["classes"]
        }

pprint.pprint(result)
