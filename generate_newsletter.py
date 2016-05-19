import sys
import json
import xml.dom.minidom

def dict2xml(d, root_node=None):
    """
    Credit: https://gist.github.com/reimund/5435343/
    """

    wrap = False if None == root_node or isinstance(d, list) else True
    root = 'objects' if None == root_node else root_node
    root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
    xml = ''
    children = []

    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, dict):
                children.append(dict2xml(value, key))
            elif isinstance(value, list):
                children.append(dict2xml(value, key))
            else:
                try:
                    xml = xml + ' ' + key + '="' + value + '"'
                except TypeError:
                    xml = xml + ' ' + key + '="' + str(value) + '"'
                except UnicodeDecodeError:
                    xml = xml + ' ' + key + '="' + value.encode('utf-8') + '"'
                except UnicodeEncodeError:
                    xml = xml + ' ' + key + '="' + value.decode('utf-8') + '"'
    else:
        for value in d:
            children.append(dict2xml(value, root_singular))

    end_tag = '>' if 0 < len(children) else '/>'

    if wrap or isinstance(d, dict):
        xml = '<' + root + xml + end_tag

    if 0 < len(children):
        for child in children:
            xml = xml + child

        if wrap or isinstance(d, dict):
            xml = xml + '</' + root + '>'

    return xml


def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')


if __name__ == "__main__":

    # load json file to dict
    feed_dict = {"stories": json.loads(file2string(sys.argv[1]))}

    # convert json dict to xml
    feed_xml = '<?xml version="1.0" encoding="UTF-8"?>' + dict2xml(feed_dict)

    # save xml as a file
    with open('feed.xml', 'w') as outfile:

        xml = xml.dom.minidom.parseString(feed_xml.encode("UTF-8"))
        pretty_xml_as_string = xml.toprettyxml()

        outfile.write(pretty_xml_as_string.encode("UTF-8"))
        outfile.close()
