from urllib.request import urlopen
import simplejson
import pprint

host = "localhost"
port = "8983"
collection = "phenotype_annotations"
qt = "query"
url = 'http://' +host + ':' + port + '/solr/' + collection + '/' + qt + '?'
print(url)
q = "q=*:*"
fq = "fq=phenotypic_feature:ZP\:0002588"
rows = "rows=0"
wt = "wt=json"
jsonfacet = 'json.facet={genes:{type:terms,field:gene,facet:{publication_count:"unique(publications)"}}}'
# wt        = "wt=python"
params = [q, fq, wt, rows, jsonfacet]
p = "&".join(params)

print(url + p)
connection = urlopen(url + p)

if wt == "wt=json":
    response = simplejson.load(connection)
else:
    response = eval(connection.read())

print("Number of hits: " + str(response['response']['numFound']))
pprint.pprint(response['facets']['genes']['buckets'])
