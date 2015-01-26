#!/usr/bin/python
from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree.ElementTree import *
import urllib2
import vobject

# This is called when markdown() is called on some text


class HeaderFinder(Extension):

    def extendMarkdown(self, md, md_globals):
        ext = MyTreeprocessor(md)
        md.treeprocessors.add("toc", ext, "<prettify")


# This is called from HeaderFinder()
class MyTreeprocessor(Treeprocessor):

    def run(self, root):
        # Prepare an array to hold the headings we find
        headings = []
        # loop through each top level element
        for c in range(len(root) - 1, -1, -1):
            # If it's a h1 or h2, add the text to our heading
            if root[c].tag == "h1" or root[c].tag == "h2":
                headings.append(root[c].text)
            # delete the element because we're totally changing our root
            del root[c]
        # start our table
        new_root = SubElement(root, "ul")
        for h in reversed(headings):
            item = SubElement(new_root, "li")
            item.text = h
        # return our modified root
        return root


req = urllib2.Request(
    'https://www.google.com/calendar/ical/uq2m73m8lvm2hf86nbfl9g8gkk%40group.calendar.google.com/private-12556f00fa50f0f4a10c2dcf65d7771f/basic.ics')
response = urllib2.urlopen(req)
icalstream = response.read()

parsedCal = vobject.readOne(icalstream)
print parsedCal.vevent.dtstart.value
description = parsedCal.vevent.description.value

systemlist = markdown(description, extensions=[HeaderFinder()])

print systemlist
