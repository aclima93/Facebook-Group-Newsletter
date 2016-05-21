"""
Credit: http://stackoverflow.com/questions/3702331/python-test-for-a-url-and-image-type
"""

import mimetypes  # for checking MIME type of URL source (namely, images and videos)
import urllib2


class HeadRequest(urllib2.Request):
    def get_method(self):
        return 'HEAD'


def get_contenttype(image_url):
    try:
        response = urllib2.urlopen(HeadRequest(image_url))
        maintype = response.headers['Content-Type'].split(';')[0].lower()
        return maintype
    except urllib2.HTTPError as e:
        print(e)
        return None


def get_mimetype(image_url):
    (mimetype, encoding) = mimetypes.guess_type(image_url)
    return mimetype


def get_extension_from_type(type_string):
    if type(type_string) == str or type(type_string) == unicode:
        temp = type_string.split('/')
        if len(temp) >= 2:
            return temp[1]
        elif len(temp) >= 1:
            return temp[0]
        else:
            return None


def get_type(image_url):
    content_type = get_contenttype(image_url)
    if content_type is not None and (("image" in content_type) or ("video" in content_type)):
        return get_extension_from_type(content_type)
    mimetypes = get_mimetype(image_url)
    if mimetypes is not None and (("image" in mimetypes) or ("video" in mimetypes)):
        return get_extension_from_type(mimetypes)
    return None
