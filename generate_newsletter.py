import sys
import json
import xml.dom.minidom
import lxml.etree as ET


def dict2xml(d, root_node=None):
    """
    Credit: https://gist.github.com/reimund/5435343/
    """

    wrap = False if None == root_node or isinstance(d, list) else True
    root = 'objects' if None == root_node else root_node
    root_singular = root[:-1] if 's' == root[-1] and None == root_node else root
    xml_str = ''
    children = []

    if isinstance(d, dict):
        for key, value in dict.items(d):
            if isinstance(value, dict):
                children.append(dict2xml(value, key))
            elif isinstance(value, list):
                children.append(dict2xml(value, key))
            else:
                try:
                    xml_str = xml_str + ' ' + key + '="' + value + '"'
                except TypeError:
                    xml_str = xml_str + ' ' + key + '="' + str(value) + '"'
                except UnicodeDecodeError:
                    xml_str = xml_str + ' ' + key + '="' + value.encode('utf-8') + '"'
                except UnicodeEncodeError:
                    xml_str = xml_str + ' ' + key + '="' + value.decode('utf-8') + '"'
    else:
        for value in d:
            children.append(dict2xml(value, root_singular))

    end_tag = '>' if 0 < len(children) else '/>'

    if wrap or isinstance(d, dict):
        xml_str = '<' + root + xml_str + end_tag

    if 0 < len(children):
        for child in children:
            xml_str = xml_str + child

        if wrap or isinstance(d, dict):
            xml_str = xml_str + '</' + root + '>'

    return xml_str


def file2string(filepath):
    with open(filepath, 'r') as file:
        return file.read().replace('\n', '')


if __name__ == "__main__":
    print('Generating newsletter...')

    # load json file to dict
    feed_dict = {"stories": json.loads(file2string(sys.argv[1]))}

    # convert json dict to xml
    feed_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    feed_xml += '<?xml-stylesheet type="text/xsl" href="feed.xsl" ?>\n'
    feed_xml += dict2xml(feed_dict)

    # get pretty printed XML document
    xml = xml.dom.minidom.parseString(  feed_xml.encode("UTF-8"))
    pretty_xml_as_string = xml.toprettyxml()

    # save xml as a file
    with open('feed.xml', 'w') as outfile:
        outfile.write(pretty_xml_as_string.encode("UTF-8"))
        outfile.close()

    # convert XML to HTML with regard to XSL
    dom = ET.parse('feed.xml')
    xslt = ET.parse('feed.xsl')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    http_string = ET.tostring(newdom, pretty_print=True)

    # save html as a file
    with open('feed.html', 'w') as outfile:
        outfile.write(http_string.encode("UTF-8"))
        outfile.close()

    print('Finished generating newsletter.')
