import sys  # for command line arguments
import urllib2  # for HTTP GET request
import json  # for parsing retrieved data
import time  # for current time
from xml.sax.saxutils import escape
from datetime import datetime
import pytz
import tzlocal

def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')

def read_url_as_dict(url):
    try:
        return json.loads(urllib2.urlopen(url).read())
    except urllib2.HTTPError:
        return {}

def get_likes(element_id):
    # get likes for this id
    likes_url = BASE_FB_API_URL + element_id + "/likes?access_token=" + ACCESS_TOKEN
    likes_dict = read_url_as_dict(likes_url)
    if "data" in likes_dict:
        return len(likes_dict["data"])
    return 0

def get_comments_and_replies(element_id):
    # get comments for this id
    comments_url = BASE_FB_API_URL + element_id + "/comments?access_token=" + ACCESS_TOKEN
    comments_dict = read_url_as_dict(comments_url)

    # update and creation time
    for key, value in get_creation_and_update_time(element_id).items():
        comments_dict[key] = value

    # get replies for each comment
    if "data" in comments_dict:
        for comment in comments_dict["data"]:
            if "id" in comment:

                # get the author
                for key, values in get_author(comment["id"]).items():
                    comment[key] = values

                # get comments and replies (recursively)
                replies = get_comments_and_replies(comment["id"])
                if bool(replies):  # check for empty replies
                    comment["comments"] = replies

                # update and creation time
                for key, value in get_creation_and_update_time(comment["id"]).items():
                    comment[key] = value

                # get pictures and videos
                attatchment = get_link_and_preview(comment["id"])
                if bool(attatchment):  # empty dictionaries evaluate to false
                    if "link" in attatchment:
                        comment["attatchment"] = attatchment

                likes = get_likes(comment["id"])
                if likes != 0:
                    comment["likes"] = likes

            if "message" in comment:
                comment["message"] = escape(comment["message"])

            if "story" in comment:
                comment["story"] = escape(comment["story"])

        return comments_dict["data"]
    return {}

def unix_time_to_datetime_str(unix_timestamp_str):
    return datetime.fromtimestamp(int(unix_timestamp_str), tzlocal.get_localzone()).strftime("%H:%M %d/%m/%Y")

def get_creation_and_update_time(element_id):
    # get author for this id
    times_url = BASE_FB_API_URL + element_id + "?fields=created_time&date_format=U&access_token=" + ACCESS_TOKEN
    times_dict = read_url_as_dict(times_url)

    # convert time to human-readable format
    if "created_time" in times_dict:
        times_dict["created_time"] = unix_time_to_datetime_str( times_dict["created_time"] )

    return times_dict

def get_author(element_id):
    # get author for this id
    author_url = BASE_FB_API_URL + element_id + "?fields=from&access_token=" + ACCESS_TOKEN
    author_dict = read_url_as_dict(author_url)

    # get the author's picture
    if "from" in author_dict:
        if "id" in author_dict["from"]:
            picture_url = get_author_picture(author_dict["from"]["id"])
            if bool(picture_url):
                author_dict["from"]["picture"] = picture_url

    return author_dict

def get_author_picture(author_id):
    # get author picture for this id
    author_picture_url = BASE_FB_API_URL + author_id + "?fields=picture&access_token=" + ACCESS_TOKEN
    author_picture_dict = read_url_as_dict(author_picture_url)

    if "picture" in author_picture_dict:
        if "data" in author_picture_dict["picture"]:
            return escape(author_picture_dict["picture"]["data"]["url"])
    return None

def get_link_and_preview(element_id):
    # get author for this id
    link_url = BASE_FB_API_URL + element_id + "?fields=link,full_picture&access_token=" + ACCESS_TOKEN
    link_dict = read_url_as_dict(link_url)

    escaped_dict = {}
    for key, value in link_dict.items():
        escaped_dict[key] = escape(value)  # escape the characters in the URL for XML later on
    return escaped_dict

def get_additional_data(feed):

    for story in feed:
        if "id" in story:

            # get the author (it's not sent for unknown reasons)
            for key, values in get_author(story["id"]).items():
                story[key] = values

            # update and creation time
            for key, value in get_creation_and_update_time(story["id"]).items():
                story[key] = value

            # get comments
            comments = get_comments_and_replies(story["id"])
            if bool(comments):  # empty dictionaries evaluate to false
                story["comments"] = comments

            # get pictures and videos
            attatchment = get_link_and_preview(story["id"])
            if bool(attatchment):  # empty dictionaries evaluate to false
                if "link" in attatchment:
                    story["attatchment"] = attatchment

            likes = get_likes(story["id"])
            if likes != 0:
                story["likes"] = likes

        if "message" in story:
            story["message"] = escape(story["message"])

        if "story" in story:
            story["story"] = escape(story["story"])

    return feed

if __name__ == "__main__":
    print("Fetching posts...")

    BASE_FB_API_URL = "https://graph.facebook.com/v2.8/"

    # format HTTP GET request for feed stories
    ACCESS_TOKEN = file2string(sys.argv[1])
    GROUP_ID = file2string(sys.argv[2])

    cur_time = round(time.time())
    num_seconds = 7 * 24 * 60 * 60  # a week in seconds = 604800
    a_week_ago_time = round(cur_time - num_seconds)

    feed_url = BASE_FB_API_URL + GROUP_ID + "/feed?date_format=U&since=" + str(a_week_ago_time) + \
               "&until=" + str(cur_time) + "&access_token=" + ACCESS_TOKEN

    feed_dict = read_url_as_dict(feed_url)

    if "data" in feed_dict.keys():
        feed_data = get_additional_data(feed_dict["data"])

        with open('feed.json', 'w') as outfile:
            json.dump(feed_data, outfile, sort_keys=True, indent=4, separators=(',', ': '))

        print("Finished fetching posts.")
        sys.exit(0)

    else:
        print("Error fetching posts.")
        sys.exit(1)
