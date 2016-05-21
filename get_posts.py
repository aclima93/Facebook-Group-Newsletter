import sys  # for command line arguments
import urllib2  # for HTTP GET request
import json  # for parsing retrieved data
import time  # for current time
import HeadRequest as hr
from xml.sax.saxutils import escape

def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')

def get_picture_or_video(id):
    # get picture and video for this id
    url = "https://graph.facebook.com/v2.6/" + id + "?fields=source&access_token=" + access_token
    picture_video_dict = json.loads(urllib2.urlopen(url).read())  # read content from url and load it as JSON

    if "source" in picture_video_dict:

        picture_video_dict["source"] = escape(picture_video_dict["source"]) # escape the characters in the URL for XML later on

        mime_type = hr.get_type(picture_video_dict["source"])
        picture_video_dict["mime_type"] = mime_type

        if mime_type is not None:
            if "image" in mime_type:
                picture_video_dict["source_type"] = "image"
            elif "video" in mime_type:
                picture_video_dict["source_type"] = "video"

    return picture_video_dict


def get_comments_and_replies(id):
    # get comments for this id
    comments_url = "https://graph.facebook.com/v2.6/" + id + "/comments?access_token=" + access_token
    comments_dict = json.loads(urllib2.urlopen(comments_url).read())

    # get replies for each comment
    for reply in comments_dict["data"]:
        if "id" in reply:
            replies = get_comments_and_replies(reply["id"])
            if bool(replies):  # check for empty replies
                reply["replies"] = replies

    return comments_dict["data"]

def get_additional_data(dic):

    for element in dic:
        if "id" in element:

            # get comments
            comments = get_comments_and_replies(element["id"])
            if bool(comments):  # empty dictionaries evaluate to false
                element["comments"] = comments

            # get pictures and videos
            picture_video = get_picture_or_video(element["id"])
            if bool(picture_video):  # empty dictionaries evaluate to false
                element["picture_video"] = picture_video

    return dic

if __name__ == "__main__":
    print("Fetching posts...")

    # format HTTP GET request for feed stories
    access_token = file2string(sys.argv[1])
    group_id = file2string(sys.argv[2])

    cur_time = round(time.time())
    num_seconds = 7 * 24 * 60 * 60  # a week in seconds = 604800
    a_week_ago_time = round(cur_time - num_seconds)

    url = "https://graph.facebook.com/v2.6/" + group_id + "/feed?date_format=U&since=" + str(a_week_ago_time) + \
          "&until=" + str(cur_time) + "&access_token=" + access_token

    feed = json.loads(urllib2.urlopen(url).read())
    feed_data = get_additional_data(feed["data"])

    with open('feed.json', 'w') as outfile:
        json.dump(feed_data, outfile)

    print("Finished fetching posts.")
