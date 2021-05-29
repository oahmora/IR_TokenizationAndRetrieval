import re
import operator
import csv
from parsing import createInvertedLists

def createFiles():
	createInvertedLists()

def createIndexFromFile(filename):
	try:
		inFile = open(filename, "r")
	except FileNotFoundError:
		print(filename + " does not exist. Generating...")
		createFiles()
	
	index = {}
	with inFile as f:
		reader = csv.reader(f, delimiter='\t')
		for row in reader:
			index[row[1]] = row[0]
	return index		
	
def findAndSplit(f, offset):
	string = f.seek(offset)
	string = f.readline()
	
	string = string.replace('\t', ' ')
	#string = string.replace(':', ' ')
	string = string.split()
	return string
	
def getTermInfo(term_id):
	term_info_dict = {}
	term_index_dict = {}
	
	with open("term_info.txt", 'r') as f:
		info = f.read()
		term_offset = info.index(str(term_id) + '\t')
		#term_offset = word, offset, total documents, distinct documents
		term_info = findAndSplit(f, term_offset)
		term_info_dict[term_id] = {'Total': term_info[2], 'Distinct': term_info[3]}
	
	inFile = open("term_index.txt", "r")
	#term_index = word, doc, position, doc, position, ...
	term_index = findAndSplit(inFile, term_offset)
	
	for i in range(1, len(term_index)):
		if term_index[i].partition(":")[0] not in term_index_dict:
			term_index_dict[term_index[i].partition(":")[0]] = [term_index[i].partition(":")[2]]
		else:
			term_index_dict[term_index[i].partition(":")[0]].append(term_index[i].partition(":")[2])
	return(term_info_dict, term_index_dict)