# Information Retrieval - Assignment 1 (Tokenization)

## Team member 1 - Omar Hernandez

- Python was used for this project.
- To parse the documents, enter: python3 read_index.py parse
- To run the code for finding information about a term, enter: python3 read_index.py --term <term>
- To run the code to find the information about a document, enter: python3 read_index.py --doc <document>
- To run the code that will find information about a term in a document, enter: python3 read_index.py --term <term> --doc <document>
- read_index.py references the inverted lists to find information about the terms and documents.
- This project uses stemming for both the query and the documents. 
- All of the extra credit was attempted, including stemming, writing inverted list to disc along with the additional files it entails for indexing.
Specific commands:
```bashpython3 read_index.py parse```
```bash python3 read_index.py --term asparagus```
```bash python3 read_index.py --doc ap890101-0001```

# Information Retrieval - Assignment 2 (Retrieval)

## Team member 1 - Omar Hernandez

- Python was used for this project. To run the code, enter: python3 VSM.py <query list text file> <output file>
- This project uses stemming for both the query and the documents. 
- The extra credit was attempted, and it can be run by entering: python3 LM-unigram.py <query list text file> <output file>
- The other part can be run by entering: python3 LM-bigram.py <query list text file> <output file>
Specific commands:
```bash python3 VSM.py query_list.txt output.txt```
```bash python3 LM-unigram.py query_list.txt output2.txt```
```bash python3 LM-bigram.py query_list.txt output3.txt```