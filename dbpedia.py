from SPARQLWrapper import SPARQLWrapper,JSON
from movie import Movie
import re
import utils

class DbPediaSearch:

	@staticmethod
	def __sendQuery(query):
		sparql = SPARQLWrapper("http://dbpedia.org/sparql")
		sparql.setReturnFormat(JSON)
		sparql.setQuery(query)  # the previous query as a literal string
		return sparql.query().convert()
	
	@staticmethod
	def __queryForActorsMovies(name):
		actor = "http://dbpedia.org/resource/" + name
		return "PREFIX dbo:     <http://dbpedia.org/property/> \
		PREFIX dbpedia: <http://dbpedia.org/ontology/> \
		SELECT ?movie \
		WHERE {?movie dbo:starring <"+actor+">.}"
	
	@staticmethod
	def __getYear(movieURL):
		pattern = r'^.+\(.*([0-9][0-9][0-9][0-9]).*\)+.*$'
		match = re.match(pattern, movieURL)
		if match != None:
			return match.group(1)
		return "Missing"
		
	@staticmethod
	def search(nameList, movieList,nameListOriginal):
		name = "_".join(nameList)
		print(name)
		query = DbPediaSearch.__queryForActorsMovies(name)
		results = DbPediaSearch.__sendQuery(query)
		
		#give another try with name, but this will not cover all cases of cours
		if (not results["results"]["bindings"]):
			name = "_".join(nameList[::-1])
			print("Trying " +  name + "...")
			query = DbPediaSearch.__queryForActorsMovies(name)
			results = DbPediaSearch.__sendQuery(query)
		
		#give another try with name, use original which user set, maybe user knows what he/she is doing
		if (not results["results"]["bindings"]):
			name = "_".join(nameListOriginal)
			print("Last shot, trying " +  name + "...")
			query = DbPediaSearch.__queryForActorsMovies(name)
			results = DbPediaSearch.__sendQuery(query)
			
		if (not results["results"]["bindings"]):
			print("Actor not found on Dbpedia!")
			return
		
		#iterate true movie results and add them to the list
		for result in results["results"]["bindings"]:
			movieURL = result["movie"]["value"]
			
			#search for official title of the movie on movie page
			query1 = "PREFIX dbo:     <http://dbpedia.org/property/> \
			SELECT ?title \
			WHERE { <"+movieURL+"> dbo:name ?title.} "
			results1 = DbPediaSearch.__sendQuery(query1)
			
			movieName = ""
			if results1["results"]["bindings"]:
				movieName = results1["results"]["bindings"][0]["title"]["value"]
			else:
			#if no name property on movie page or more than one name in name property, try parsing movie name from url string
				movieName = utils.parseNameFromURL(movieURL)
				#print(movieName.encode('utf'))
				
			#there's no year property on dbmedia, so try to get a year from the movie url
			year = DbPediaSearch.__getYear(movieURL)
			
			movieList.append(Movie(movieName, year, "None", movieURL))
			
		