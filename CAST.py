import sys, threading, os, time, gc
from datetime import datetime
from funcs import *
#    ^^^^ This contains a lot of defs that are REQUIRED for this program to run

#import libs from internet
try:
	import tweepy
except:
	print("tweepy not installed, use 'pip install tweepy'")
	sys.exit(-1)
try:
	import pytz
except:
	print("pytz not installed, use 'pip install pytz'")
	sys.exit(-1)
#Declare some globals, mainly for writing to files and reading from them
LINESTART = "\""
LINESEPARATOR = "\",\""
LINEEND = "\"\n"
twitterTimePattern = "%Y-%m-%d"
specificTimePattern = "%Y-%m-%d %H:%M:%S"

#Display the title
print('''┌───────────────────┐
│Welcome to C.A.S.T.│
└───────────────────┘''')


#Authenticate with twitter
print("Authenticating...")
auth = tweepy.AppAuthHandler("Je049vMVniY7K57AchtKbBfUB", "isdrAhxl43KIadHqx05wNOVqMuZRpa1A5EpZbFSw5alvd2rXLy")
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
if(not api):
	print("Error connecting to twitter API.")
	sys.exit(-1)
print("Done.")

#################################
######FUNCTION DEFINITIONS#######
#################################

#Gets tweets, returns the most recent tweet's post time
def getData(threadQuery, threadFileName, num, fromDate = datetime.now(pytz.timezone("GMT")).replace(tzinfo=None), fromId = None):
	#declare useful variables that are needed in entire function scope
	filterRetweets = True #This can be adjusted
	maxId = -1
	#this is also an option, but is not used currently
	result = []
	query = threadQuery
	queryAmount = 100
	fname = threadFileName 
	ret = None
	#Display a message showing that the thread has begun a search
	print("Thread #" + str(num) + " (" + query + "): Searching.")
	while(True): #Go until we break
		try:
			#Logic for getting tweets based on various conditions
			if(maxId <= 0):
				if(not fromId):
					ret = api.search(q=query, count=queryAmount, since=fromDate.strftime(twitterTimePattern))
				else:
					#print("Searching from ID#" + str(fromId))
					ret = api.search(q=query, count=queryAmount, since_id=fromId, since=fromDate.strftime(twitterTimePattern))
			else:
				if(not fromId):
					ret = api.search(q=query, count=queryAmount, max_id=str(maxId - 1), since=fromDate.strftime(twitterTimePattern))
				else:
					#print("Searching from ID#" + str(fromId))
					ret = api.search(q=query, count=queryAmount, since_id=fromId, max_id=str(maxId - 1), since=fromDate.strftime(twitterTimePattern))
			if(not ret): #If nothing is returned
				break
			#print(len(ret))
			#Every time we get some tweets, add valid ones to our result list
			for tweet in ret:
				if(filterRetweets):
					if(not hasattr(tweet, 'retweeted_status')):
						if(datetime.strptime(getCreationDate(tweet), specificTimePattern) > fromDate):
							result.append(tweet)
					else:
						pass
				else:
					if(datetime.strptime(getCreationDate(tweet), specificTimePattern) > fromDate):
						result.append(tweet)
			#Adjust out max Id so we search from there back, ensuring no duplicates
			maxId = ret[-1].id
		except Exception as e: #If we end up grabbing too many tweets
			#remove this later
			print("ERROR: " + str(e))
			print("Twitter API overloaded, saving what has been retrieved.")
			log = open(threadFileName + ".log", 'ba')
			log.write(bytes(str(e), 'utf-8'))
			log.write(bytes("\n",'utf-8'))
			log.close()
			#Put what we have into results
			for tweet in ret:
				if(filterRetweets):
					if(not hasattr(tweet, 'retweeted_status')):
						#This is for the initial run, will not factor in once IDs are set
						if(datetime.strptime(getCreationDate(tweet), specificTimePattern) > fromDate):
							result.append(tweet)
					else:
						pass
						#discarded = discarded + 1
				else:
					#This is for the initial run, will not factor in once IDs are set
					if(datetime.strptime(getCreationDate(tweet), specificTimePattern) > fromDate):
						result.append(tweet)
			#Adjust maxId just in case
			maxId = ret[-1].id
			break
	#Write the data
	writeData(fname, result)
	#Show a report message
	print("Thread #" + str(num) + " (" + query + "): Got " + str(len(result)) + " new tweets.")
	#Return the appropriate time
	if(len(result) > 0):
		return (datetime.strptime(getCreationDate(result[0]), specificTimePattern), str(result[-1].id))
	else:
		#print("Returning default")
		if(not fromId == None):
			return (fromDate, str(fromId))
		else:
			return (fromDate, str(maxId))
