#Omar Shalaby - 7/22/22
#Imports block
import os
import re
import sys
import nltk
import json
import logging
import argparse
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#==========================# 
# Prep tools/variables/folder
lemm = WordNetLemmatizer()
LOG = logging.getLogger('HelioMatch')
logging.basicConfig(level=logging.INFO)
stopWords = list(stopwords.words('english'))
punct = "#$%&'()*+,\.\/:;<=>?@[\\]^_`{|}~]+]*"
# Path preparation
path = os.getcwd()
path = os.path.join(path, 'Data')
try:
    os.mkdir(path)
except:
    pass
#==========================# 
# Function definitions
def sortDict(inDict):
    '''Function to sort dictionaries based on numerical values of keys'''
    retDict = dict(sorted(inDict.items(), key=lambda x: x[1], reverse=True))
    return retDict
# End of dictionary sorting function ==================================|


def analyzeBib(paperCode):
    '''Function to analyze the bibcode of a paper to see which bibstem it belongs to, True for Heliophysics related.'''
    biblist = ['SpWea','GeoRL','JGR','JGRA','JGRE','LRSP','STP','P&SS',
            'Ap&SS','SoPh','RvGSP','SSRv','AcAau','AcA','SLSci','SpReT',
            'AdAnS','AdA&A','AASP','AdAp','AdAtS','AdGeo','AdSpR','ASPRv',
            'AurPh','JComp','JPCom','Cmplx','LRCA','ApL', 'FrASS', 'E&SS']

    bibCode = re.findall("[A-Za-z!\"#$%&'()*+, \-/:;<=>?@[\\]^_`{|}~]+]*[0-9]*", paperCode)
    bibCode = bibCode[0]

    if bibCode in biblist: 
        LOG.debug("Matched bibcode: {}".format(paperCode))
        return True
    else:
        return False
# End of bibcode matching function ==================================|


def analyzeTxt(inPaper, wordsList, threshHold):
    '''Function to process the abstract and title of a paper using a list of keywords'''
    global punct
    global stopWords
    global paperCount
    matches = {}
    totalMatches = 0 
    terms = wordsList

#==========================#
    # Removing punctuation from abstract
    pAbs = inPaper['abstract']
    for char in pAbs:
        if char == '-':
            pAbs = pAbs.replace(char, " ")
        elif char in punct:
            pAbs = pAbs.replace(char, '')
            
    # Removing stop words from abstract
    pAbs = pAbs.split()
    for word in pAbs:
        if word in stopWords:
            LOG.debug("Removed: {} from abstract".format(word))
            pAbs = [keep for keep in pAbs if keep != word]

    # Lemmatizing abstract
    for word in pAbs:
        if not isAcronym(word):
            word = lemm.lemmatize(word)
#==========================#       
    # Removing punctuation from title
    pTitle = inPaper['title'][len(inPaper['title'])-1]
    for char in pTitle:
        if char == '-':
            pTitle = pTitle.replace(char, " ")
        elif char in punct:
            pTitle = pTitle.replace(char, '')

    # Removing stop words from title
    pTitle = pTitle.split()
    for word in pTitle:
        if word in stopWords:
            LOG.debug("Removed: {} from title".format(word))
            pTitle = [keep for keep in pTitle if keep != word]
     
    # Lemmatizing title
    for word in pTitle:
        if not isAcronym(word):
            word = lemm.lemmatize(word.lower())
#==========================#
    #Phrase matching
    for word in terms:
        if " " in word:
            if word in pAbs or word in pTitle:
                if word not in matches:
                    matches[word] = 1
                else:
                    matches[word] += 1
#==========================#                        
    # Abstract matching
    for word in pAbs:
        if isAcronym(word):
            continue
        
        for key in terms:
            if word == key:
                LOG.debug("Matched '{}' with '{}' in paper# {}'s abstract.".format(word, key, paperCount))
                if word not in matches:
                    matches[word] = 1
                else:
                    matches[word] += 1
#==========================# 
    # Title matching
    for word in pTitle:
        if isAcronym(word):
            continue
        
        for key in terms:
            if word == key:
                LOG.debug("Matched '{}' with '{}' in paper# {}'s title.".format(word, key, paperCount))
                if word not in matches:
                    matches[word] = 1
                else:
                    matches[word] += 1
