import sys  # for command line arguments
import urllib2  # for HTTP GET request
import json  # for parsing retrieved data
import time # for current time

def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')

if __name__ == "__main__":

    access_token = file2string(sys.argv[1])
    group_id = file2string(sys.argv[2])

    cur_time = round(time.time())
    num_seconds = 7 * 24 * 60 * 60  # a week in seconds = 604800
    a_week_ago_time = round(cur_time - num_seconds)

    url = "https://graph.facebook.com/v2.6/" + group_id + "/feed?date_format=U&since=" + str(a_week_ago_time) + "&until=" + str(cur_time) + "&access_token=" + access_token

    print(url)

    feed = json.loads(urllib2.urlopen(url).read())

    print(feed)
