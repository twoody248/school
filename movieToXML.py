# Python 2.7 program that retrieves data from a sqlite database and transforms it into XML
# Database used is the Internet Movie Database, freely available online
# Assumes that the db file is in the same dir as this program
# Harvard Extension School - CSCI-E66
# Tom Lehmann

import sqlite3

# get the db file that the user specifies
db_filename = raw_input("Enter database file name: ")
db = sqlite3.connect(db_filename)

# Creates the movies.xml file
def writeMovies():
	# first, query for all data in the movies table
	cursor = db.cursor()
	cursor.execute('SELECT * FROM Movie;')

	# open the output file
	moviesfile = open("movies.xml", 'w')

	# now, add xml header and root element open tag
	moviesfile.write('<?xml version="1.0"?>' + '\n' + "<movies>" + '\n')

	# now, iterate over each tuple in the cursor
	# build a string that represents the movie, and add it to the output file
	for tuple in cursor:

		# first, create the open movie tag with id, actor, director attributes
		movieID = str(tuple[0])
		movieBuffer = '  <movie id="M' + movieID + '"' # movieBuffer represents movie entry to be added to xml file

		# get the movie's directors if they exist, add them to the buffer
		directorCursor = db.cursor()
		directorCursor.execute('SELECT director_id FROM Director WHERE movie_id =?',(movieID,))
		firstDirector = directorCursor.fetchone()
		if firstDirector is not None: # only do this if the movie has a director
			movieBuffer += ' directors="' + 'P' + str(firstDirector)[3:10] + ' '
			for director in directorCursor:
				movieBuffer += 'P' + str(director)[3:10] + ' '
		movieBuffer = movieBuffer[:-1] + '"'

		# get the movie's actors, add them to the buffer
		actorCursor = db.cursor()
		actorCursor.execute('SELECT actor_id FROM Actor WHERE movie_id=?',(movieID,))
		movieBuffer += ' actors="'
		for actor in actorCursor:
			movieBuffer += 'P' + str(actor)[3:10] + ' '
		movieBuffer = movieBuffer[:-1] + '"'

		# get the movie's oscars if they exist, add them to the buffer
		oscarCursor = db.cursor()
		oscarCursor.execute('SELECT * FROM Oscar WHERE movie_id=?',(movieID,))
		firstOscar = oscarCursor.fetchone()
		if firstOscar is not None: #only do this if the movie has an oscar
			movieBuffer += ' oscars="' + parseOscar(firstOscar)
			for oscar in oscarCursor:
				movieBuffer += parseOscar(oscar)
		movieBuffer = movieBuffer[:-1] + '">\n'

		# next, add the remaining attributes of the movie as child elements to the movie element
		movieBuffer += '    ' + writeTags(str(tuple[1]),"name") + '\n'
		movieBuffer += '    ' + writeTags(str(tuple[2]),"year") + '\n'
		movieBuffer += '    ' + writeTags(str(tuple[3]),"rating") + '\n'
		movieBuffer += '    ' + writeTags(str(tuple[4]),"runtime") + '\n'
		movieBuffer += '    ' + writeTags(str(tuple[5]),"genre") + '\n'
		# only add the earnings rank if it exists
		if(str(tuple[6])!='None'):
			movieBuffer += '    ' + writeTags(str(tuple[6]),"earnings_rank") + '\n'
		movieBuffer += '  </movie>'

		# write the buffer to the output file
		moviesfile.write(movieBuffer + "\n")

	# finally, write the closing movies tag and close the file
	moviesfile.write("</movies>")
	moviesfile.close()

