from movie import Movie
from imdb import IMDb

class IMDBSearch:
	#checking if actor is actualy in results, because imdb returns also similar names
	@staticmethod
	def __findActorInResult(actors, nameList):
		foundActor = []
		nameLen = len(nameList)
		for actor in actors:
			actorList = actor["name"].split(" ")
			if (len(actorList) != nameLen):
				continue
			found = True
			for name in nameList:
				match = next((x for x in actorList if x.upper() == name.upper()), None)
				if match == None:
					found = False
				
			if found:
				return actor
		return []
			
	#if there's no "actor" or "actress" key, the person is not declared as actor/actress on imdb
	@staticmethod	
	def __checkIfPersonIsAnActor(person):
		match = next((x for x in person.keys() if x == "actor" or x=="actress"), None)
		if (match == None):
			print (person["name"] + " is not an actor/actress on  IMDB")
			return ""
		
		return match
		
	@staticmethod
	def search(nameList, movieList):
		ia = IMDb()
		name = " ".join(nameList)
		print(name)
		#search imdb to find actor
		actors = ia.search_person(name)
		if (not actors):
			print("Actor not found on IMDB!")
			return
		#find match in list of actors that imdb returned
		actor = IMDBSearch.__findActorInResult(actors, nameList)
		if (not actor):
			print("Actor not found on IMDB!")
			return
		
		full_person = ia.get_person(actor.getID(), info=["filmography"])

		key = IMDBSearch.__checkIfPersonIsAnActor(full_person)
		if (not key):
			return
		
		#iterate true movie results and add them to the list
		films = full_person[key]
		for film in films:
			movieName = film["title"]
			year = "Missing"
			match = next((x for x in film.keys() if x == "year"), None)
			if (match != None):
				year = film["year"]
			else:
				print("IMDB year is missing for movie " + movieName)
			
			results = ia.search_movie(movieName)
			if (not results):
				print "No " +movieName + "on imdb."
				continue
			url= ia.get_imdbURL(results[0])
			#print "URL: "+url
			url = url.replace("//akas.", "//www.")
			movieList.append(Movie(movieName, year, url))
			