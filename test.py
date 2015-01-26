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
		headings = []
		for c in range(len(root)-1, -1, -1):
			if root[c].tag == "h1" or root[c].tag == "h2":
				headings.append(root[c].text)
			del root[c]
		root.text = ""
		for h in reversed(headings):
			root.text += "* " + h + "\n"
		return root

description = '''Github Appliance
=====
The Github appliance will be upgraded to 2.1.0 and the hostname will be reconfigured from github.local. The github appliance will be intermittently available during this time.

Second system
====
Description'''

systemlist = markdown(description, extensions=[HeaderFinder()])

print markdown(systemlist + '\n\n' + description)
