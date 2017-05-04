Python version (2.7.13)

install https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266 (imdbpy needs that)
install imdbpy 
install SPARQLWrapper

script use argparser for parsing the arguments.
How to run a script:
python searchActors.py -a Tom Hanks

There are also parameters -s and -f, for source and format.
For help information about parameters which can be used run:
python searchActors.py -h

known bugs (and things to think of :) ): 
1. if movie name is translated, it won't get original name (didn't find original name support in imdbpy), 
so in that case there can be duplicates from dbpedia and imdb. It probably can be done with scraping with BeautifulSoup(TODO ...)
2. there can be duplicates because of different format of movie names in dbpedia and imdb
3. imdbpy was not the happiest choise, not sure if it is supported yet for python 3, it needs vs2008 redistirbutables and it is slow.
