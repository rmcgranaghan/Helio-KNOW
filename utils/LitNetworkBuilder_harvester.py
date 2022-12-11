import os
import json
import traceback
import requests

#Please provide the ADS token.
token = ''


bibList = ['SpWea','GeoRL','JGR','JGRA','JGRE','LRSP','STP','P&SS',
        'Ap&SS','SoPh','RvGSP','SSRv','AcAau','AcA','SLSci','SpReT',
        'AdAnS','AdA&A','AASP','AdAp','AdAtS','AdGeo','AdSpR','ASPRv',
        'AurPh','JComp','JPCom','Cmplx','LRCA','ApL', 'FrASS', 'E&SS']

fileName = 'AllData'


def sortDict(inDict):
    '''Function to sort dictionaries based on numerical values of keys'''
    retDict = dict(sorted(inDict.items(), key=lambda x: x[1], reverse=True))
    return retDict

path = os.getcwd()
path = os.path.join(path, 'Data')
try:
    os.mkdir(path)
except:
    pass



stats = {}
actual = 0
totalFound = 0
totalRetrieved = 0
papers = {"numFound": totalFound, "docs": []}

#Send requests for each bibtree.
for code in bibList:
    start = 0
    bib = code
    if '&' in bib:
        bib = bib.replace('&', "%26")

    url = 'https://api.adsabs.harvard.edu/v1/search/query?q=bibstem%3A{} year%3A2010-2022'.format(bib)
    headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
     
    response = requests.get(url, headers = headers)
    
    if response.status_code == 200:
        try:
            data = json.loads(response.content.decode('utf-8'))
        except:
            print("Loading JSON failed.")
            traceback.print_exc()
    num = data['response']['numFound']
    #Batching the requests and recieved papers
    while start <= num:
        print("Retrieving {} out of {} papers from {} journal".format(start, num, code))
        url = 'https://api.adsabs.harvard.edu/v1/search/query?q=bibstem%3A{} year%3A2010-2022&fl=bibcode%2Cauthor%2Ctitle%2Ccitation%2Cabstract%2Ckeyword&start={}&rows=200'.format(bib, start)
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer {0}'.format(token)}
        response = requests.get(url, headers = headers)
      
        if response.status_code == 200:
            try:
                data = json.loads(response.content.decode('utf-8'))
            except:
                print("Loading JSON failed.")
                traceback.print_exc()
            stats[code] = int(data['response']['numFound'])         
            for paper in data['response']['docs']:
                actual += 1
                papers["docs"].append(paper)


               
            start += 200
        else:
            print("Query for {} journals failed.".format(code))  
    totalRetrieved = len(papers['docs'])
    totalFound = totalFound + int(data['response']['numFound'])
    papers["numFound"] = totalFound

#Saving the fetched papers to a JSON file  
print("Writing data to file.")
with open('{path}\\{fileName}.json'.format(path = path, fileName), "w", encoding = "utf-8") as outFile:
    outFile.write(json.dumps(papers, indent=3, sort_keys = True))
    outFile.write("\n")
    
stats['numFound'] = totalFound
stats = sortDict(stats)

#Cache some statistics to disk
with open('{path}\\{fileName}.txt'.format(path = path, fileName = 'Stats'), "w", encoding = "utf-8") as statFile:
    statFile.write("|==============[ Statistics ]==============|\n")
    statFile.write("Total retrieved: " + str(totalRetrieved) + '\n')
    for el in stats:
        statFile.write(str(el) + ": " + str(stats[el]) + '\n')

print("\nTotal found: ", totalFound)
print("\nDone!\n")
