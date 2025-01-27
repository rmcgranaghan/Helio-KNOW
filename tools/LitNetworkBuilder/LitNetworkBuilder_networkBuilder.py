#HelioKnow - Omar Shalaby
# 07/26/22
# Change these fields to use the program
# Input file must be a .JSON file
inFile = "W4" 
adsAPIKey = ''
iterations = 0 #The number of times to traverse the citations chain.
saveADSData = False #Cache the retrieved ADS papers? (overwrites previous runs)
saveStats = True #Save the centrality and degree measures of the network graph? (overwrites previous runs)
#---------------------------------------------------------------------------#
import os
import re
import sys
import math
import json
import requests
import traceback
import colorcet as cc
import networkx as nx
import matplotlib.pyplot as plt
path = os.getcwd()
path = os.path.join(path, 'NetworkMetrics')
try:
    os.mkdir(path)
except:
    pass
#---------- Function Definitions ----------#
def sortDict(inDict):
    '''Function to sort dictionaries based on numerical values of keys'''
    retDict = dict(sorted(inDict.items(), key=lambda x: x[1], reverse=True))
    return retDict
#End of dictionary sorting function ------------#

def buildDatabase(inDict, currBibcodes, currPapers):
    '''Function to loop through a ['docs'] dictionary and return list of needed papers'''
    neededCites = []
    for paper in inDict['docs']:
        if paper['bibcode'] not in currBibcodes:
            currBibcodes.append(paper['bibcode'])
            currPapers['docs'].append(paper)
            
    for paper in currPapers['docs']:  
        try:
            for citation in paper['citation']:
                if citation not in currBibcodes and citation not in neededCites:
                    neededCites.append(citation)
        except:
            pass
    return neededCites
#End of initializing function ------------#
 
def fetchPapers(inList, apiKey, currBibcodes):
    '''Returns a parsed JSON dictionary from the requested ADS Papers'''
    bibString = 'bibcode\n'
    retDict = {'numFound': 0, 'docs': []}
    
    if len(inList) > 200:
        start = 0
        
        while start < len(inList):
            bibString = 'bibcode\n'
            
            for code in inList[start:(start + 201)]:
                bibString = bibString + code + '\n'
                
            bibString = bibString[:-2]
            
            req = requests.post("https://api.adsabs.harvard.edu/v1/search/bigquery",
                     params={"q":"*:*", "wt": "json", "fl": "bibcode,author,title,citation,abstract,keyword","fq":"{!bitset}","rows":200},
                     headers={'Authorization': 'Bearer ' + apiKey},
                     data=bibString)
            if req.status_code != 200:
                print("Failed to pull papers\nADS Request status code:", req.status_code)
            else:
                recieved = json.loads(req.content.decode('utf-8'))
                for paper in recieved['response']['docs']:
                    if paper not in retDict['docs']:
                        retDict['docs'].append(paper)

            start += 200
            
        retDict['numFound'] = len(retDict['docs'])
        return retDict
    #-------------------------------------------#
    for code in inList:
        bibString = bibString + code + '\n'
        
    bibString = bibString[:-2]
    
    req = requests.post("https://api.adsabs.harvard.edu/v1/search/bigquery",
                 params={"q":"*:*", "wt": "json", "fl": "bibcode,author,title,citation,abstract,keyword","fq":"{!bitset}","rows":200},
                 headers={'Authorization': 'Bearer ' + apiKey},
                 data=bibString)
    if req.status_code != 200:
        print("Failed to pull papers\nADS Request status code:", req.status_code)
    else:
        adsPapers = json.loads(req.content.decode('utf-8'))
        print("Requested {} papers, recieved: {}".format(len(inList), len(adsPapers['response']['docs'])))
        retDict = {'numFound': adsPapers['response']['numFound'], 'docs': adsPapers['response']['docs']}
        
    return retDict
#End of paper retrieval function ------------#

def buildNetwork(inPapers):
    '''Function to build network graph structure, returns a tuple of two dicts.
    dict 1: dict of papers (nodes) and their links to other nodes (citations)
    dict 2: dict of papers (nodes) and the count of times they have been cited'''
    links = {}
    counts = {}
    for paper in inPapers['docs']:
        try:
            for citation in paper['citation']:
                
                #Build links
                if paper['bibcode'] not in links:
                    links[paper['bibcode']] = [citation]
                else:
                    links[paper['bibcode']].append(citation)
                        
                #Build count (centrality)
                if citation not in counts:
                    counts[citation] = 1
                else:
                    counts[citation] += 1
        except:
            pass

    return(links, counts)
