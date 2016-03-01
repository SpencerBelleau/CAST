def delimit(string):
	newString = ""
	for i in range(len(string)):
		newString = newString + str(string[i])
		if(string[i] == '"'):
			newString = newString + '"'
	return newString

def getText(tweet):
	if(hasattr(tweet, 'text')):
		return str(tweet.text)
	else:
		return "None"

def getCreationDate(tweet):
	if(hasattr(tweet, 'created_at')):
		return str(tweet.created_at)
	else:
		return "None"

def getRetweetCount(tweet):
	if(hasattr(tweet, 'retweet_count')):
		return str(tweet.retweet_count)
	else:
		return "None"
		
def getFavoriteCount(tweet):
	if(hasattr(tweet, 'favorite_count')):
		return str(tweet.favorite_count)
	else:
		return "None"
		
def getCountry(tweet):
	if(hasattr(tweet, 'place')):
		if(hasattr(tweet.place, 'country')):
			return str(tweet.place.country)
		else:
			return "None"
	else:
		return "None"
		
def getCity(tweet):
	if(hasattr(tweet, 'place')):
		if(hasattr(tweet.place, 'full_name')):
			return str(tweet.place.full_name)
		else:
			return "None"
	else:
		return "None"
		
def getLanguage(tweet):
	if(hasattr(tweet, 'language')):
		return str(tweet.language)
	else:
		return "None"
		
def getUserName(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'name')):
			return str(tweet.user.name)
		else:
			return "None"
	else:
		return "None"
		
def getUserDescription(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'description')):
			return str(tweet.user.description)
		else:
			return "None"
	else:
		return "None"
		
def getUserFavoritesCount(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'favorites_count')):
			return str(tweet.user.favorites_count)
		else:
			return "None"
	else:
		return "None"
		
def getUserFollowersCount(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'followers_count')):
			return str(tweet.user.followers_count)
		else:
			return "None"
	else:
		return "None"
		
def getUserFriendsCount(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'friends_count')):
			return str(tweet.user.friends_count)
		else:
			return "None"
	else:
		return "None"
		
def getUserGeoEnabled(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'geo_enabled')):
			return str(tweet.user.geo_enabled)
		else:
			return "None"
	else:
		return "None"
		
def getUserLanguage(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'lang')):
			return str(tweet.user.lang)
		else:
			return "None"
	else:
		return "None"
		
def getUserLocation(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'location')):
			return str(tweet.user.location)
		else:
			return "None"
	else:
		return "None"
		
def getUserScreenName(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'screen_name')):
			return str(tweet.user.screen_name)
		else:
			return "None"
	else:
		return "None"
		
def getUserStatusesCount(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'statuses_count')):
			return str(tweet.user.statuses_count)
		else:
			return "None"
	else:
		return "None"
		
def getUserTimeZone(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'time_zone')):
			return str(tweet.user.time_zone)
		else:
			return "None"
	else:
		return "None"
		
def getUserVerified(tweet):
	if(hasattr(tweet, 'user')):
		if(hasattr(tweet.user, 'verified')):
			return str(tweet.user.verified)
		else:
			return "None"
	else:
		return "None"	