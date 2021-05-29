import re
import os
import sys
import math
from irfunctions import tokenize
from parsing import termID, termInfo, docID, docCorpus

def cosineSim(query, document):
	querySize = len(query)
	totalDocs = len(docID.keys())	###total docs
	doc_tfidf = []
	for i in range(len(query)):
		queryWord = query[i]
		
		#search for the query word in the termInfo bank, then loop through all documents containing the word
		#tfidf for document
		if queryWord in termInfo:
			docIndex = 3
			for z in range(3, len(termInfo[queryWord])):
				if document == termInfo[queryWord][z][0]:
					docIndex = z
			idf = math.log(totalDocs/termInfo[queryWord][1])
			docName = termInfo[queryWord][docIndex][0]
			termDocFreq = termInfo[queryWord][docIndex][1]
			
			tf = termDocFreq / docCorpus[docName][0]
			doc_tfidf.append(tf*idf)
		else:
			doc_tfidf.append(0)
	
	#calculate query tfidf
	query_tfidf = []
	for i in range(len(query)):
		tf = query.count(query[i]) / querySize
		if query[i] in termInfo: 
			idf = math.log(totalDocs/termInfo[query[i]][1])
		else:
			idf = 0
		query_tfidf.append(tf*idf)
	
	#normalize query idf
	docNorm = (sum(number ** 2 for number in doc_tfidf))**(1/2)
	queryNorm = (sum(number ** 2 for number in query_tfidf))**(1/2)
	dotProduct = sum([doc_tfidf[i]*query_tfidf[i] for i in range(len(doc_tfidf))])
	cosineSimilarity = dotProduct / (queryNorm * docNorm)
	
	return cosineSimilarity
	

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
		queryScores[doc] = cosineSim(queryList[key], doc)
	
	sortedScores = sorted(queryScores.items(), key=lambda x:x[1], reverse  = True)
	
	#output documents with their ranks
	for i in range(10):
		outFile.write(str(key) + ' ' + 'Q0' + ' ' + str(sortedScores[i][0]) + ' ' + str(rank) + ' ' + str(sortedScores[i][1]) + ' ' + 'Exp' + '\n')
		rank+=1
outFile.close()