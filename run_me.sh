#!/bin/bash

# get posts from facebook group
python get_posts.py

# generate newsletter from facebook group
python generate_newsletter.py

# send newsletter to mailing list
python send_newsletter.py

#EOF