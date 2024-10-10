import tweepy
import pandas as pd
import schedule
import time

# Twitter APIの認証情報
API_KEY = 'YOUR_API_KEY'
API_SECRET_KEY = 'YOUR_API_SECRET_KEY'
ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'YOUR_ACCESS_TOKEN_SECRET'

# Twitter APIの認証
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# 設定
keywords = ["キーワード1", "キーワード2"]
like_limit = 5  # 一度の実行でいいねするツイートの数
like_interval = 10  # いいね間隔（分）
like_data = []

def like_tweets():
    for keyword in keywords:
        tweets = api.search_tweets(q=keyword, count=like_limit, result_type='recent')
        for tweet in tweets:
            if not tweet.retweeted and 'http' not in tweet.text:  # リツイートとURL回避
                try:
                    api.create_favorite(tweet.id)
                    like_data.append({'tweet_id': tweet.id, 'text': tweet.text})
                    print(f"Liked tweet: {tweet.text}")
                except tweepy.TweepError as e:
                    print(f"Error liking tweet: {e}")

def export_likes():
    df = pd.DataFrame(like_data)
    df.to_csv('liked_tweets.csv', index=False)

# スケジュール設定
schedule.every(like_interval).minutes.do(like_tweets)
schedule.every().day.at("23:59").do(export_likes)  # 毎日23:59にエクスポート

while True:
    schedule.run_pending()
    time.sleep(1)
