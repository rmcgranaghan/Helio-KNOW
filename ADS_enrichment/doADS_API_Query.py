# Import standard Python libraries
import urllib2
import urllib
import json
import sys
import math
import csv
from datetime import datetime
## Input parameters
# Bumblebee API token
APItoken = 'TOKEN'
# Address of API
API_URL = 'https://api.adsabs.harvard.edu/v1'
QUERY_URL = "%s/search/query" % API_URL
# Query parameters
# The number of records to be returned in Solr query
rows = 300
# What data do we need back from Solr
fields = "bibcode,doi,first_author_norm,title,property"
# date string for output file
dstring = datetime.today().strftime('%Y%m%d')
## Get the query for which we want the data
try:
    query_file = sys.argv[1]
except:
    sys.exit('Please provide name for file with queries as argument...')
## Helper functions
# Execute a search query
def do_query(URL, params):
    qparams = urllib.urlencode(params)
    req = urllib2.Request("%s?%s"%(URL, qparams))
    # and add the correct header information
    req.add_header('Content-type', 'application/json')
    req.add_header('Accept', 'text/plain')
    req.add_header('Authorization', 'Bearer %s' % APItoken)
    # do the actual request
    resp = urllib2.urlopen(req)
    # and retrieve the data to work with
    data = json.load(resp)
    return data
# Get records from Solr
def get_records(token, query_string, return_fields):
    start = 0
    results = []
    params = {
        'q':query_string,
        'fl': return_fields,
        'rows': rows,
        'start': start
    }
    data = do_query(QUERY_URL, params)
    try:
        results = data['response']['docs']
    except:
        raise Exception('Solr returned unexpected data!')
    num_documents = int(data['response']['numFound'])
    num_paginates = int(math.ceil((num_documents) / (1.0*rows))) - 1
    start += rows
    for i in range(num_paginates):
        params['start'] = start
        data = do_query(QUERY_URL, params)
        try:
            results += data['response']['docs']
        except:
            raise Exception('Solr returned unexpected data!')
        start += rows
    return results
### Main part of script
# get the entries in the input file
try:
    queries = open(query_file).read().strip().split('\n')
except Exception, err:
    sys.exit('Failed to get queries from file: %s'%str(err))
# Now execute the queries
for entry in queries:
    # ignore comment lines
    if entry.startswith('#'):
        continue
    # get file name and query
    fname, query = entry.split('\t')
    # retrieve the records found by the query
    try:
        pubdata = get_records(APItoken, query, fields)
    except Exception, err:
        sys.exit('Failed to get results for query provided: %s\n' % str(err))
    # determine output file
    ofile = "{0}_{1}.tsv".format(fname, dstring)
    # save some data in the records retrieved to the TSV file
    with open(ofile, 'w') as out_file:
        tsv_writer = csv.writer(out_file, delimiter='\t')
        for entry in pubdata:
            properties = entry['property']
            refstatus = 1
            if 'REFEREED' not in properties:
                refstatus = 0
            openaccess = 1
            if 'OPENACCESS' not in properties:
                openaccess = 0
            row = []
            row.append(entry['bibcode'])
            row.append(entry['doi'][0])
            row.append(entry['first_author_norm'])
            row.append(entry['title'][0].encode('utf-8'))
            row.append(refstatus)
            row.append(openaccess)
            tsv_writer.writerow(row)

