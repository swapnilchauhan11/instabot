#import requests library
import requests

#import url library
import urllib

from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer


from termcolor import colored, cprint

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
from os import path



APP_ACCESS_TOKEN = ''


BASE_URL = 'https://api.instagram.com/v1/'

#Function for getting own info

def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print colored('Error due to Status code other than 200 received!','red')


# Function for getting the ID of a user


def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()

'''
Function declaration to get the info of a user by username
'''

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!', 'red')
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people user is following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print colored('---There is no data for this user!---', 'red')
    else:
        print colored('---Status code other than 200 received!---', 'red') #error in code


#Function declaration to get your recent post
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')


#Function declaration to get the recent post of a user by username
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print colored('User does not exist!','red')
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print colored('Your image has been downloaded!','green')
        else:
            print colored('Post does not exist!','red')
    else:
        print colored('Status code other than 200 received!','red')



def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            return user_media['data'][0]['id']
        else:
            print 'There is no recent post of the user!'
            exit()
    else:
        print 'Status code other than 200 received!'
        exit()



'''
Function declaration to like the recent post of a user
'''


def like_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print colored('Like was successful!','green')
    else:
        print colored('Your like was unsuccessful. Try again!','red')



def get_like_list(insta_username):            # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/likes?access_token=%s' % (media_id, APP_ACCESS_TOKEN)
    print colored('GET request url : %s', 'blue') % (request_url)
    like_list = requests.get(request_url).json()

    if like_list['meta']['code'] == 200:  # checking the status code .....
        if len(like_list['data']):
            position = 1
            print colored("List of people who Liked Your Recent post", 'blue')
            for users in like_list['data']:
                if users['username']!= None:
                    print position, colored(users['username'],'green')
                    position = position + 1
                else:
                    print colored('No one had liked Your post!', 'red')
        else:
            print colored("User Does not have any post",'red')
    else:
        print colored('Status code other than 200 recieved', 'red')




def get_comment_list(insta_username):  # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)   #    passing the end points and media id along with access token ..
    print colored('GET request url : %s', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented Your Recent post", 'blue')
            for users in comment_list['data']:
                if users['username'] != None:
                    print position, colored(users['username'], 'green')
                    position = position + 1
                else:
                    print colored('No one had commented on Your post!', 'red')
        else:
            print colored("User Does not have any post", 'red')
    else:
        print colored('Status code other than 200 recieved', 'red')


#        Function declaration to Get the lists of comments on  the recent post of a user.........


def get_comment_list(insta_username):  # Defining the Function ............
    media_id = get_post_id(insta_username)  # Getting post id by passing the username .......
    request_url = BASE_URL + 'media/%s/comments?access_token=%s' % (media_id, APP_ACCESS_TOKEN)   #    passing the end points and media id along with access token ..
    print colored('GET request url : %s\n', 'blue') % (request_url)
    comment_list = requests.get(request_url).json()

    if comment_list['meta']['code'] == 200:  # checking the status code .....
        if len(comment_list['data']):
            position = 1
            print colored("List of people who commented on Your Recent post", 'blue')
            for _ in range(len(comment_list['data'])):
                if comment_list['data'][position-1]['text']:
                    print colored(comment_list['data'][position-1]['from']['username'],'magenta') +colored( ' said: ','magenta') + colored(comment_list['data'][position-1]['text'],'blue')      #    Json Parsing ..printing the comments ..
                    position = position+1
                else:
                    print colored('No one had commented on Your post!\n', 'red')
        else:
            print colored("There is no Comments on User's Recent post.\n", 'red')
    else:
        print colored('Status code other than 200 recieved.\n', 'red')






'''
Function declaration to make a comment on the recent post of the user
'''


def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.post(request_url, payload).json()

    if make_comment['meta']['code'] == 200:
        print "Successfully added a new comment!"
    else:
        print "Unable to add comment. Try again!"


def hash_tag_trend(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        cprint("This user doesn't exist in your sandbox list", 'red')
        menu()
    request_url = Base_Url + 'users/' + user_id + '/media/recent/?access_token=' + App_access_token
    print('GET request url :', request_url)
    try:
        user_media = requests.get(request_url).json()
    except requests.exceptions.ConnectionError:
        cprint("Please check your internet connection", 'red')
        menu()
    item = 1
    flag = False
    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            for post in user_media['data']:
                if len(post['tags']):
                    flag = True
                    #caption = post['caption']
                    hash_tag['media_id'].append(post['id'])
                    hash_tag['words'].append(post['tags'])
            if (not flag):
                cprint("No hashtags found",'red')
            else:
                wordcloud()

        else:
            cprint("User doesn't have any post\n", 'blue')
    else:
        print(colored('Status code other than 200 received!\n', 'red'))




'''
Function declaration to make delete negative comments from the recent post
'''

def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] == 200:
        if len(comment_info['data']):
            #Here's a naive implementation of how to delete the negative comments :)
            for x in range(0, len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url).json()

                    if delete_info['meta']['code'] == 200:
                        print 'Comment successfully deleted!\n'
                    else:
                        print 'Unable to delete comment!'
                else:
                    print 'Positive comment : %s\n' % (comment_text)
        else:
            print 'There are no existing comments on the post!'
    else:
        print 'Status code other than 200 received!'







def start_bot():
    while True:
        print '\n'
        print colored('Hello! ---Welcome to InstaBot---!','green')
        print colored('Menu options are:','blue')
        print colored("a.Get your own details\n",'blue')
        print colored("b.Get details of a user by username\n", 'blue')
        print colored("c.Get your own recent post\n",'blue')
        print colored("d.Get the recent post of a user by username\n",'blue')
        print colored("e.Get a list of people who have liked the recent post of a user\n",'blue')
        print colored("f.Like the recent post of a user\n",'blue')
        print colored("g.Get a list of comments on the recent post of a user\n",'blue')
        print colored("h.Make a comment on the recent post of a user\n",'blue')
        print colored("i.Delete negative comments from the recent post of a user\n",'blue')
        print colored("j.Sub trend for an event and plot on wordcloud\n",'blue')
        print colored("k.Exit", 'blue')

        choice=raw_input(colored("Enter you choice: ",'blue'))
        if choice=="a":
            self_info()
        elif choice=="b":
            insta_username = raw_input(colored("Enter the username of the user: ", 'blue'))
            get_user_info(insta_username)
        elif choice == "c":
            get_own_post()
        elif choice == "d":
            insta_username = raw_input(colored("Enter the username of the user: ",'blue'))
            get_user_post(insta_username)
        elif choice=="e":
           insta_username = raw_input("Enter the username of the user: ")
           get_like_list(insta_username)
        elif choice=="f":
           insta_username = raw_input("Enter the username of the user: ")
           like_a_post(insta_username)
        elif choice=="g":
           insta_username = raw_input("Enter the username of the user: ")
           get_comment_list(insta_username)
        elif choice=="h":
           insta_username = raw_input("Enter the username of the user: ")
           post_a_comment(insta_username)
        elif choice=="i":
           insta_username = raw_input("Enter the username of the user: ")
           delete_negative_comment(insta_username)

        elif choice=="i":
            insta_username = input("Enter username : ")
            hash_tag_trend(insta_username)
           
        elif choice=="k":
            exit()
        else:
            print colored("Invalid choice", 'red')  #selected choice is wrong

start_bot()