# Creates the people.xml file
def writePeople():

	# first, query for all data in the movies table
	cursor = db.cursor()
	cursor.execute('SELECT * FROM Person;')

	# open the output file
	peoplefile = open("people.xml", 'w')

	# now, add xml header and root element open tag
	peoplefile.write('<?xml version="1.0"?>' + '\n' + "<people>" + '\n')

	# now, iterate over each tuple in the cursor
	# build a string that represents the movie, and add it to the output file
	for tuple in cursor:

		# first, create the open person tag with id, acted, directed, oscar attributes
		personID = str(tuple[0])
		personBuffer = '  <person id="P' + personID + '"' # personBuffer represents person entry to be added to xml file

		# get the movies the person has directed if they exist, add them to the buffer
		directedCursor = db.cursor()
		directedCursor.execute('SELECT movie_id FROM Director WHERE director_id =?',(personID,))
		firstDirected = directedCursor.fetchone()
		if firstDirected is not None: # only do this if the person has directed a movie
			personBuffer += ' directed="' + 'M' + str(firstDirected)[3:10] + ' '
			for directed in directedCursor:
				personBuffer += 'M' + str(directed)[3:10] + ' '
		personBuffer = personBuffer[:-1] + '"'

		# get the movies the person has acted in if they exist, add them to the buffer
		actedInCursor = db.cursor()
		actedInCursor.execute('SELECT movie_id FROM Actor WHERE actor_id =?',(personID,))
		firstactedIn = actedInCursor.fetchone()
		if firstactedIn is not None: # only do this if the person has acted in a movie
			personBuffer += ' actedIn="' + 'M' + str(firstactedIn)[3:10] + ' '
			for actedIn in actedInCursor:
				personBuffer += 'M' + str(actedIn)[3:10] + ' '
		personBuffer = personBuffer[:-1] + '"'

		# get the oscars the person has won if they exist, add them to the buffer
		oscarCursor = db.cursor()
		oscarCursor.execute('SELECT * FROM Oscar WHERE person_id =?',(personID,))
		firstOscar = oscarCursor.fetchone()
		if firstOscar is not None: # only do this if the person has won an oscar
			personBuffer += ' oscars="' + parseOscar(firstOscar)
			for oscar in oscarCursor:
				personBuffer += parseOscar(oscar)
		personBuffer = personBuffer[:-1] + '">\n'

		# next, add the remaining attributes of a person as child elements to the person element
		personBuffer += '    ' + writeTags(str(tuple[1]),"name") + '\n'
		if (str(tuple[2])!='None'): # only write the child element if it has data
			personBuffer += '    ' + writeTags(str(tuple[2]),"dob") + '\n'
		if (str(tuple[3])!='None'): # only write the child element if it has data
			personBuffer += '    ' + writeTags(str(tuple[3]),"pob") + '\n'
		personBuffer += '  </person>'

		# write the buffer to the output file
		peoplefile.write(personBuffer + "\n")

	# finally, write the closing people tag and close the file
	peoplefile.write("</people>")
	peoplefile.close()

# Creates the oscar.xml file
def writeOscar():

	# first, query for all data in the oscars table
	cursor = db.cursor()
	cursor.execute('SELECT * FROM Oscar;')

	# open the output file
	oscarfile = open("oscar.xml", 'w')

	# now, add xml header and root element open tag
	oscarfile.write('<?xml version="1.0"?>' + '\n' + "<oscars>" + '\n')

	# now, iterate over each tuple in the cursor
	# build a string that represents the oscar, and add it to the output file
	for tuple in cursor:

		# first, create the open oscar tag with id, movie, and person attribute (if it exists)
		oscarID = parseOscar(tuple)
		oscarBuffer = '  <oscar id="' + oscarID # oscarBuffer represents oscar entry to be added to xml file
		oscarBuffer = oscarBuffer[:-1] + '"'
		oscarBuffer += ' movie_id="' + str(tuple[0]) + '"' # add the movie id
		if str(tuple[2]) != 'BEST-PICTURE': # if the oscar is not best picure, add the person it was awarded to as an attribute of oscar
			oscarBuffer += ' person_id="' + str(tuple[1]) + '"'
		oscarBuffer += '>\n'

		# next, add the remaining attributes of a oscar as child elements to the oscar element
		oscarBuffer += '    ' + writeTags(str(tuple[2]),"type") + '\n'
		oscarBuffer += '    ' + writeTags(str(tuple[3]),"year") + '\n'
		oscarBuffer += '  </oscar>'

		#write the buffer to the output file
		oscarfile.write(oscarBuffer + "\n")
		
	# finally, write the closing oscar tag and close the file
	oscarfile.write("</oscars>")
	oscarfile.close()

# Returns a data item as a string with tags around it
# @param data: data item
# @param tagName: name of tag to be surrounding data
def writeTags(data,tagName):
	opentag = "<" + tagName + ">"
	closetag = "</" + tagName + ">"
	return str(opentag + str(data) + closetag)

# Retuns a string representing an oscar id
# @param oscar: the oscar array to parsed
def parseOscar(oscar):
	oscarParsed = ''
	if str(oscar[2]) == 'BEST-PICTURE':
		oscarParsed += 'O' + str(oscar[3]) + '0000000 '
	else:
		oscarParsed += 'O' + str(oscar[3]) + str(oscar[1]) + ' '
	return oscarParsed

# Write the movies.xml file.  
writeMovies()
print "movies.xml has been written."
# Write the people.xml file.
writePeople()
print "people.xml has been written."
# Write the oscars.xml file.
writeOscar()
print "oscars.xml has been written."
db.close()