import encodings
import sys
import os
import urllib2
import re

from lxml import etree

#TODO: Change the other xpaths to use this since its much more succinct
def rssxpath(e, path):
    return e.xpath(path, namespaces={
        "rss":"http://purl.org/rss/1.0/",
        "rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "slash":"http://purl.org/rss/1.0/modules/slash/",
        "content":"http://purl.org/rss/1.0/modules/content/",
        "taxo":"http://purl.org/rss/1.0/modules/taxonomy/",
        "dc":"http://purl.org/dc/elements/1.1/",
        "syn":"http://purl.org/rss/1.0/modules/syndication/",
        "admin":"http://webns.net/mvcb/"
        })



#xml = etree.parse(urllib2.urlopen("http://rss.slashdot.org/Slashdot/slashdotMain"))
xml = etree.parse(open("example_slashdot.rss","r"))

root = xml.getroot()
print(root)

rdf = rssxpath(xml.getroot(), "//rdf:RDF")[0]
print(rdf)

entries = rssxpath(rdf, "./rss:item")

for e in rdf :
    print(e)

if len(sys.argv) > 1:
    outdir =  sys.argv[1] 
else:
    outdir = "default"

try:
    os.mkdir( outdir )
except OSError:
    print("Directory exists - reusing!")

r = re.compile(r"https://(\w+)\.slashdot\.org/story/(\d+)/(\d+)/(\d+)/(\d+)/([\w-]+)")
for e in entries :
    # TODO: Use this to generate the output directory
    link = rssxpath(e, "./rss:link/text()")[0]
    #TODO: CLean the extra cruft out of the link (?utm_source=rss1.0mainlinkanon&utm_medium=feed) 
    link = re.sub("\?.*","",link,0,re.DOTALL)

    g = r.match(link)
    if not g :
        print("Unable to parse id for "+link)
        continue
    idx = "slashdot-%s-%s-%s-%s-%s" % ( g.group(2), g.group(3), g.group(4), g.group(5), g.group(6) )
    print("Processing "+idx)
    # TODO: Check the file doesn't already exist!
    if os.path.exists(outdir + "/" + idx + ".md"):
        print( "Already have an entry for " + idx )
        continue
    f=open(outdir + "/" + idx + ".md", "w")
    
    f.write( "# " + rssxpath(e,"./rss:title/text()")[0].replace("\n"," " ) + "\n" )
    f.write( link + "\n" )
    description = rssxpath(e, "./rss:description/text()")
    # Slashdot adds a whole lot of cruft at the end of the RSS description
    # Lets trim it out.
    description = re.sub("<p>.*","",description[0],0, re.DOTALL) 
    # TODO: Prep this with leading > marks
    description = re.sub("^", "> ", description,0, re.MULTILINE) 
    f.write( encodings.utf_8.encode(description)[0] )

    ### print( "\n" )
    ###print( axpath(e, "./Atom:summary/text()")[0] + "\n" )