#############	
def writeData(fname, result):
	#Ensure we're writing to a csv file
	if(not fname[-4:] == ".csv"):
		f = open(fname + ".csv", 'ba') #Open in byte-append mode
	else:
		f = open(fname, 'ba') #Open in byte-append mode
	#optional header, disabled to avoid making duplicates
	#f.write(bytes(LINESTART + "TEXT" + LINESEPARATOR + "DATE" + LINESEPARATOR + "FAVORITES" + LINESEPARATOR + "RETWEETS" + LINESEPARATOR + "CITY" + LINESEPARATOR + "COUNTRY" + LINESEPARATOR + "LANGUAGE" + LINESEPARATOR + "USER'S NAME" + LINESEPARATOR + "USER'S HANDLE" + LINESEPARATOR + "USER'S DESCRIPTION" + LINESEPARATOR + "USER'S FAVORITES COUNT" + LINESEPARATOR + "USER'S FOLLOWER COUNT" + LINESEPARATOR + "USER'S FRIENDS COUNT" + LINESEPARATOR + "USER GEO ENABLED" + LINESEPARATOR + "USER'S LANGUAGE" + LINESEPARATOR + "USER'S LOCATION" + LINESEPARATOR + "USER'S POST COUNT" + LINESEPARATOR + "USER'S TIMEZONE" + LINESEPARATOR + "USER TWITTER VERIFIED" + LINEEND, 'utf-8'))
	#Get every tweet from result, and make an entry for them
	for tweet in result:
		f.write(bytes(LINESTART + delimit(tweet.text) + LINESEPARATOR + str(tweet.created_at) + LINESEPARATOR + str(tweet.favorite_count) + LINESEPARATOR + str(tweet.retweet_count) + LINESEPARATOR + getCity(tweet) + LINESEPARATOR + getCountry(tweet) + LINESEPARATOR + getLanguage(tweet) + LINESEPARATOR + getUserName(tweet) + LINESEPARATOR + getUserScreenName(tweet) + LINESEPARATOR + getUserDescription(tweet) + LINESEPARATOR + getUserFavoritesCount(tweet) + LINESEPARATOR + getUserFollowersCount(tweet) + LINESEPARATOR + getUserFriendsCount(tweet) + LINESEPARATOR + getUserGeoEnabled(tweet) + LINESEPARATOR + getUserLanguage(tweet) + LINESEPARATOR + getUserLocation(tweet) + LINESEPARATOR + getUserStatusesCount(tweet) + LINESEPARATOR + getUserTimeZone(tweet) + LINESEPARATOR + getUserVerified(tweet) + LINEEND, 'utf-8'))
	f.close() #Save the file
	
