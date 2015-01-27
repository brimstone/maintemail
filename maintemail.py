#!/usr/bin/python
import sys
import getopt
# for markdown processing
from markdown import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
# for ics feed
import urllib2
import vobject
# for email
from mailer import Mailer
from mailer import Message


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


def usage(message=""):
    # TODO fill this out
    print message
    print "Usage: icsmailer.py ..."
    sys.exit(2)


def main(argv):

    verbose = False
    ics = ""
    smtp = ""
    template = ""
    try:
        opts, args = getopt.getopt(argv, "hi:u:p:s:t:f:v",
                                   ["help", "ics=", "username=", "password=", "smtp=", "template=", "from=", "verbose"])
        print argv
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-i", "--ics"):
            ics = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-s", "--smtp"):
            smtp = arg
        elif opt in ("-t", "--template"):
            template = arg
        elif opt in ("-f", "--from"):
            fromaddress = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
    # Check to make sure we have everything we need
    if ics == "":
        usage("--ics is required")
    if smtp == "":
        usage("--smtp is required")
    if template == "":
        usage("--template is required")

    req = urllib2.Request(ics)
    response = urllib2.urlopen(req)
    icalstream = response.read()

    # http://vobject.skyhouseconsulting.com/usage.html
    parsedCal = vobject.readOne(icalstream)
    description = parsedCal.vevent.description.value
    if verbose:
        print "Found: " + parsedCal.vevent.summary.value

    headerfinder = HeaderFinder()
    systemdesc = markdown(description, extensions=[headerfinder])

    overview = "On "
    overview += parsedCal.vevent.dtstart.value.strftime(
        "%A, %B %d %Y, from %I:%M%p")
    overview += " to "
    overview += parsedCal.vevent.dtend.value.strftime("%I:%M%p")
    overview += " will be performing maintenance on the following systems:\n\n"

    for h in headerfinder.getHeadings():
        overview += "* " + h + "\n"

    overview += "\n"

    template = open(template, 'r').read()

    template = template.replace("%SYSTEMDESC%", systemdesc)
    template = template.replace("%SUMMARY%", parsedCal.vevent.summary.value)
    template = template.replace(
        "%MONTH%", parsedCal.vevent.dtstart.value.strftime("%B"))
    template = template.replace(
        "%DAY%", parsedCal.vevent.dtstart.value.strftime("%d"))
    template = template.replace("%STARTEND%", parsedCal.vevent.dtstart.value.strftime(
        "%I:%M%p&nbsp;to&nbsp;") + parsedCal.vevent.dtend.value.strftime("%I:%M%p"))
    template = template.replace("%OVERVIEW%", markdown(overview))

    message = Message(From=fromaddress,
                      To=parsedCal.vevent.location.value,
                      Subject="IT Maintenance - " + parsedCal.vevent.summary.value)
    message.Body = overview + description
    message.Html = template

    sender = Mailer(smtp)
    sender.send(message)

if __name__ == "__main__":
    main(sys.argv)
