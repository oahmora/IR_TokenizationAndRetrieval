# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.
from irfunctions import createIndexFromFile, getTermInfo, createFiles
from parsing import doStem
import sys

termID_index = createIndexFromFile("termids.txt")
docID_index = createIndexFromFile("docids.txt")

if (len(sys.argv) == 2):
	if(sys.argv[1] == 'parse'):
		createFiles()

if(len(sys.argv) == 3):
	
	if(sys.argv[1] == '--term'):
		w = doStem(sys.argv[2])
		term_id = termID_index[w]
		term_info, term_index = getTermInfo(termID_index[w])
		
		print("Listing for term (stemmed): ", w)
		print("TERMID: ", term_id)
		print("Number of documents containing term: ", term_info[term_id]['Distinct'])
		print("Term frequency in corpus: ", term_info[term_id]['Total'])

	if(sys.argv[1] == '--doc'):
		doc = sys.argv[2].upper()
		docIndex = docID_index[doc]
		print("Listing for document: ", doc)
		print("DOCID: ", docIndex)
		print("Distinct terms: ", docCorpus[doc][1])
		print("Total terms: ", docCorpus[doc][0])

if(len(sys.argv) == 5):
	w = doStem(sys.argv[2])
	if(sys.argv[1] == '--term' and sys.argv[3] == '--doc'):
		term_id = termID_index[w]
		term_info, term_index = getTermInfo(termID_index[w])
		doc = sys.argv[4].upper()
		docIndex = docID_index[doc]
		
		print("Inverted list for term: ", w)
		print("In document: ", doc)
		print("TERMID: ", term_id)
		print("DOCID: ", docIndex)
		print("Term frequency in document: ", len(term_index[docIndex]))
		print("Positions: ", term_index[docIndex])

