import os
import sys
from xml.etree import ElementTree as ET

def createTargetDirectory():
    try:
        os.mkdir('./jQuery')
    except OSError, e:
        print "OSError", e
        sys.exit("Could not create target directory. Exiting gracefully.")

def getEntryClippingDetails(entry):
    """Gets a list of dictionary objects for each method signature version.

    Each dictionary has `filename` and 'content' keys.

    """
    format = "%s(%s)"
    methodName = entry.get('name')
    clippingsList = []

    sigs = entry.findall('./signature') #list
    for s in sigs:
        d = {}
        d["filename"] = format % (methodName,", ".join([a.get('name') for a in s.findall('./argument')]))
        d["content"]  = format % (methodName,", ".join(["<#%s#>" % a.get('name') for a in s.findall('./argument')]))
        clippingsList.append(d)
        # and do dollar shortcuts
        if d["filename"].startswith('jQuery'):
            s = {}
            s["filename"] = d["filename"].replace('jQuery','$',1)
            s["content"] = d["content"].replace('jQuery','$',1)
            clippingsList.append(s)
    return clippingsList

def writeClippingFile(dictionary):
    """Creates clipping file.

    Dictionary param needs `filename` and `content` keys.

    """
    filename = dictionary["filename"]
    content  = dictionary["content"]

    path = "./jQuery/%s" % filename
    try:
        f = open(path, "w")
        f.write(content)
    except IOError, e:
        print e
        sys.exit("Failed to write file. Exiting gracefully.")
    finally:
        f.close()

def main():
    createTargetDirectory()

    jquery = ET.parse('jquery.api.xml')
    for entry in jquery.findall('/entries/entry'):
        [writeClippingFile(d) for d in getEntryClippingDetails(entry)]

def clippingsDetailsTest():
    jquery = ET.parse('jquery.api.xml')
    entry = jquery.find('/entries/entry')
    print getEntryClippingDetails(entry)

if __name__ == "__main__":
    main()