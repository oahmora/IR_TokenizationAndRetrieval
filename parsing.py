import re
import os
import zipfile
import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()

def createInvertedLists():
	# Regular expressions to extract data from the corpus
	doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
	docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
	text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

	termInfo = {}
	docID = {}
	termID = {}

	#for bigram
	docTerms = {}

	with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
		zip_ref.extractall()

	# Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
	for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
		allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]


	docIndexNo 	= 1000000
	termIndexNo = 2000000
	docCorpus = {}
	for file in allfiles:
		with open(file, 'r', encoding='ISO-8859-1') as f:
			filedata = f.read()
			result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
		
		for document in result[0:]:
			# Retrieve contents of DOCNO tag
			docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
			# Retrieve contents of TEXT tag
			text = "".join(re.findall(text_regex, document))\
				.replace("<TEXT>", "").replace("</TEXT>", "")\
				.replace("\n", " ")
			
			# step 1 - lower-case words, remove punctuation, remove stop-words, etc.
			# step 2 - create tokens, then remove stop-words and stem words
			tokens = tokenize(text)
			docTerms[docno] = tokens	#for bigram only
			
			# step 3 - build index
			docID[docno] = docIndexNo
			docIndexNo += 1
			docCorpus[docno] = [len(tokens), 0]	#number of tokens, number of distinct tokens
			
			position = 0
			for w in tokens:
				if w not in termID:
					termID[w] = termIndexNo
					termIndexNo+=1
					
					#postingList['token ID'] = [word, # of distinct docs, total frequency, {posting list}]
					#postinglist = (doc#, frequency in document, [ position1, position2, .....] ) 
					termInfo[w] = [w, 1, 1, [docno, 1, [position]]]
					
					docCorpus[docno][1] += 1	#distint term in document
				
				#non-distinct doc
				elif(docno in termInfo[w][3]):
					termInfo[w][2] += 1
					termInfo[w][3][1] += 1
					termInfo[w][3][2].append(position)
					#termInfo[w]['Posting list'] = docID[docno]
				
				#distinct doc
				else:
					termInfo[w][1] += 1
					termInfo[w][2] += 1
					termInfo[w].append([docno,1,[position]])
					docCorpus[docno][1] += 1	#distint term in document
					
				position+=1
			
			docIndexNo+=1

	createFileFromIndex('docids.txt', docID)
	createFileFromIndex("termids.txt", termID)
	createFileForTermInfo(termID, termInfo, docID)

def tokenize(text):
	text = text.lower()
	text = re.sub(r'[^\w\s]','',text)
	
	tokens = text.split()
	
	#remove stop words
	file = open("stopwords.txt", "r")
	stop_words = file.read().splitlines()
	for i in stop_words:
		while i in tokens:
				tokens.remove(i)
				
	#stem
	for i in range(0, len(tokens)):
			tokens[i] = ps.stem(tokens[i])
			
	return(tokens)

def doStem(text):
	ps = PorterStemmer()
	return ps.stem(text)
	
def createFileFromIndex(filename, index):
	#output term ids and term names
	outFile = open(filename, 'w')
	for key in index:
		outFile.write(str(index[key]) + "\t" + str(key) + "\n")
		
def createFileForTermInfo(termID, termInfo, docID):
	#output term indexes (term id, docID:pos, docID:pos2, ...)
	#also output term info (term id, offset, total frequency of term, distinct documents with term)
	outFile = open("term_index.txt", 'w')
	outFile2 = open("term_info.txt", 'w')
	for termName in termInfo:
		outFile2.write(str(termID[termName]) + "\t" + str(outFile.tell() + 1) + "\t" + str(termInfo[termName][2]) + "\t" + str(termInfo[termName][1]) + "\n")
		outFile.write((str(termID[termName])))
		for i in range(3, len(termInfo[termName])):
			termPositions = termInfo[termName][i]
			for x in range(len(termPositions[2])):
				outFile.write("\t" + str(docID[termPositions[0]]) + ":" + str(termPositions[2][x]))
		outFile.write("\n")
	outFile.close()