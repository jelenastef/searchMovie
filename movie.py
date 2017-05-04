class Movie:
	def __init__(self, name, year, imdbURL="None", dbPediaURL="None"):
		self.name = name
		self.year = year
		self.imdbURL = imdbURL
		self.dbPediaURL = dbPediaURL

	def toXML(self):
		xmlStr = '<movie>\n'
		xmlStr+=('\t<name>' + self.name + '</name>\n')
		xmlStr+=('\t<year>' + str(self.year) +'</year>\n')
		xmlStr+=('\t<imdbURL>' + self.imdbURL + '</imdbURL>\n')
		xmlStr+=('\t<dbPediaURL>' + self.dbPediaURL + '</dbPediaURL>\n')
		xmlStr+=('</movie>\n')
		return xmlStr
		
	def toCSV(self):
		str_list = [self.name, str(self.year), self.imdbURL,self.dbPediaURL.replace(";",",")] #solution for multiple urls from dbpedia with same name
		return ','.join(str_list) + "\n"
		
		
	
	
		
