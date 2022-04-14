import tweepy
import datetime

from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier

import pickle

import warnings
warnings.filterwarnings('ignore')

import os

import time

import urllib.request

import requests


import pandas as pd

def auth_user_collect_data():
	'''
	input -> None

	output -> defines api variable to be used in other functions.
	
	Initializes api variable if api key is valid, else gives an error.

	'''
	
	try:
		load_dotenv()
		twt_api=os.environ.get('tweepy_api_key')
		twt_api_secret=os.environ.get('tweepy_api_key_secret')
		twt_access_token=os.environ.get('tweepy_access_token')
		twt_access_token_secret=os.environ.get('tweepy_access_token_secret')
		
		auth=tweepy.OAuthHandler(twt_api,twt_api_secret)
		auth.set_access_token(twt_access_token,twt_access_token_secret)
		api=tweepy.API(auth)

		print('Correct Credentials')

		return api

	except:

		print('Error : Incorrect Credentials. Authentication Failed, terminating process.')

def auth_user_post_tweets():
	try:
		load_dotenv()
		twt_api=os.environ.get('tweepy_api_key')
		twt_api_secret=os.environ.get('tweepy_api_key_secret')
		twt_access_token=os.environ.get('tweepy_access_token')
		twt_access_token_secret=os.environ.get('tweepy_access_token_secret')
		
		auth=tweepy.OAuthHandler(twt_api,twt_api_secret)
		auth.set_access_token(twt_access_token,twt_access_token_secret)
		api=tweepy.API(auth)

		print('Correct Credentials')

		return api

	except:

		print('Error : Incorrect Credentials. Authentication Failed, terminating process.')


def get_latest_tweets(query,n):
	'''
	input -> query : searchword '#hashtag' ; n : number of tweets to scout.

	output -> a list containing tweet data in json format.
	'''
	#try:
	tweets=tweepy.Cursor(api.search_tweets,q='{}'.format(query),since_id=str(datetime.date.today()),include_entities=True,lang="en",tweet_mode="extended",result_type="recent").items(n)
	tweets_list=[tweet._json for tweet in tweets]

	return tweets_list

	#except:
	#	print("Error : Couldn't fetch tweets.")

def filter_1(tweets_list):
	'''
	input -> list containing tweet data in json format.

	output -> list containing tweet data in json format.

	Discards tweet which have '#hashtags' in them. Ex: #giveaway / #giveaways / etc.


	'''
	final_data=[]

	for tweet in tweets_list:
		hashtags=[]
		# to get retweeted info // if it is a retweet
		try:

			if 'retweeted_status' in tweet:
				for i in range((len(tweet['retweeted_status']['entities']['hashtags']))):
					hashtags.append(tweet['retweeted_status']['entities']['hashtags'][i]['text'].lower())

				if 'news' in hashtags or 'nftopensea' in hashtags or 'opensea' in hashtags or 'giveaway' in hashtags or 'nftgiveaway' in hashtags or 'nftgiveaways' in hashtags or 'openseaart' in hashtags:
					pass

				else:
					final_data.append(tweet)

		# if it is a normal tweet
		except:

			for i in range((len(tweet['entities']['hashtags']))):
				hashtags.append(tweet['entities']['hashtags'][i]['text'].lower())
				
				if 'news' in hashtags or 'nftopensea' in hashtags or 'opensea' in hashtags or 'giveaway' in hashtags or 'nftgiveaway' in hashtags or 'nftgiveaways' in hashtags or 'openseaart' in hashtags:
					pass

				else:
					final_data.append(tweet)

	return final_data

def filter_2(tweets_list):
	'''
	input -> list containing tweet data in json format.

	output -> list containing tweet data in json format.

	Discards tweets which contain 'keywords' in them. Ex: hello this is a giveaway -> 'giveaway' present hence discard.

	'''

	final_data=[]

	for tweet in tweets_list:
		# if tweet is retweet
		try:
			if 'giveaway' in tweet['retweeted_status']['full_text'].lower():
				pass
			else:
				final_data.append(tweet)

		# if it is a normal tweet
		except:
			if 'giveaway' in tweet['full_text'].lower():
				pass
			else:
				final_data.append(tweet)

	return final_data


