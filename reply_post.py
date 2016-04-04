#!/usr/bin/python
import praw
import pdb
import re
import os
import time
from config_bot import *

def post_reply(comment):
    while True:
        try:
            print ("made it to try")
            count = len(re.findall(r'\w+', comment.body))
            pay = count*41660
            comment.reply("Hillary Clinton received $500 000 at a single speech to Bank of America in London. Based on an average speaking rate of 120 words per minute, and a speech length of 10 minutes, your comment would be worth **$" + str(pay/100) + "** if Hillary Clinton were to say it.  I'm triggered only in this subreddit with the phrase 'speaking fees'. PM me if you wish to contact my owner :)")
            posts_replied_to.append(comment.id)
            print ("Made a reply")
            break
        except praw.errors.RateLimitExceeded as error:
            print ('\tSleeping for %d seconds' % error.sleep_time)
            time.sleep(error.sleep_time)



# Check that the file that contains our username exists
if not os.path.isfile("config_bot.py"):
    print ("You must create a config file with your username and password.")
    print ("Please see config_skel.py")
    exit(1)

# Create the Reddit instance
user_agent = ("PyFor Eng bot 0.1")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        #posts_replied_to = filter(None, posts_replied_to)


while True:
    print("Starting cycle")
    flat_comments = praw.helpers.flatten_tree(r.get_comments('sandersforpresident'))
    for comment in flat_comments:
        if not hasattr(comment, 'body'):
            continue
        if comment.id not in posts_replied_to:
            if re.search("speaking fees",comment.body, re.IGNORECASE):
				if (comment.author.name != "HillarySpeechFeesBot"):
					print ("redy to reply")
					post_reply(comment)
    with open("posts_replied_to.txt", "w") as f:
        for post_id in posts_replied_to:
            f.write(post_id + "\n")
    time.sleep(60)
