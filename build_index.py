#importing the required libraries
import os
from HTMLParser import HTMLParser
from subprocess import Popen

wordList = {} #contains the list of temporary words, gets refreshed for every new data page
docId = 1
# Modifying the inbuilt functions of the HTMLParser to suit our requirements.
class MyHTMLParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.wordTag = ''
		#list of tags that are being ignored when considering the context of the a word
		self.tagList = ['html', 'head', 'table', 'tr', 'td', 'img', 'br', 'td', 'script', 'tbody', 'meta', 'link', 'input', 'font' ]
		#list of delimiters are are being ignored while parsing the webpage
		self.delimList = [',', '.', '!', '"', ' ', '?', '~', ':', ';', '%', '$', '#', ')', '(', '*', '&', '^', '`', '[', ']', '|', '{', '}', '/', ':', ';', '\'', '<', '>', '=', '-']
		self.dontUseTags = ['body', 'title', 'span']
	def handle_starttag(self, tag, attrs):
		#print "In start tag"
		try:
			if tag not in self.tagList:
				self.wordTag += ' ' + tag
		except HTMLParseError:
			print "Error"
		#print self.wordTag
	def increaseDocId(self):
		docId += 1
		#print self.docId
	def handle_endtag(self, tag):
		#print "In end tag"
		try:
			#print tag + '\n'
			if tag in self.wordTag:
				self.wordTag = self.wordTag.replace(tag + ' ', '')	
		except HTMLParseError:
			print "Error"
		#print self.wordTag
	def handle_data(self, data):
		#print data
		try:
			wordTags = self.wordTag.split() 
			if len(wordTags) > 0: 
				line, index = self.getpos() 
				words = data.split()
				for word in words:
					for delim in self.delimList:
						word = word.strip(delim)	# stripping out the delimiters
					word = word.lower()				# converting the word to lower case
					#print word
					if len(word) >= 3:			# ignoring words like a, an, the,.., length less than 3
						if word not in wordList.keys():
							toAppend = [line, index, wordTags[len(wordTags)-1]]	# appending all the occurrences of a word
							wordList[word] = [docId, 1, toAppend]
						else:       
							toAppend = [line, index, wordTags[len(wordTags)-1]] 
							if docId != wordList[word][0]:
								wordList[word].append([docId, 1, toAppend])
							else:                                                
								wordList[word][1] += 1
								wordList[word].append(toAppend)
						index += 1 
		except HTMLParseError:
			print "Error"


# gets the URLs from the index file and the sizes of the webpage. Its also checks if the page contains 404, or other errors.
def createIndex(fileName, urls):
	size = []
	fileRead = open(fileName)
	indexData = fileRead.read()
	items = indexData.split()
	for index in range(len(items)):
		if index % 7 == 0 and items[index + 6] == 'ok':
			#print items[index + 6]
		 	urls.append(items[index])
		 	size.append(int(items[index+3]))
	fileRead.close()
	return (urls, size)
	
# writes to a file in binary mode
def writeBinary(fileWrite, line):
	for char in line:
		#print char
		byte = ord(char)
		byte = bin(byte)
		#print byte
		fileWrite.write(byte)
		fileWrite.write(' ')

		
def writeFile(fileName):
    fileWrite = open(fileName, 'w')
    for key in wordList.keys():
        fileWrite.write(key + ' ' + str(wordList[key]) + '\n')
    fileWrite.close()

# reads from a binary file
def readBinary(fileName):
	file = open(fileName, 'rb')
	line = ''
	while True:
		char = ''
		read = ''
		while read != ' ':
			read = file.read(1)
			char += read
		char = chr(int(char,2))
		if char != '.':
			line += char
		else:
			#print line
			line = ''
		if not read:
			break
	file.close()

def setSize(size):
	for ind in range(1,len(size)):
		size[ind] -= size[ind-1]
	return size

# Builds the lexicon and the Inverted index from the final postings file.
def buildLexi(fileName):
	fileRead = open(fileName, 'r')
	fileWrite = open('InvertedIndex.txt', 'w')
	data = ''
	for line in fileRead:
		ind = line.find(' ')
		word = line[0:ind].strip()
		if len(wordList) > 0:
			if wordList.has_key(word):
				data += ' ' + line[ind:]
			else:
				wordList[word] = fileWrite.tell()
				writeBinary(fileWrite, data)
				data = ''
		else:
			wordList[word] = fileWrite.tell()
			data = ' ' + line[ind:]
	fileRead.close()
	fileWrite.close()		
		
	
# handles all the communications between the different functions and the calls to the shell scripts.	
def main():
	urls = []
	ind = 0
	for filename in os.listdir("/Users/shivanigupta/Downloads/nz2_merged/"):
		parser = MyHTMLParser()
		wordList.clear()
		#print len(wordList)
		if '_data' in filename:
			Process = Popen(['./unzip.sh ' + filename] , shell=True)
			Process.communicate()
			names = filename.split('_')
			indexFileName = names[0] + '_index'
			Process = Popen(['./unzip.sh ' + indexFileName] , shell=True)
			Process.communicate()
			#print indexFileName
			urls, size = createIndex(indexFileName,urls)
			#size = setSize(size)
			#print size
			fileRead = open(filename, 'r')
			ind += 1
			for index in range(len(size)):
				try:
					parser.feed(fileRead.read(size[index]))
					parser.increaseDocId()
				except:
					pass
					#print "Don't go in"
				#print "File location " + str(fileRead.tell())
				#print "Size :  " + str(size[index]) 
			fileName = "postings" + str(ind) + ".dat"
			#print fileName + ' ' + str(len(wordList))
			writeFile(fileName)
			fileRead.close()
	wordList.clear()
	Process = Popen(['./sort.sh'] , shell=True)
	Process.communicate()
	buildLexi('FinalPostings.dat')
	Process = Popen(['./zip.sh ' + indexFileName] , shell=True)
	Process.communicate()
main()