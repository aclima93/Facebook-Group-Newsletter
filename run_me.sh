#!/bin/bash

# get an access token for a user belonging to the target group
python get_access_token.py app_id.txt app_secret.txt profile_id.txt

# get posts from facebook group
python get_posts.py access_token.txt group_id.txt

# generate newsletter from facebook group
python generate_newsletter.py feed.json

# send newsletter to mailing list
python send_newsletter.py sender.txt receivers.txt feed.html

#EOF