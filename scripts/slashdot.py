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



xml = etree.parse(urllib2.urlopen("http://rss.slashdot.org/Slashdot/slashdotMain"))
#xml = etree.parse(open("example_slashdot.rss","r"))

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
    outdir = "_leads"

try:
    os.mkdir( outdir )
except OSError:
    print("Directory exists - reusing!")

r = re.compile(r"https://(\w+)\.slashdot\.org/story/(\d+)/(\d+)/(\d+)/(\d+)/([\w-]+)")
filt = re.compile(r"\bai\b|deep.*learn|machine.*learn|neural|quantum", re.I | re.S)
for e in entries :
    title = encodings.utf_8.encode(rssxpath(e,"./rss:title/text()")[0])[0].replace("\n"," " )
    description = rssxpath(e, "./rss:description/text()")
    # Slashdot adds a whole lot of cruft at the end of the RSS description
    # Lets trim it out.
    description = re.sub("<p>.*","",description[0],0, re.DOTALL)

    if not filt.search(description):
        print "skipping "+title
        continue
    else:
        print "processing "+title

    description = re.sub("^", "> ", description,0, re.MULTILINE)


    # TODO: Use this to generate the output directory
    link = rssxpath(e, "./rss:link/text()")[0]
    #TODO: CLean the extra cruft out of the link (?utm_source=rss1.0mainlinkanon&utm_medium=feed)
    link = re.sub("\?.*","",link,0,re.DOTALL)

    g = r.match(link)
    if not g :
        print("Unable to parse id for "+link)
        continue
    filename = "20%s-%s-%s-slashdot-%s-%s.md" % ( g.group(2), g.group(3), g.group(4), g.group(5), g.group(6) )

    print("Processing "+filename)
    if os.path.exists(outdir + "/" + filename):
        print( "Already have an entry for " + filename )
        continue
    # TODO: Need to filter these based on their content!
    f=open(outdir + "/" + filename, "w")
#    url = axpath(e, "./Atom:link[@type='application/pdf']/@href")[0]
    f.write("---\n")
    f.write("title: \""+title+"\"\n")
    f.write("source: \"" + link + "\"\n")
#    f.write("authors:\n")
#    for a in axpath(e, "./Atom:author/Atom:name/text()"):
#        f.write("  - \"" + encodings.utf_8.encode(a)[0] + "\"\n")

    f.write("tags:\n")
    f.write("  - slashdot\n")
    f.write("  - needs-commentary\n")
#    # TODO: Get the thisweekid better!
    f.write("thisweekid: crazydragon\n")
    f.write("---\n")


    f.write( encodings.utf_8.encode(description)[0] )