#==========================# 
    # Tally matches and final decision
    for el in matches:
        totalMatches = totalMatches + matches[el]

    if totalMatches >= threshHold:
        matches = sortDict(matches)
        matches["TotalMatches"] = totalMatches
        inPaper["MatchedWords"] = matches
        LOG.debug("Paper word match success for paper#: {}".format(paperCount))
        return True
    return False
# End of text analysis function =====================================|


def isAcronym(inWord):
    '''Function to identify acronyms, if 50% or more of the character are captilaized, it is an acronym'''
    capCount = 0

    if inWord.isupper():
        return True
        
    for letter in inWord:
        if letter.isupper():
            capCount += 1
            
    if ((capCount / len(inWord)) * 100) >= 50:
        LOG.debug("Word {} detected as acronym".format(inWord))
        return True
    
    return False
# End of acronym rejection function ===================================|

# ====== [Main] ====== #
if __name__ == '__main__': 

    ap = argparse.ArgumentParser(description='Extracts papers about Heliophysics topics from ADS Data')

    ap.add_argument('-i', '--inFile', type=str, help='Data file to analyze', required=True)
    ap.add_argument('-d', '--debug', default = False, action = 'store_true', help='Turn on debugging messages')
    ap.add_argument('-o', '--outFile', type=str, default = 'matchedPapers.json', help='Save files to path\\fileName')
    ap.add_argument('-w', '--wordCount', type=int, default = 7, help='Number of words to consider a paper heliophysics based if mode 2 or 3 are selected, defaults to 7')
    ap.add_argument('-m', '--mode', type=int, default = 1, help='Mode selection to match papers\n"1" - for bibcode only (default)\n"2" - for bibcode AND abstract\n"3" - for bibcode OR abstract')

    args = ap.parse_args()

    failures = 0
    matchCount = 0
    progPrint = True

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        LOG.setLevel(logging.DEBUG)
        progPrint = False
    # Opening data file.
    try:
        file = open("{}".format(args.inFile), 'r', encoding="utf-8")
        print("\nLoading data file, please wait.")
        LOG.debug("Provided file name: '{}'".format(str(args.inFile)))
    except:
        LOG.debug("Provided file name (Failed): '{}'".format(args.inFile))
        sys.exit("File load failed, check input file.")

    # Load data file into JSON dict.
    try:
        docs = json.load(file)
        file.close()
        print("Done loading and parsing file.")
    except:
        sys.exit("Data load failed, JSON syntax failure.")

    # Preparing output file and JSON structure.
    out = open("{path}\\{fileName}.json".format(path = path, fileName = args.outFile), 'w', encoding="utf-8")
    matchedPapers = {"numFound": 0, "docs": []}

    #   Mode 1 - Bibcode only           #
    if args.mode == 1:
        LOG.debug("MODE 1 SELECTED")
        # Analyze papers.
        print("\nAnalyzing papers:")
        paperCount = 1
        for paper in docs['docs']:
            try:
                if analyzeBib(paper['bibcode']):
                    matchCount += 1
                    matchedPapers["numFound"] = matchCount
                    matchedPapers["docs"].append(paper)
                else:
                    pass
                if progPrint:
                    prog = round((paperCount / docs['numFound']) * 40)
                    print('[' + ('=' * prog) + ('-' * (40 - prog)) + ']\t' + str(paperCount) + 
                          " out of " + str(docs['numFound']) + " papers (" + str(round((paperCount / docs['numFound']) * 100)) + "%)", end='\r')
                paperCount += 1
            except (KeyError):
                failures += 1
                paperCount += 1

    #   Mode 2 - Bibcode AND abstract   #
    elif args.mode == 2:
        LOG.debug("MODE 2 SELECTED")
        
        with open('matchKeys.txt', 'r') as termFile:
            termsIn = termFile.readlines()
            terms = []
            for line in termsIn:
                terms.append(line[:-1])
            
        c = 0
        # Removing punctuation from terms
        for word in terms:
            if " " in word:
                for sub in word.split():
                    for char in sub:
                        if char == '-':
                            temp = sub.split('-')
                            if len(temp[0]) == 1:
                                new = sub.replace(char, '')
                                terms[c] = word.replace(sub, new)
                            else:
                                new = sub.replace(char, ' ')
                                terms[c] = word.replace(sub, new)
                                
            else:     
                for char in word:
                    if char == '-':
                        temp = word.split('-')
                        if len(temp[0] == 1):
                            terms[c] = word.replace(char, '')
                        else:
                            terms[c] = word.replace(char, ' ')
                            
                    elif char in punct:
                        terms[c] = word.replace(char, '')
            c += 1
        
        # Removing stop words from terms
        c = 0
        for word in terms:
            if " " in word:
                continue

            else:
                if word in stopWords:
                    terms = [keep for keep in terms if keep != word]
            c += 1
        # Lemmatizing terms
        c = 0
        for word in terms:
            new = ""
            if " " in word:
                for sub in word.split():
                    new = new + lemm.lemmatize(sub) + " "
                new = new[:-1]
                terms[c] = new
            else:
                terms[c] = lemm.lemmatize(word)
            c += 1

        #Seeing prepared terms       
        with open("lemmatizedKeys.txt", "w", encoding = "utf-8") as testFile:
            for el in terms:
                testFile.write(el + "\n")
                
        # Analyze papers.
        print("\nAnalyzing papers:")
        paperCount = 1
        for paper in docs['docs']:
            try:
                if analyzeBib(paper['bibcode']) and analyzeTxt(paper, terms, args.wordCount):
                    matchCount += 1
                    matchedPapers["numFound"] = matchCount
                    matchedPapers["docs"].append(paper)
                    
                if progPrint:
                    prog = round((paperCount / docs['numFound']) * 40)
                    print('[' + ('=' * prog) + ('-' * (40 - prog)) + ']\t' + str(paperCount) +
                          " out of " + str(docs['numFound']) + " papers (" + str(round((paperCount / docs['numFound']) * 100)) + "%)", end='\r')
                paperCount += 1
            except (KeyError):
                failures += 1
                paperCount += 1

    #   Mode 3 - Bibcode OR abstract   #
    elif args.mode == 3:
        LOG.debug("MODE 3 SELECTED")
        
        with open('matchKeys.txt', 'r') as termFile:
            termsIn = termFile.readlines()
            terms = []
            for line in termsIn:
                terms.append(line[:-1])
                
        c = 0
        # Removing punctuation from terms
        for word in terms:
            if " " in word:
                for sub in word.split():
                    for char in sub:
                        if char == '-':
                            temp = sub.split('-')
                            if len(temp[0]) == 1:
                                new = sub.replace(char, '')
                                terms[c] = word.replace(sub, new)
                            else:
                                new = sub.replace(char, ' ')
                                terms[c] = word.replace(sub, new)
                                
            else:     
                for char in word:
                    if char == '-':
                        temp = word.split('-')
                        if len(temp[0] == 1):
                            terms[c] = word.replace(char, '')
                        else:
                            terms[c] = word.replace(char, ' ')
                            
                    elif char in punct:
                        terms[c] = word.replace(char, '')
            c += 1
        
        # Removing stop words from terms
        c = 0
        for word in terms:
            if " " in word:
                continue

            else:
                if word in stopWords:
                    terms = [keep for keep in terms if keep != word]
            c += 1
        # Lemmatizing terms
        c = 0
        for word in terms:
            new = ""
            if " " in word:
                for sub in word.split():
                    new = new + lemm.lemmatize(sub) + " "
                new = new[:-1]
                terms[c] = new
            else:
                terms[c] = lemm.lemmatize(word)
            c += 1

        #Seeing prepared terms       
        with open("lemmatizedKeys.txt", "w", encoding = "utf-8") as testFile:
            for el in terms:
                testFile.write(el + "\n")

        # Analyze papers.
        print("\nAnalyzing papers:")
        paperCount = 1
        for paper in docs['docs']:
            try:
                if analyzeBib(paper['bibcode']) or analyzeTxt(paper, terms, args.wordCount):
                    matchCount += 1
                    matchedPapers["numFound"] = matchCount
                    matchedPapers["docs"].append(paper)
                    
                if progPrint:
                    prog = round((paperCount / docs['numFound']) * 40)
                    print('[' + ('=' * prog) + ('-' * (40 - prog)) + ']\t' + str(paperCount) +
                          " out of " + str(docs['numFound']) + " papers (" + str(round((paperCount / docs['numFound']) * 100)) + "%)", end='\r')
                paperCount += 1
            except (KeyError):
                failures += 1
                paperCount += 1
                
    # Failure to select mode
    else:
        sys.exit("Mode selection failed.")

# END anaylsis, finalize file and exit.    
    out.write(json.dumps(matchedPapers, indent=3, sort_keys = False))
    out.write("\n")
    out.close()
    print("\n\nMatched", matchCount, "papers out of", paperCount - 1)
    print("Number of corrupted papers encountered:", failures)
    sys.exit("\nAll done!\n")
# End of main function
    