def filter_3(tweets_list):
	'''
	input -> list containing tweet data in json format.

	output -> list containing tweet data in json format.
	
	Checks for media queries in tweets // gets rid of tweets containing hyperlinks.

	'''

	final_data=[]

	for tweet in tweets_list:
		# if tweet is a retweet
		try:
			if 'media' in tweet['retweeted_status']['entities']:
				final_data.append(tweet)
			else:
				pass
		# if tweet is a normal tweet
		except:
			if 'media' in tweet['entities']:
				final_data.append(tweet)
			else:
				pass

	return final_data

def convert_time(df):
	'''
	input -> dataframe containing tweet info.

	output -> dataframe with a new columns 'time_label'.

	Classifies time into 4 different categories 
	'''

	times=[]

	for time in df['time of tweet']:
		hour=int(time.split(':')[0])

		if hour > 0 and hour < 6:
			times.append('early/late')
		elif hour > 6 and hour < 12:
			times.append('morning')
		elif hour > 12 and hour < 18:
			times.append('noon/evening')
		else:
			times.append('night')

	df['time_label']=times

def get_data(tweet):
	'''
	input -> single tweet data in json format.

	output -> dataframe : containing relevant tweet info ; list : containing media url links ; string : screen name of twitter user


	'''
	#try:    
	l1,l2,l3,l4,l5,l6,l7,l8,l9,l10,l11=[],[],[],[],[],[],[],[],[],[],[]
	media_urls=[]

	if 'retweeted_status' in tweet:
		a1=str(tweet['retweeted_status']['id_str'])
		a2=tweet['retweeted_status']['user']['followers_count']
		a3=len(tweet['retweeted_status']['entities']['hashtags'])
		a4=tweet['retweeted_status']['created_at'].split(' ')[0]
		a5=tweet['retweeted_status']['created_at'].split(' ')[3]
		a6=tweet['retweeted_status']['user']['verified']
		a7=tweet['retweeted_status']['user']['favourites_count']
		a8=tweet['retweeted_status']['user']['friends_count']
		a9=tweet['retweeted_status']['user']['statuses_count']
		screen_name=tweet['user']['screen_name']
		
		if 'extended_entities' in tweet:
			for i in range(len(tweet['retweeted_status']['extended_entities']['media'])):
				media_urls.append(tweet['retweeted_status']['extended_entities']['media'][i]['media_url'])
		
		elif 'entities' in tweet:
			for i in range(len(tweet['retweeted_status']['entities']['media'])):
				media_urls.append(tweet['retweeted_status']['entities']['media'][i]['media_url'])
	else:
		a1=str(tweet['id_str'])
		a2=tweet['user']['followers_count']
		a3=len(tweet['entities']['hashtags'])
		a4=tweet['created_at'].split(' ')[0]
		a5=tweet['created_at'].split(' ')[3]
		a6=tweet['user']['verified']
		a7=tweet['user']['favourites_count']
		a8=tweet['user']['friends_count']
		a9=tweet['user']['statuses_count']
		screen_name=tweet['user']['screen_name']
		
		if 'extended_entities' in tweet:
			for i in range(len(tweet['extended_entities']['media'])):
				media_urls.append(tweet['extended_entities']['media'][i]['media_url'])
		
		elif 'entities' in tweet:
			for i in range(len(tweet['entities']['media'])):
				media_urls.append(tweet['entities']['media'][i]['media_url'])

	l1.append(a1)
	l2.append(a2)
	l3.append(a3)
	l4.append(a4)
	l5.append(a5)
	l6.append(a6)
	l7.append(a7)
	l8.append(a8)
	l9.append(a9)
	
	data={
	'id':l1,
	'number of hashtags':l3,
	'day of tweet':l4,
	'time of tweet':l5,
	'verified status':l6,
	'total followers':l2,
	'total likes':l7,
	'total following':l8,
	'total posts':l9,
	}

	df=pd.DataFrame(data)
	
	return {'data':df,'media_links':media_urls,'user_name':screen_name}

	#except:
	#	pass

