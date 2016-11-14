import encodings
import sys
import os
import urllib2
from lxml import etree
import re

#TODO: Change the other xpaths to use this since its much more succinct
def axpath(e, path):
    return e.xpath(path, namespaces={'Atom':'http://www.w3.org/2005/Atom'})

def axtext(e, path):
    return [ encodings.utf_8.encode(ee) for ee in axpath(e, path+"/text()") ]

def download(url, file_name):
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,
    f.close()

print("Downloading query results")
data=urllib2.urlopen("http://export.arxiv.org/api/query?search_query=cat:cs.NE&sortBy=submittedDate&start=0&max_results=30")
print(data)
xml = etree.parse(data)
#xml = etree.parse(open("example.atom","r"))
print(xml)
entries = axpath(xml.getroot(), "//Atom:entry")

if len(sys.argv) > 1:
    outdir =  sys.argv[1]
else:
    outdir = "_posts"

try:
    os.mkdir( outdir )
except OSError:
    print("Directory exists - reusing!")

for e in entries :
    base = axpath(e, "./Atom:id/text()")[0].replace("http://arxiv.org/abs/","")
    published = axpath(e, "./Atom:published/text()")[0]
    published = re.sub("T.*$","", published)


    filename = published+"-arxiv-"+re.sub("v.$","", base).replace(".","-")+".md"
    print("Processing "+filename)
    if os.path.exists(outdir + "/" + filename):
        print( "Already have an entry for " + filename )
        continue
    f=open(outdir + "/" + filename, "w")
    url = axpath(e, "./Atom:link[@type='application/pdf']/@href")[0]
    f.write("---\n")
    f.write("title: \""+encodings.utf_8.encode(axpath(e,"./Atom:title/text()")[0])[0].replace("\n"," " )+"\"\n")
    f.write("source: \"" + url + "\"\n")
    f.write("authors:\n")
    for a in axpath(e, "./Atom:author/Atom:name/text()"):
        f.write("  - \"" + encodings.utf_8.encode(a)[0] + "\"\n")

    f.write("tags:\n")
    f.write("  - arxiv\n")
    f.write("  - needs-commentary\n")
    # TODO: Get the thisweekid better!
    f.write("published_in:\n")
    f.write("  - grimsheep-research\n")
    f.write("abstract: |\n")
    description = axpath(e, "./Atom:summary/text()")[0]
    description = re.sub("^ *","",description, 0, re.MULTILINE)
    description = re.sub("^", "  ", description, 0, re.MULTILINE)
    f.write( encodings.utf_8.encode(description)[0] )
    f.write("\n")
    f.write("---\n")
