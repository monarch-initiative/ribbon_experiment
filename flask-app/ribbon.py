import requests
import pandas as pd
import pprint
import csv
from flask import Flask

app = Flask(__name__)

@app.route("/")
def show_ribbon():
    df = pd.read_csv('../ribbon.csv')
    # get the ribbon terms
    ribbon_terms = pd.unique(df[["Top level", "Sub level"]].values.ravel()).tolist()
    categories = []
    ribbon_stuff = {}

    # Top level,Top level name,Sub level,Sub level label
    with open('../ribbon.csv') as file:
        reader = csv.reader(file)
        current_id = ''
        for row in reader:
            if row[0] == 'Top level':
                continue
            if current_id == '':
                current_id = row[0]
                category = {"id": row[0],
                            "label": row[1],
                            "description": row[1],
                            "groups": [{"id": row[2],
                                        "label": row[3]}]
                            }
            else:
                if row[0] == current_id:
                    category["groups"].append({"id": row[2],
                                            "label": row[3]})
                else:
                    category = {"id": row[0].replace(":", "\\:"),
                                "label": row[1],
                                "description": row[1],
                                "groups": [row[2]]}
            categories.append(category)

    ribbon_stuff["categories"] = categories
    ribbon_stuff["subjects"] = []
    pprint.pprint(ribbon_stuff)
    #value.replace(":", "\\:")

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


    result = {'categories': []}


    for key, value in response.json()["facets"].items():
        if key != 'count':
            if len(value) > 1:
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

    return ribbon_stuff
