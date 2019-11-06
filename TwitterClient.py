'''
Twitter Client
'''
import tweepy
from textblob import TextBlob
import re

class TwitterClient(object):
	"""
	represents the tweepy api.
	"""
	def __init__(self):
		# --- Twitter Authentication ---
		creds = getCredentials("auth.txt")
		try:
			self.auth = tweepy.OAuthHandler(creds[0],creds[1])
			self.auth.set_access_token(creds[2],creds[3])
			self.api =tweepy.API(self.auth)
		except tweepy.TweepError:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Removes links/special characters using regex statements
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)","", tweet.text).split())

	def get_tweet_polarity(self, tweet):
		'''
		obtain polarity of passed tweet using TextBlob's methods.
		'''
		analysis = TextBlob(self.clean_tweet(tweet))
		return analysis.sentiment.polarity

	def grab_tweets(self,query,count=10):
		"""
		queries twitter api and grabs tweets based on query
		"""
		data = []
		try:
			#currently focusing on NYC area
			fetched_tweets = self.api.search(q=query,rpp=count,lang="en",geocode='40.71455,-74.00712,50000km')
			for tweet in fetched_tweets:
				clean_text=self.clean_tweet(tweet)
				tweet_polarity=self.get_tweet_polarity(tweet)
				location="40.71455,-74.00712"
				newData= ParsedData(query,clean_text,tweet_polarity,location,lang="en")
				data.append(newData)
			return data

		except tweepy.TweepError as e:
			print("Error : " +str(e))

def getCredentials(path_to_file):
	"""
	opens a credential file, to grab api keys.
	stores the credentials in a list of creds.
	"""
    with open(path_to_file,"r") as keys:
        consumer_key=keys.readline()
        consumer_secret=keys.readline(2)
        access_token=keys.readline(3)
        access_token_secret=keys.readline(4)
    return [consumer_key,consumer_secret,access_token,access_token_secret]