def preprocess(df):
	'''
	input -> dataframe

	output -> dataframe

	Prepares data to be fed into machine learning algorithm.
	'''
	convert_time(df)
    
    # label encode according to training data
	for i in range(len(df['time_label'])):
		if df['time_label'].iloc[i]=='early/late':
			df['time_label'].iloc[i]=0
		elif df['time_label'].iloc[i]=='morning':
			df['time_label'].iloc[i]=1
		elif df['time_label'].iloc[i]=='night':
			df['time_label'].iloc[i]=2
		else:
			df['time_label'].iloc[i]=3
    
    # making average likes column
	df['average_likes']=df['total likes']/df['total posts']
    
	x=df[['number of hashtags','total followers','total likes','average_likes','time_label']]
    
	return x

def make_prediction(model,tweet):
	'''
	input -> model : sklearn model ; tweet : tweet data in json format

	output -> float : score // 0 if an error occurs.

	'''
	#try:
	data=get_data(tweet)
	df=data['data']
	df_=preprocess(df)
	media_links=data['media_links']
	username=data['user_name']

	res=model.predict_proba(df_)[0][1]

	return res
    
	#except:
	#	return 0

def get_tweet_scores(model,tweets_list):
	'''
	input -> model : sklearn model ; tweets_list : list containing tweet data in json format.

	output -> scores : list of scores ; id : list of id of tweet ; media_links : list of media urls ; screen_name : twitter username
	'''
	scores=[]
	media_links=[]
	screen_names=[]
	id_=[]

	for tweet in tweets_list:
		df,media_urls,screen_name=get_data(tweet)['data'],get_data(tweet)['media_links'],get_data(tweet)['user_name']
		df_=preprocess(df)
		score=model.predict_proba(df_)[0][1]
		scores.append(score)
		media_links.append(media_urls)
		screen_names.append(screen_name)
		id_.append(df['id'])

	return {'scores':scores,'id':id_,'media_links':media_urls,'screen_name':screen_names}

def download_media(media_urls):
	'''
	input -> media_urls : list containing media links

	output -> None // saves media files into 'media' folder.

	'''
	files=[]
	path_folder='media/'
	count=0
	for url in media_urls:
		if 'video' in url.split('.')[0]:
			file_type='.mp4'
		else:
			file_type='.'+str(url.split('.')[-1])
		
		urllib.request.urlretrieve(url,'media/'+str(count)+str(file_type))
		files.append('media/'+str(count)+str(file_type))
		count+=1
	#print(files)
	print('Total number of url files saved : ',len(files))
	return files

def get_media(tweet):
	media_urls=[]

	if 'retweeted_status' in tweet:
		if 'extended_entities' in tweet:
			for i in range(len(tweet['retweeted_status']['extended_entities']['media'])):
				media_urls.append(tweet['retweeted_status']['extended_entities']['media'][i]['media_url'])
		elif 'entities' in tweet:
			for i in range(len(tweet['retweeted_status']['entities']['media'])):
				media_urls.append(tweet['retweeted_status']['entities']['media'][i]['media_url'])
	else:
		if 'extended_entities' in tweet:
			for i in range(len(tweet['extended_entities']['media'])):
				media_urls.append(tweet['extended_entities']['media'][i]['media_url'])
		elif 'entities' in tweet:
			for i in range(len(tweet['entities']['media'])):
				media_urls.append(tweet['entities']['media'][i]['media_url'])


	print(media_urls)
	return media_urls


def check_timeline():
	pass
def repost_tweet(tweet,media_links):
    filename = 'media/temp.jpg'
    request = requests.get(media_links[0], stream=True)
    print('caption : ',tweet['full_text'])
    print('id : ',tweet['id'])
    message='''Original author : @{}\n\n{}'''.format(tweet['user']['screen_name'],tweet['full_text'])

    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api_1.update_status_with_media(message, filename)
        os.remove(filename)
    else:
        print("Unable to download image")

def prepare_tweet(tweet):
	if 'retweeted_status' in tweet:
		caption=tweet['retweeted_status']['full_text']
		username=tweet['retweeted_status']['user']['screen_name']
		id_=tweet['retweeted_status']['id']
	else:
		caption=tweet['full_text']
		username=tweet['user']['screen_name']
		id_=tweet['id']
	
	media_links=get_media(tweet)

	return {'username':username,'id':id_,'caption':caption,'media_links':media_links}


