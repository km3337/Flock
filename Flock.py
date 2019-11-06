import re
import tweepy
from textblob import TextBlob

class ParsedData:
	#container class for data parsed from twitter
	def __init__(self,topic,text,sentiment,coordinates,lang):
		self.topic=topic
		self.text=text
		self.sentiment=sentiment
		self.coordinates=coordinates
		self.lang=lang

	def get_csv(self):
		return '{},{},{},{},{}\n'.format(self.topic,self.text,self.sentiment,self.coordinates,self.lang)

class TwitterClient(object):
	def __init__(self):
		# --- Twitter Authentication ---
		with open("auth.txt","r") as keys:
		consumer_key=keys.readline()
		consumer_secret=keys.readline(2)
		access_token=keys.readline(3)
		access_token_secret=keys.readline(4)
		try:
			self.auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
			self.auth.set_access_token(access_token,access_token_secret)
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
		#queries twitter api and grabs tweets based on query
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

def main():
	api = TwitterClient()
	fetched_data=api.grab_tweets(query='MTA', count=300)
	print("outputting into CSV...")
	display_csv(filename="MTA.csv",fetched_data=fetched_data)
	print("\nSuccess. Squawk?..")


def display_csv(filename="testfile.csv", fetched_data=[], *args):
	#grabs the fetched twitter posts and outputs in csv format
	#default  location is the testfile
	outfile= open(filename,"a")
	for data in fetched_data:
		line=data.get_csv()
		outfile.write(line)
	outfile.close()


if __name__ == "__main__":
	main()
