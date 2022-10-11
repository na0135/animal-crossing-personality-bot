import tweepy
import time
import requests
import warnings
import random
import json
import os
import config
# Initialization code
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)
api = tweepy.API(auth)

def request_json(https):
    resp = requests.get(https)
    if resp.status_code != 200:
        # This means something went wrong.
        raise Exception('{}: Error {}'.format(https, resp.status_code))

    return resp.json()


api_endpoint = 'http://acnhapi.com/v1/{}'
villagers = request_json(api_endpoint.format('villagers'))
# vill = requests.get('http://acnhapi.com/v1/villagers').json()
# print (vill[0]['name']['name-EUfr'])
peppy_villagers_id = []
peppy_villagers_name = []
peppy_imgs = []
normal_villagers_id = []
normal_villagers_name = []
normal_imgs = []
snooty_villagers_id = []
snooty_villagers_name = []
snooty_imgs = []
bigsis_villagers_id = []
bigsis_villagers_name = []
bigsis_imgs = []
lazy_villagers_id = []
lazy_villagers_name = []
lazy_imgs = []
jock_villagers_id = []
jock_villagers_name = []
jock_imgs = []
cranky_villagers_id = []
cranky_villagers_name = []
cranky_imgs = []
smug_villagers_id = []
smug_villagers_name = []
smug_imgs = []
for villager in villagers:
    if villagers[villager]['personality'] == 'Peppy':
        peppy_villagers_id += [villagers[villager]['file-name']]
        peppy_imgs += [villagers[villager]['image_uri']]
        peppy_villagers_name += [villagers[villager]['name']['name-EUfr']]
    if villagers[villager]['personality'] == 'Normal':
        normal_villagers_id += [villagers[villager]['file-name']]
        normal_imgs += [villagers[villager]['image_uri']]
        normal_villagers_name += [villagers[villager]['name']['name-EUfr']]
    if villagers[villager]['personality'] == 'Snooty':
        snooty_villagers_id += [villagers[villager]['file-name']]
        snooty_imgs += [villagers[villager]['image_uri']]
        snooty_villagers_name += [villagers[villager]['name']['name-EUfr']]
    if villagers[villager]['personality'] == 'Uchi':
        bigsis_villagers_id += [villagers[villager]['file-name']]
        bigsis_imgs += [villagers[villager]['image_uri']]
        bigsis_villagers_name += [villagers[villager]['name']['name-EUfr']]
    if villagers[villager]['personality'] == 'Jock':
        jock_villagers_id += [villagers[villager]['file-name']]
    if villagers[villager]['personality'] == 'Cranky':
        cranky_villagers_id += [villagers[villager]['file-name']]
    if villagers[villager]['personality'] == 'Smug':
        smug_villagers_id += [villagers[villager]['file-name']]
    if villagers[villager]['personality'] == 'Lazy':    
        lazy_villagers_id += [villagers[villager]['file-name']]
        
# print('Here is the list of all peppy villagers : {}'.format(peppy_villagers))
print(villagers[peppy_villagers_id[0]]['name']['name-USen'])
print(villagers[peppy_villagers_id[0]]['catch-phrase'])
print(villagers[peppy_villagers_id[0]]['birthday'])
# print(villagers[peppy_villagers[0]]['personality'])
# print(villagers[peppy_villagers[0]]['personality'])
# api.update_status(villagers[peppy_villagers_id[0]]['name']['name-USen'])

# Make a dictionary that maps MBTI type to a random ACNL with same personality
mbti_map = dict([("ISTJ", tuple(normal_villagers_id)), ("ISFJ", tuple(bigsis_villagers_id)), ("INFJ", tuple(normal_villagers_id)), ("INTJ", tuple(cranky_villagers_id)), ("ISTP", tuple(jock_villagers_id)), ("ISFP", tuple(bigsis_villagers_id)), ("INFP", tuple(normal_villagers_id)), ("INTP", tuple(smug_villagers_id)), ("ESTP", tuple(jock_villagers_id)), ("ESFP", tuple(peppy_villagers_id)), ("ENFP", tuple(lazy_villagers_id)), ("ENTP", tuple(smug_villagers_id)), ("ESTJ", tuple(snooty_villagers_id)), ("ESFJ", tuple(peppy_villagers_id)), ("ENFJ", tuple(smug_villagers_id)), ("ENTJ", tuple(cranky_villagers_id))])


def tweet_image(url):
    # api = twitter_api()
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        media = api.media_upload(filename)
        # api.update_status(status=message, media_ids = [media.media_id_string])
        os.remove(filename)
    else:
        print("Error downloading image")
    return [media.media_id_string]

# working 
# url = villagers[peppy_villagers_id[0]]['image_uri']
# message = "test"
# tweet_image(message, url)
# print("success")

# api.update_status("test")
# media = api.media_upload('test.png')
# api.update_status(status="test", media_ids = [media.media_id_string])


client = tweepy.Client(config.bearer_token, config.consumer_key, config.consumer_secret, config.access_token, config.access_token_secret)
client_id = client.get_me().data.id

start_id = 1
initialisation_resp = client.get_users_mentions(client_id)
if initialisation_resp.data != None:
    start_id = initialisation_resp.data[0].id

# Will continue to make sure it has mentions
while True:
    response = client.get_users_mentions(client_id, since_id=start_id)

    # If a user mentions the account properly the bot will reply with an image
    # and a picture
    if response.data != None:
        for tweet in response.data:
            try:
                print(tweet.text)
                new_tweet = tweet.text.replace("@actwtbot ", "")
                print(new_tweet)
                similar_villagers = mbti_map.get(new_tweet)
                if similar_villagers != None:
                    mbti = tweet.text
                    your_villager = random.choice(similar_villagers)
                    name = villagers[your_villager]['name']['name-USen']
                    fave_phrase = villagers[your_villager]['catch-phrase']
                    birthday = villagers[your_villager]['birthday-string']
                    personality = villagers[your_villager]['personality']
                    image = villagers[your_villager]['image_uri']
                    print(name)
                    final_tweet = "Hello! Meet " + name + "! Their birthday is on " + birthday + ", their favorite phrase is '" + fave_phrase + "', and their animal crossing personality is " + personality
                    client.create_tweet(in_reply_to_tweet_id=tweet.id, text=final_tweet, media_ids=tweet_image(image))
                    print("yay you replied successfully")
                    start_id = tweet.id
            except Exception as error:
                print(error)

    
    time.sleep(5)