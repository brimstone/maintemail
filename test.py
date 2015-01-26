#!/usr/bin/python
from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import urllib2
import vobject

# This is called when markdown() is called on some text


class HeaderFinder(Extension):

    def __init__(self):
        self.headings = []
        Extension.__init__(self)

    def extendMarkdown(self, md, md_globals):
        ext = MyTreeprocessor(md)
        md.treeprocessors.add("toc", ext, "<prettify")
        self.headings = ext.getHeadings()

    def getHeadings(self):
        return self.headings


# This is called from HeaderFinder()
class MyTreeprocessor(Treeprocessor):

    # Prepare an array to hold the headings we find
    def __init__(self, md):
        self.headings = []
        Treeprocessor.__init__(self, md)

    def run(self, root):
        # loop through each top level element
        for c in range(len(root) - 1, -1, -1):
            # If it's a h1 or h2, add the text to our heading
            if root[c].tag == "h1" or root[c].tag == "h2":
                self.headings.append(root[c].text)
        return root

    def getHeadings(self):
        return self.headings


req = urllib2.Request(
    'https://www.google.com/calendar/ical/uq2m73m8lvm2hf86nbfl9g8gkk%40group.calendar.google.com/private-12556f00fa50f0f4a10c2dcf65d7771f/basic.ics')
response = urllib2.urlopen(req)
icalstream = response.read()

# http://vobject.skyhouseconsulting.com/usage.html
parsedCal = vobject.readOne(icalstream)
print parsedCal.vevent.dtstart.value
description = parsedCal.vevent.description.value

headerfinder = HeaderFinder()
systemdesc = markdown(description, extensions=[headerfinder])

print systemdesc

print headerfinder.getHeadings()
