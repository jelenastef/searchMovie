import sys
import re
import json
from movie import Movie

def printMovies(movieList):
	for movie in movieList:
		print(movie.name, movie.year, movie.imdbURL, movie.dbPediaURL)
		
def printXML(movieList, name):
	file = open(name + ".xml", "w")
	file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
	file.write ("<actor name=\"" + name + "\">\n")
	for movie in movieList:
		str = movie.toXML()
		file.write(str.encode('utf8')) 
	file.write("</actor>\n")
	file.close()
	
def printCSV(movieList,name):
	file = open(name + ".csv", "w")
	for movie in movieList:
		str = movie.toCSV()
		file.write(str.encode('utf8'))
	file.close()

def printJSON(movieList,name):
	file = open(name + ".json", "w")
	file.write("{\"actor\": {\"_name\": \"" + name +"\" , \"movie\":")
	json_string = json.dumps([ob.__dict__ for ob in movieList], ensure_ascii=False).encode('utf8')
	file.write(json_string)
	file.write("}}")
	file.close()

def checkNameFormat(nameList):
	if (not nameList) :
		print ("Wrong name format!")
		return False
		
	if len(nameList) < 2:
		nameList = nameList[0].split("_")
		if (not nameList) or (len(nameList) < 2):
			print ("Wrong name format!")
			return False
			
	pattern = r'^[A-Z][a-z]*$'
	for i in range(len(nameList)):
		if re.match(pattern, nameList[i]) == None:
			nameList[i] = nameList[i][0].upper() + nameList[i][1:].lower()
			
	return True

	
def removeParentheses(name):
	#if there's some parentheses in name with year, we don't want that
	pattern = r'^.+\([0-9][0-9].*\)+.*$'
	if re.match(pattern, name) != None:
		index = name.rfind('(')
		if (index != -1):
			name = name[0 : index]
			

def parseNameFromURL(url):
	index = url.rfind('/')
	name = url[index+1 : len(url)]
	name = name.replace("_"," ")
	#if there's some parenthesess in name with year, we don't want that
	removeParentheses(name)
	return name.strip()
	
#~ #merge movieList2 to movieList1
def mergeLists(imdbList, dbPediaList):
	#pattern for some special case matching
	pattern = r'\s+|-+|__+|\\+|/+'
	for movie in dbPediaList:
		match = next((x for x in imdbList if x.name == movie.name), None)
		#if no match, add movie
		if (match == None):
			#give it one more try, remove special characters
			mn = re.sub(pattern, '',movie.name)
			match = next((x for x in imdbList if re.sub(pattern, '', x.name) == mn), None)
			if (match == None):
				imdbList.append(movie)
				continue
		#adding year/movie from list2 if necessary
		if (movie.year != "Missing"):
			if (match.year == "Missing" ):
				match.year = movie.year
			#special, but rare case
			elif(int(match.year) != int(movie.year)):
				print ("Movies from the sources has same name (" + match.name + ") but different years ("+str(match.year) + ","+str(movie.year)+").")
				imdbList.append(movie)
				continue
		
		#adding list2 url
		if (match.dbPediaURL == "None"):
			match.dbPediaURL = movie.dbPediaURL
		else:
			#it seems there's some wierd situation with movie names in dbpedia, append the url to already existing url
			match.dbPediaURL += ";" + movie.dbPediaURL

			