#End of network building function ------------#

# ====== [Main] ====== #
if __name__ == '__main__':

    #Variables
    heldBibcodes = [] #Will hold all the bibcodes we have
    heldPapers = {'numFound': 0, 'docs': []} #Will hold the actual metadata
    stemList = [] #To find all unique cited bibcodes for coloring purposes

    #File/data loading
    try:
        print("Attempting to open file now.")
        if '.json' in inFile.lower():
            inFile = inFile[:-5]
        dataFile = open('{}.json'.format(inFile), 'r', encoding="utf-8")
    except:
        sys.exit("Data load failed, File '{}' not found.".format(inFile))
    try:   
        initDocs = json.load(dataFile)
        dataFile.close()
        print("Done loading and parsing file.\n")
    except:
        sys.exit("Data load failed, JSON syntax failure.")

    requiredPapers = buildDatabase(initDocs, heldBibcodes, heldPapers)
    
    for i in range(0, (iterations)):
        print("Fetching {} papers from ADS...".format(len(requiredPapers)))
        newData = fetchPapers(requiredPapers, adsAPIKey, heldBibcodes)
        requiredPapers = buildDatabase(newData, heldBibcodes, heldPapers)
        heldPapers['numFound'] = len(heldPapers['docs'])

    graph = nx.Graph()
    citeLinks, citeRanks = buildNetwork(heldPapers)


    if saveADSData:
        #Saving the new paper dictionary for future use to reduce load on ADS
        with open("networkPapers.json", 'w', encoding = 'utf-8') as outFile:
            outFile.write(json.dumps(heldPapers, indent=3, sort_keys = False))
            outFile.write('\n')


    #Finding all the unique bibstems we have for colorization purposes
    print("Finding unique bibstems and number of papers for each bibstem.")
    stemRank = {}
    for bibcode in citeLinks:
        bibStem = re.findall("[A-Za-z!\"#$%&'()*+, \-/:;<=>?@[\\]^_`{|}~]+]*", bibcode)
        bibStem = bibStem[0]
        if bibStem not in stemRank:
            stemRank[bibStem] = 1
        else:
            stemRank[bibStem] += 1
        for citeCode in citeLinks[bibcode]:
            citeStem = re.findall("[A-Za-z!\"#$%&'()*+, \-/:;<=>?@[\\]^_`{|}~]+]*", citeCode)
            citeStem = citeStem[0]
            if citeStem not in stemRank:
                stemRank[citeStem] = 1
            else:
                stemRank[citeStem] += 1
            
    colorDict = {}          
    stemRank = sortDict(stemRank)
    
    if saveStats:
        with open("{}\\journalCounts.txt".format(path), "w", encoding = "utf-8") as r:
            for el in stemRank:
                r.write(str(el) + ": " + str(stemRank[el]) + "\n")            
         
    

    print("Adding papers to network.")
    #Adding the papers as nodes to the graph.
    for paper in citeRanks:
        graph.add_node(str(paper))
    #Adding the links/connections between the nodes.
    for paper in citeLinks:
        for cite in citeLinks[paper]:
            graph.add_edge(paper, cite)
            
    print("Constructing color index.")

    i = 255
    for stem in stemRank:
        if stemRank[stem] not in colorDict:
            colorDict[stemRank[stem]] = cc.kbc[i]
            i -= 2

    colorMap = []
    for paper in graph:
        stem = re.findall("[A-Za-z!\"#$%&'()*+, \-/:;<=>?@[\\]^_`{|}~]+]*", paper)
        stem = stem[0]
        colorMap.append(str(colorDict[stemRank[stem]]))
    
    print("Drawing network graph.")
    fig, ax = plt.subplots(nrows=1, ncols=1)
    nx.draw(graph, node_color = colorMap, edge_color = '#42f780', width = 2)
    ax.set_facecolor('#1b202d')
    ax.axis('off')
    fig.set_facecolor('#1b202d')
    plt.show()
   
    print("Calculating centrality measures.")
    degCent = nx.degree_centrality(graph)
    subCent = nx.subgraph_centrality(graph)
    betCent = nx.betweenness_centrality(graph)
    
    if saveStats:
        with open("{}\\Degree Centrality.txt".format(path), "w", encoding="utf-8") as statFile:
            statFile.write("|==============[ Degree Centrality ]==============|\n")
            for node in degCent:
                statFile.write(str(node) + ": " + str(degCent[node]) + '\n')
        print("Degree centrality saved successfully.")
                
        with open("{}\\Subgraph Centrality.txt".format(path), "w", encoding="utf-8") as statFile:
            statFile.write("|==============[ Subgraph Centrality ]==============|\n")
            for node in subCent:
                statFile.write(str(node) + ": " + str(subCent[node]) + '\n')
        print("Subgraph centrality saved successfully.")
        
        with open("{}\\Betweenness Centrality.txt".format(path), "w", encoding="utf-8") as statFile:
            statFile.write("|==============[ Betweenness Centrality ]==============|\n")
            for node in betCent:
                statFile.write(str(node) + ": " + str(betCent[node]) + '\n')
        print("Betweenness centrality saved successfully.")
            
    paperDeg = {}
    for paper in citeRanks:
        paperDeg[paper] = 0
        try:
            paperDeg[paper] += citeRanks[paper]
            paperDeg[paper] += len(citeLinks[paper]) 
        except(KeyError):
            pass

    paperDeg = sortDict(paperDeg)
    if saveStats:
        with open("{}\\Bibcode Degrees.txt".format(path), "w", encoding="utf-8") as statFile:
            statFile.write("|==============[ Bibcode Degrees ]==============|\n")
            for paper in paperDeg:
                statFile.write(str(paper) + ": " + str(paperDeg[paper]) + '\n')

    degDict = {}
    for bibcode in paperDeg:
        if paperDeg[bibcode] not in degDict:
            degDict[paperDeg[bibcode]] = 1
        else:
            degDict[paperDeg[bibcode]] += 1
    if saveStats:   
        with open("{}\\Degree Distribution.txt".format(path), "w", encoding="utf-8") as statFile:
            statFile.write("|==============[ Degree Distribution ]==============|\n")
            for paper in degDict:
                statFile.write(str(paper) + ": " + str(degDict[paper]) + '\n')
                
    paperStats = {}
    #print(traceback.format_exc())
    for paper in heldPapers['docs']:
        bibcode = paper['bibcode']
        try:
            title = paper['title'][len(paper['title']) - 1]
            author = paper['author'][0]
        except:
            title = None
            author = None
        try:
            citeCount = len(paper['citation'])
        except:
            citeCount = 0
        try:
            refCount = paperDeg[bibcode] - citeCount
        except:
            refCount = 0
        try:
            degree = paperDeg[bibcode]
        except:
            degree = refCount + citeCount
        try:
            degCentrality = degCent[bibcode]
        except:
            degCentrality = None
        try:
            betCentrality = betCent[bibcode]
        except:
            betCentrality = None
        try:
            subCentrality = subCent[bibcode]
        except:
            subCentrality = None
        paperStats[bibcode] = {"title": title,
                               "author": author,
                               "degree": citeCount + refCount,
                               "citations": citeCount,
                               "references": refCount,
                               "degree centrality": degCentrality,
                               "betweenness centrality": betCentrality,
                               "subgraph centrality": subCentrality}
        
    
    if saveStats:
        with open("{}\\paperStats.json".format(path), "w", encoding="utf-8") as statFile:
            statFile.write(json.dumps(paperStats, indent=4, sort_keys=False))
        
    print("Creating centrality plots.")
    #Plotting centrality
    fig, (ax1,ax2,ax3) = plt.subplots(1, 3)
    cenX = []
    degY = []

    betY = []
    subY = []

    for point in citeRanks:
        cenX.append(citeRanks[point])
        degY.append(degCent[point])

    for point in citeRanks:
        betY.append(betCent[point])

    for point in citeRanks:
        subY.append(subCent[point])    

    ax1.bar(x = cenX, height = degY, color = 'r')
    ax1.set_xlabel('Num. of Citations')
    ax1.set_title('Degree Centrality')

    ax2.bar(x = cenX, height = betY, color = 'b')
    ax2.set_xlabel('Num. of Citations')
    ax2.set_title('Betweenness Centrality')

    ax3.bar(x = cenX, height = subY, color = 'm')
    ax3.set_xlabel('Num. of Citations')
    ax3.set_title('Subgraph Centrality')

    plt.show()
    logX = []
    logY = []
    for el in list(degDict):
        logX.append(math.log(el,10))
    for el in list(degDict.keys()):
        logY.append("{:.2f}".format(math.log(el,10)))

    degDict = sortDict(degDict)
    fig, ax4 = plt.subplots()
    ax4.bar(range(len(degDict)), logX, tick_label = logY)
    ax4.set_title("Log Log Degree distribution")
    
    plt.show()
    
print("Done!")
#End of main ----------------------#

#EOF
