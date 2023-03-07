import xml.etree.ElementTree as ET


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


xml_path = ".\\gbXML\\building_test.xml"
tree = ET.parse(xml_path)
root = tree.getroot()
print(is_iterable(root[0]))

for child in root:
    # print(type(child.tag))
    if 'Campus' in child.tag and is_iterable(child.tag):
        for sub_child in child:
            if 'Surface' in sub_child.tag:
                print(sub_child.get('surfaceType'))

# for element in root:
#
#     print(element[0].tag)


