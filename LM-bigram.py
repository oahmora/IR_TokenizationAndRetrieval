import re
import os
import sys
import math
from irfunctions import tokenize
from parsing import termID, termInfo, docID, docCorpus, docTerms

def bigram(query, document):
	##need tf, length of document, total distinct words
	
	vocabSize = len(termID.keys())
	querySize = len(query)
	p_laplace = []
	
	for i in range(len(query) - 1):
		queryWord = query[i]
		queryWord2 = query[i+1]
		positions = []
		
		if queryWord in termInfo:
			docIndex = 3
			for z in range(3, len(termInfo[queryWord])):
				if document == termInfo[queryWord][z][0]:
					docIndex = z
					positions = termInfo[queryWord][z][2]
			
			docName = termInfo[queryWord][docIndex][0]
			
			for z in range(len(docTerms[docName])-1):
				if docTerms[docName][z] == queryWord:
					if docTerms[docName][z+1] == queryWord2:
						docLength = docCorpus[docName][0]
						termDocFreq = termInfo[queryWord][docIndex][1]
						
						tf = termDocFreq / docCorpus[docName][0] ###
						p_laplace.append((tf + 1)/(docLength + vocabSize))
	lm_laplace = sum(math.log(number) for number in p_laplace)	
	
	return lm_laplace
	

#postingList['token ID'] = [word, # of distinct docs, total frequency, {posting list}]
#postinglist = (doc#, frequency in document, [ position1, position2, .....] ) 
queryList = {}
inFile = open(sys.argv[1], "r")
while True:
	line = inFile.readline()
	if not line:
		break
	
	queryText = tokenize(line)
	queryList[queryText[0]] = queryText[1:]
inFile.close()

outFile = open(sys.argv[2], 'w')
for key in queryList:
	queryScores = {}
	rank = 1
	for doc in docID:
		queryScores[doc] = bigram(queryList[key], doc)
	
	sortedScores = sorted(queryScores.items(), key=lambda x:x[1], reverse  = False)
	
	#output documents with their ranks
	for i in range(10):
		outFile.write(str(key) + ' ' + 'Q0' + ' ' + str(sortedScores[i][0]) + ' ' + str(rank) + ' ' + str(sortedScores[i][1]) + ' ' + 'Exp' + '\n')
		rank+=1
outFile.close()