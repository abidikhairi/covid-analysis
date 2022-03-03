import tweepy as tw
import pandas as pd


consumer_key='JdG0QpBQ5pSoYBtw7PLCxr3YK'
consumer_secret='0bdsK4LwCPREU4rBAkxvNogF90HfRK3iJumLqjBAm8MgqrBhdD'
access_key='1296498183665848320-r7axdEBmMjjwhk5uEAYVJgbjm09Dhw'
access_secret='UVfooEK2oZ6MAOivpjExPoV3j1JB20RQyzJ0qbjkuO8Dh'

keywords = ['covid']
langs = ['en']

def extract_tweet_information(status):
	text = status.text.replace('\n', '')
	tweet_id = status.id_str
	lang = status.lang

	return {
		'id': tweet_id,
		'text': text.lower(),
		'lang': lang,
	}

class ProcessTweets(tw.Stream):
	def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, *, chunk_size=512, daemon=False, max_retries=..., proxy=None, verify=True):
		super().__init__(consumer_key, consumer_secret, access_token, access_token_secret, chunk_size=chunk_size, daemon=daemon, max_retries=max_retries, proxy=proxy, verify=verify)
	
		self.total_tweets = 2000
		self.data = []

	def on_status(self, status):
		tweet = extract_tweet_information(status)
		
		self.data.append(tweet)
		self.total_tweets -= 1

		if self.total_tweets == 0:

			pd.DataFrame(self.data).to_csv(f"./data/tweets.csv", index=False)
			self.running = False

		return super().on_status(status)

auth = tw.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
auth.set_access_token(key=access_key, secret=access_secret)


stream = ProcessTweets(consumer_key, consumer_secret, access_key, access_secret, max_retries=10)
stream.filter(track=keywords, languages=langs)
