import sys  # for command line arguments
import urllib2  # for HTTP GET request
import json  # for parsing retrieved data
import time  # for current time
from xml.sax.saxutils import escape

def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')

def get_comments_and_replies(element_id):
    # get comments for this id
    comments_url = "https://graph.facebook.com/v2.6/" + element_id + "/comments?access_token=" + ACCESS_TOKEN
    comments_dict = json.loads(urllib2.urlopen(comments_url).read())

    # get replies for each comment
    for reply in comments_dict["data"]:
        if "id" in reply:
            replies = get_comments_and_replies(reply["id"])
            if bool(replies):  # check for empty replies
                reply["replies"] = replies

    return comments_dict["data"]

def get_author(element_id):
    # get author for this id
    author_url = "https://graph.facebook.com/v2.6/" + element_id + "?fields=from&access_token=" + ACCESS_TOKEN
    return json.loads(urllib2.urlopen(author_url).read())

def get_link_and_preview(element_id):
    # get author for this id
    link_url = "https://graph.facebook.com/v2.6/" + element_id + "?fields=link,full_picture&access_token=" + ACCESS_TOKEN
    link_dict = json.loads(urllib2.urlopen(link_url).read())
    escaped_dict = {}
    for key, value in link_dict.items():
        escaped_dict[key] = escape(value)  # escape the characters in the URL for XML later on
    return escaped_dict

def get_additional_data(dic):

    for element in dic:
        if "id" in element:

            # get the author (it's not sent for unknown reasons)
            author = get_author(element["id"])
            for key, values in author.items():
                element[key] = values

            # get comments
            comments = get_comments_and_replies(element["id"])
            if bool(comments):  # empty dictionaries evaluate to false
                element["comments"] = comments

            # get pictures and videos
            picture_video = get_link_and_preview(element["id"])
            if bool(picture_video):  # empty dictionaries evaluate to false
                if "link" in picture_video:
                    element["picture_video"] = picture_video

    return dic

if __name__ == "__main__":
    print("Fetching posts...")

    # format HTTP GET request for feed stories
    ACCESS_TOKEN = file2string(sys.argv[1])
    GROUP_ID = file2string(sys.argv[2])

    cur_time = round(time.time())
    num_seconds = 7 * 24 * 60 * 60  # a week in seconds = 604800
    a_week_ago_time = round(cur_time - num_seconds)

    feed_url = "https://graph.facebook.com/v2.6/" + GROUP_ID + "/feed?date_format=U&since=" + str(a_week_ago_time) + \
               "&until=" + str(cur_time) + "&access_token=" + ACCESS_TOKEN

    feed_dict = json.loads(urllib2.urlopen(feed_url).read())
    feed_data = get_additional_data(feed_dict["data"])

    with open('feed.json', 'w') as outfile:
        json.dump(feed_data, outfile)

    print("Finished fetching posts.")
