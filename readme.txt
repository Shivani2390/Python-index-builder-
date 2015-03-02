----INPUT---
All the data and index files in the compressed format.

----OUTPUT----
An inverted index for all the data files.

----PROGRAM----
The program performs the following operations-
1. Uncompress a pair of the data and index file from the input files.
2. Based on the values in the index files, parse the respective data file.
3. Parse all the content of all URLs present in each data file.
4. Get the frequency, position of the word (with respect to the beginning of the file) and the context for each word present in the webpage. This is the temporary posting for each word in that data file. We also store the Document ID which is an integer generated from the respective index file based on the size of the webpage.
5. Once all the temporary postings for a data file is created, it is written to the postings file on disk.
6. After all the temporary postings file has been created, we perform a unix sort which sorts all the postings files and merges them into one 'FinalPostings.txt' file which is then written in compressed format to the disk. 
7. Using this 'final postings' file we create the 'InvertedIndex.txt' file and the 'lexicon'.
8. Clean up / delete all the temporary postings files and the 'final postings' file as these were required only temporarily.
9. Finally, we compress the 'InvertedIndex.txt' binary file.

NOTE: 
Unix Sort is implemented using shell scripting, which is called through the Python code. Filename - "sort.sh"
Compressing and uncompressing a file is implemented using shell scripting, which is called through the Python code. Filename - "unzip.sh"
'wordList' is a lexicon data structure gets loaded into the main memory and remains there. This will be used for processing queries.
'urls' is a simple data structure that contains the mapping of the Document ID to url. This is required after we finish processing the query and want to display the urls as a search result.


----CONFIGURATION / EXECUTE----
1. All the input files should be stored in the same folder and the path of the this folder should be mentioned in the "build_index.py" file (Line no : 139)
2. Make sure all three shell script files have the correct access rights for the user, if not use the command chmod 777 filename.sh 
3. Save the "build_index.py", "unzip.sh", "sort.sh", "zip.sh" in the same folder and run the command python build_index.py to run the program. The output file appears in the same folder.

----MODULES / FUNCTIONS----
Class Parser that parses to eliminate the tags and find out the words present in the cached web pages in order to build up the lexicon. The class parser has methods handle_starttag that gets the start tag, handle_endtag that handles the end tag and handle_data that handles the data, finds out the word and store it in the temporary word list which is being maintained for every data page we get.

createIndex function parses the index file associated with the data file and get all the urls in the index page for that particular data page which is appended in the url list.
 
buildLexi function builds up the lexicon after we have got all the words and their postings have been built. The postings have redundant words from which only distinct words are taken and they are used to build up the lexicon. The postings are written to a seperate file.

writeBinary function writes the file in binary format.

Modules are script files unzip.sh, sort.sh and zip.sh. The script unzip.sh unzips the file passed in as an argument. The script sort.sh sorts the unsorted files by the word . It uses unix sort to sort the files and merge them in a single file. The script zip.sh cleans up all the temporary postings files and compresses the final file conatining the inverted index data.     

----DATA STATISTICS / RUNNING TIME----
Time required to execute the code for the NZ2 dataset is approximately 60 mins.
The size of the output file i.e. the 'InvertedIndex.txt' is 31.3 MB (after compression)


----LIMITATION----
Currently supported for Unix-based operating systems only as we are using unix shell scripting.

