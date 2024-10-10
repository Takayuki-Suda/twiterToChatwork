import tweepy
import requests

# Twitter APIの認証情報
twitter_api_key = 'YOUR_TWITTER_API_KEY'
twitter_api_secret_key = 'YOUR_TWITTER_API_SECRET_KEY'
twitter_access_token = 'YOUR_TWITTER_ACCESS_TOKEN'
twitter_access_token_secret = 'YOUR_TWITTER_ACCESS_TOKEN_SECRET'

# Chatwork APIのトークンとルームID
chatwork_api_token = 'YOUR_CHATWORK_API_TOKEN'
chatwork_room_id = 'YOUR_CHATWORK_ROOM_ID'

# Twitterの認証
auth = tweepy.OAuth1UserHandler(twitter_api_key, twitter_api_secret_key, twitter_access_token, twitter_access_token_secret)
api = tweepy.API(auth)

# 特定のアカウントからのツイートを監視
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if 'ドラゴンクエストタクト' in status.text:
            message = status.text
            # Chatworkにメッセージを送信
            requests.post(
                f'https://api.chatwork.com/v2/rooms/{chatwork_room_id}/messages',
                headers={'X-ChatWorkToken': chatwork_api_token},
                data={'body': message}
            )

# ストリームを開始
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
myStream.filter(track=['ドラゴンクエストタクト'])
