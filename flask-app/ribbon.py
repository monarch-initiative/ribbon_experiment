import requests
import pandas as pd
import pprint
import csv
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/ribbon")
def show_ribbon():
    gene_id = request.args.get('id')
    df = pd.read_csv('../ribbon.csv')
    # get the ribbon terms
    ribbon_terms = pd.unique(df[["Top level", "Sub level"]].values.ravel()).tolist()
    categories = []
    ribbon_stuff = {}
    if not gene_id:
        gene_id = 'HGNC:11998'
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
                    category = {"id": row[0],
                                "label": row[1],
                                "description": row[1],
                                "groups": [row[2]]}
            categories.append(category)

    ribbon_stuff["categories"] = categories
    ribbon_stuff["subjects"] = []

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
                    # use the "input" of a gene id (just inject into the API result not query solr for it)
                }
            } for term in escaped_ribbon_terms}
    url = 'http://localhost:8983/solr/phenotype_annotations/query' + '?'

    query = {
        "params": {
            "q": "*:*",
            "rows": "0",
            "wt": "json",
            "fq": "gene:" + gene_id.replace(":", "\\:")
        },
        "facet": ribbon_term_facet_queries
    }

    response = requests.post(url,
                         headers={"Content-Type": "application/json"},
                         json=query)

    result = {}

    for key, value in response.json()["facets"].items():
        if key != 'count':
            if len(value) > 1:
                result[key.replace("\\", "")] = {
                    "ALL": {
                        "nb_annotations": value["annotations"],
                        "nb_classes": value["classes"]
                    }
                }
            else:
                result[key.replace("\\", "")] = {
                    "ALL": {
                        "nb_annotations": 0,
                        "nb_classes": 0
                    }
                }

    subjects = {"id": gene_id, "groups": result}
    ribbon_stuff['subjects'] = subjects

    return ribbon_stuff
