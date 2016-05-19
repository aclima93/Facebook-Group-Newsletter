import sys  # for command line arguments
import urllib2  # for HTTP GET request
import json  # for parsing retrieved data
import time  # for current time


class FeedPost:
    def __init__(self, id, created_time, from_author, story, caption, description, message, link, picture, object_id,
                 source):
        "information about the post"
        self.id = id
        self.created_time = created_time
        self.from_author = from_author

        "the post itself"
        self.story = story
        self.caption = caption
        self.description = description
        self.message = message

        "sweet addtional information"
        self.link = link
        self.picture = picture
        self.object_id = object_id
        self.source = source


def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')


def get_comments(id):
    # get comments for this id
    comments_url = "https://graph.facebook.com/v2.6/" + id + "/comments?access_token=" + access_token
    comments_dict = json.loads(urllib2.urlopen(comments_url).read())

    # get replies for each comment
    for reply in comments_dict["data"]:
        if "id" in reply:
            comments = get_comments(reply["id"])
            if bool(comments):  # check for empty comments
                reply["comments"] = comments

    return comments_dict["data"]


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

    # get comments from each story
    for story in feed["data"]:
        if "id" in story:
            comments = get_comments(story["id"])
            if bool(comments):  # empty dictionaries evaluate to false
                story["comments"] = comments

    with open('feed.json', 'w') as outfile:
        json.dump(feed, outfile)

    print("Finished fetching posts.")