if __name__=='__main__':

	queries=['#cryptoart','#artblocks','#nftartists','#nftart']
	filename=r"nbs\ai_model_rfc.pkl"
	loaded_model=pickle.load(open(filename,"rb"))
	tweet_ids=[]

	while True:
		for query in queries:
			api=auth_user_collect_data()
			print('Query : ',query)
			tweets_list=get_latest_tweets(query,15)
			print('initially : ',len(tweets_list))
			tweets_list1=filter_3(tweets_list)
			print('First Filter : ',len(tweets_list1))
			tweets_list2=filter_1(tweets_list1)
			print('Second Filter : ',len(tweets_list2))
			tweets_list3=filter_2(tweets_list2)
			print('Third Filter : ',len(tweets_list3))

			for tweet in tweets_list3:
				

				score=make_prediction(loaded_model,tweet)
				print('Score for tweet : ',score)
				if query == '#cryptoart':
					if score > 0.9:
						if tweet['id'] in tweet_ids:
							print('duplicate tweet')
							pass
						else:
							data=prepare_tweet(tweet)
							username=data['username']
							caption=data['caption']
							media_links=data['media_links']
							id_=data['id']

							print('DATA')
							print('Username : @{}\nCaption : {}\nMedia : {}\nTweet link : www.twitter.com/twitter/status{}'.format(username,caption,media_links,id_))

							files=download_media(media_links)
							print('Files : ',files)

							status='''Original Author : @{}\n\n{}'''.format(username,caption)

							media_ids = [api.media_upload(f).media_id_string for f in file_names]

							ret = api.media_upload(files[0])

							api.update_status(status=status,media_ids=[ret.media_id_string])							

							print('Tweet Made')												

							tweet_ids.append(id_)
							time.sleep(5*60)
							break


				elif query=='#artblocks':
					if score > 0.95:

						# repost
						if tweet['id'] in tweet_ids:
							print('duplicate tweet')
							pass
						else:
							data=prepare_tweet(tweet)
							username=data['username']
							caption=data['caption']
							media_links=data['media_links']
							id_=data['id']

							print('DATA')
							print('Username : @{}\nCaption : {}\nMedia : {}\nTweet link : www.twitter.com/twitter/status{}'.format(username,caption,media_links,id_))

							files=download_media(media_links)
							print('Files : ',files)

							status='''Original Author : @{}\n\n{}'''.format(username,caption)

							media_ids=[api.media_upload(f) for f in files]
							ret = api.media_upload(files[0])

							api.update_status(status=status,media_ids=[ret.media_id_string])
							print('Tweet Made')												

							tweet_ids.append(id_)
							time.sleep(5*60)
							break

				elif query=='#nftartists':
					if score >=0.95:
						if tweet['id'] in tweet_ids:
							print('duplicate tweet')
							pass
						else:
							data=prepare_tweet(tweet)
							username=data['username']
							caption=data['caption']
							media_links=data['media_links']
							id_=data['id']

							print('DATA')
							print('Username : @{}\nCaption : {}\nMedia : {}\nTweet link : www.twitter.com/twitter/status{}'.format(username,caption,media_links,id_))

							files=download_media(media_links)
							print('Files : ',files)

							status='''Original Author : @{}\n\n{}'''.format(username,caption)

							media_ids=[api.media_upload(f) for f in files]
							ret = api.media_upload(files[0])


							api.update_status(status=status,media_ids=[ret.media_id_string])
							print('Tweet Made')												

							tweet_ids.append(id_)
							time.sleep(5*60)
							break

				elif query=='#nftart':
					if score >0.35 and score <=0.65:
						if tweet['id'] in tweet_ids:
							print('duplicate tweet')
							pass
						else:
							data=prepare_tweet(tweet)
							username=data['username']
							caption=data['caption']
							media_links=data['media_links']
							id_=data['id']

							print('DATA')
							print('Username : @{}\nCaption : {}\nMedia : {}\nTweet link : www.twitter.com/twitter/status{}'.format(username,caption,media_links,id_))

							files=download_media(media_links)
							print('Files : ',files)

							status='''Original Author : @{}\n\n{}'''.format(username,caption)

							media_ids=[api.media_upload(f) for f in files]
							ret = api.media_upload(files[0])
							api.update_status(status=status,media_ids=[ret.media_id_string])
					

							print('Tweet Made')												

							tweet_ids.append(id_)
							time.sleep(5*60)
							break 	

			print('Sleeping for 1 minutes')
			time.sleep(1*60)
