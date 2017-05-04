import sys
import argparse
from imdbSearch import IMDBSearch
from dbpedia import DbPediaSearch
import utils

def searchForMovies(source,nameList, movieListImdb, movieListDBPedia, nameListOriginal):
	if (source == "imdb" or source == "all"):
		print("Searching name on IMDB...")
		IMDBSearch.search(nameList, movieListImdb)
		print("IMDB search done.")

	if (source == "dbpedia" or source == "all"):
		print("Searching name on DbPedia...")
		DbPediaSearch.search(nameList, movieListDBPedia, nameListOriginal)
		print("DbPedia search done.")
		
#main function
def Run():
	parser = argparse.ArgumentParser(description='Search for actor\'s movies on imdb and/or dbpedia')
	parser.add_argument('--actor','-a', metavar='<name>',nargs='+',
						help='Name of an actor/actress e.g. Tom Hanks.', required=True)
	parser.add_argument('--source','-s', metavar='<sourceName>', choices=['imdb','dbpedia','all'],  default = "all",
						help='Source(s) for searching movies, values can be imdb, dbpedia or all. Default is all.')
	parser.add_argument('--format', '-f', metavar='<formatType>', choices=['json','xml','csv', 'all'], default = "all",
						help='Format of output for searching movies, values can be xml, csv, json or all. Default is all.')

	args = parser.parse_args()
	#using nameList, it's sutable for dbpedia and for checking the results of imdb
	nameList = args.actor
	#nameListOriginal is needed for dbpedia in case of actor name is something like Leonardo_DiCaprio
	nameListOriginal = nameList[:]
	source = args.source
	format = args.format
	
	if utils.checkNameFormat(nameList) == False:
		sys.exit()
	#searhing for movies
	movieListImdb = []
	movieListDBPedia = []
	movieList=[]
	searchForMovies(source, nameList, movieListImdb, movieListDBPedia, nameListOriginal)
	
	#preparing the results
	if (source == "all"):
		print("Preparing results...")
		utils.mergeLists(movieListImdb, movieListDBPedia)
		print("Preparing done.")
		#utils.printMovies(movieListImdb)
		movieList = movieListImdb
	elif (source == "dbpedia"):
		movieList = movieListDBPedia
	else:
		movieList = movieListImdb
	
	name = "_".join(nameList)
	#utils.printMovies(movieList)
	if (not movieList):
		print "No movies found for actor " +name
		sys.exit()
	
	#printing the results
	if (format == "json" or format == "all"):
		utils.printJSON(movieList,name)
	if (format == "xml" or format == "all"):
		utils.printXML(movieList,name)
	if (format == "csv" or format == "all"):
		utils.printCSV(movieList,name)
	
#call main function		
Run()
sys.exit()
