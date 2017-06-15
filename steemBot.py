from steem import Steem
import json
import datetime
import os
from dateutil import parser
import time

# create Steem instance
s = Steem()

# unlock wallet by setting environmental variable
os.environ["UNLOCK"] = "Your-super-secret-wallet-passphrase"

latestPostId = s.get_feed("your-account-handle", -1, 1)[0]['entry_id']

runMe = True


def upvoteAndResteem(postAuthor, link, postVotes):
    # upvote post
    s.vote("@" + postAuthor + "/" + link, 100.0)
    # resteem post
    s.resteem("@" + postAuthor + "/" + link)
    # print out data
    message = "Upvoted post: @" + postAuthor + "/" + link + " as voter #" + str(myvote) + " at time: " + str(
        datetime.datetime.now()) + "\n"
    print(message)
    # write open and write message to log file
    f = open("log.txt", "a")
    f.write(message)
    f.close()


# get current latest post id on feed
while runMe == True:

    # gets latest post on your feed
    feed = s.get_feed("your-account-handle", -1, 1)
    latestPost = feed[0]['entry_id']

    if latestPost > latestPostId:
        # Get the author of the posts
        author = feed[0]['comment']['author']
        # Get the link to the post
        postLink = feed[0]['comment']['permlink']
        # Get the amount of upvotes on the post
        votes = feed[0]['comment']['net_votes']
        # We wan't to be in the top 10 first votes
        if votes < 11:
            upvoteAndResteem(author, postLink, votes)
            # Update the latest post value in log
            latestPostId = latestPost
        else:
            # If we're not in the first 10 votes we won't upvote and resteem
            print("votes too high")
            # Update latest post post value in log
            latestPostId = latestPost


    else:
        print("No new posts at time: " + str(datetime.datetime.now()))
        print('Sleeping for 15 seconds')
        # sleep for for 15 seconds before cheecking for new posts
        time.sleep(15)
        print("Done sleeping")
