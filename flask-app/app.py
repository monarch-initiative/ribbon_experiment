from flask import Flask, render_template, request
from urllib.request import urlopen
import simplejson

BASE_PATH = 'http://localhost:8983/solr/phenotype_annotations/select'
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    results = None

    if request.method == "POST":
        query = 'q=*:*&fq=phenotypic_feature:ZP\:0002588&rows=0&json.facet={genes:{type:terms,field:gene,facet:{publication_count:"unique(publications)"}}}'

        # query for information and return results
        connection = urlopen("{}{}".format(BASE_PATH, query))
        response = simplejson.load(connection)
        print(response)
        numresults = response['response']['numFound']
        results = response['response']['docs']

    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0')
