#!/usr/bin/python
from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from xml.etree.ElementTree import *

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


description = '''Github Appliance
=====
The Github appliance will be upgraded to 2.1.0 and the hostname will be reconfigured from github.local. The github appliance will be intermittently available during this time.

Second system
====
Description'''

systemlist = markdown(description, extensions=[HeaderFinder()])

print systemlist
print
print markdown(description)