#Main threading function
def doThread(threadQuery, threadFileName, delay, threadNumber):
	#Useful variables needed in all scopes in the function
	offset = 0
	lastTime = None
	lastId = None
	#Initial search, before looping
	#Try-catch (except) for file opening/handling
	try:
		#If the file is empty, write to it without reading
		if(os.stat(threadFileName + ".time").st_size == 0):
			print("No time record found, creating new.")
			record = open(threadFileName + ".time", 'wb')
			lastTime, lastId = getData(threadQuery, threadFileName, threadNumber)
			record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
			record.write(bytes(lastId, 'utf-8'))
			record.close()
			offset = lastTime.timestamp() - time.time()
		else:
			#Else, read the time, then write the new one
			print("Time Record: " + threadFileName + ".time found, loading")
			record = open(threadFileName + ".time", 'r')
			lastTime = datetime.strptime(record.readline().rstrip('\n'), specificTimePattern)
			lastId = record.readline().rstrip('\n')
			record.close()
			lastTime, lastId = getData(threadQuery, threadFileName, threadNumber, lastTime, lastId)
			record = open(threadFileName + ".time", 'wb')
			record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
			record.write(bytes(lastId, 'utf-8'))
			record.close()
			offset = lastTime.timestamp() - time.time()
	except Exception as e: #If the file's not there, make it
		if(not os.path.exists(os.path.dirname(threadFileName + ".time"))):
			try:
				os.makedirs(os.path.dirname(threadFileName + ".time"))
			except OSError as exc: # Guard against race condition
				print(exc)
				print("Cannot make directory, permissions invalid (Try sudo python3 <script>)")
		print("No time record found, creating new.")
		lastTime, lastId = getData(threadQuery, threadFileName, threadNumber)
		record = open(threadFileName + ".time", 'wb')
		record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
		record.write(bytes(lastId, 'utf-8'))
		record.close()
		offset = lastTime.timestamp() - time.time()
	#Loop, wait until the delay has passed, then crawl again
	while(threadController):
		if(lastTime.timestamp() - time.time() <= (offset - delay)): #While this might seem terribly inefficient, it actually allows easier stoppage
			try:
				if(os.stat(threadFileName + ".time").st_size == 0):
					lastTime, lastId = getData(threadQuery, threadFileName, threadNumber)
					record = open(threadFileName + ".time", 'wb')
					record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
					record.write(bytes(lastId, 'utf-8'))
					record.close()
					offset = lastTime.timestamp() - time.time()
				else:
					record = open(threadFileName + ".time", 'r')
					lastTime = datetime.strptime(record.readline().rstrip('\n'), specificTimePattern)
					lastId = record.readline().rstrip('\n')
					record.close()
					lastTime, lastId = getData(threadQuery, threadFileName, threadNumber, lastTime, lastId)
					record = open(threadFileName + ".time", 'wb')
					record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
					record.write(bytes(lastId, 'utf-8'))
					record.close()
					offset = lastTime.timestamp() - time.time()
			except Exception as e:
				lastTime, lastId = getData(threadQuery, threadFileName, threadNumber)
				record = open(threadFileName + ".time", 'wb')
				record.write(bytes(lastTime.strftime(specificTimePattern) + '\n', 'utf-8'))
				record.write(bytes(lastId, 'utf-8'))
				record.close()
				offset = lastTime.timestamp() - time.time()
#Actually run the program
#Read the config
print("Reading Config...")
readConfig = open("cast.cfg", 'r')
params = []
threadHolder = []
threadNumber = 1

threadController = True
#Split every line into a parameter set
for line in readConfig:
	if(not line[:1] == "*"): #Remove comments
		params.append(line.split(';'))
readConfig.close()
print("Config read, search terms are:")
for set in params:
	print("> " + set[0])
start = input("Is this correct? (y/n): ")
if(start.upper() == "Y"):
	#For every parameter set, start a thread
	for set in params:
		thread = threading.Thread(target=doThread, args=(set[0], set[2].rstrip('\n'), int(set[1]), threadNumber))
		threadHolder.append(thread)
		threadHolder[len(threadHolder) - 1].start()
		threadNumber = threadNumber + 1
	while(threadController):
		command = input()
		if(command == "stop"):
			threadController = False
			print("Stopping capture...")
		if(command == "clean"):
			gc.collect()
			print("Collecting garbage...")
else:
	print("Stopping program. Please correct cast.cfg and restart.")
	sys.exit(-1)