#!/usr/bin/env python

# FlickrGetter.py
# Seth Hoenig (c) April 2011

import sys
import os
import urllib

class Getter:
    def __init__(self, pagemin=None, pagemax=None, urlbase=None, size=None,
                       destdir="~/", imgbase=None, imgend=None):
        if urlbase==None or size==None or imgbase==None or imgend==None:
            print "Invlaid Setup: "
            print "\tsize: %s"    % str(size)
            print "\tpagemin: %s" % str(pagemin)
            print "\tpagemax: %s" % str(pagemax)
            print "\turlbase: %s" % str(urlbase)
            print "\tdestdir: %s" % str(destdir)
            print "\timgbase: %s" % str(imgbase)
            print "\timgend: %s"  % str(imgend)
            sys.exit(-1)
       
        self.pagemax = pagemax
        self.pagemin = pagemin
        self.urlbase = urlbase
        self.destdir = destdir
        self.imgbase = imgbase
        self.imgend = imgend
        self.size = size

        self.ignore = self.getIgnoreSet() 

        print "ignore: %s" % str(self.ignore)

    def executeGets(self):
        for i in xrange(self.pagemin, self.pagemax+1):
            print "Working on page: %d" % i
            self.doPage(i)

    def getIgnoreSet(self):
        files = set()
        c = 0
        flist = os.listdir(self.destdir)
        for file in flist:
            files.add(file.strip('.jpg'))
        return files

    def doPage(self, curPage):
        urlstr = self.urlbase + str(curPage) + "/"
        #print "urlstr: %s" % urlstr
        f = urllib.urlopen(urlstr)
        content = f.read()
        f.close()
        #print content
        splitted = content.split('"')
        for s in  splitted:
            s = s.strip()
            if "sv_title_" in s:
                imgnum = s.split("_")[2]
                print "image: %s" % imgnum,
                if imgnum in self.ignore:
                    print " ...ignore"
                else:
                    print " ...get"
                    self.getImage(imgnum)

    def getImage(self, imgnum):
        imgpageurl = self.imgbase + imgnum + self.imgend
        f = urllib.urlopen(imgpageurl)
        content = f.read()
        f.close()
        splitted = content.split('"')
        for s in splitted:
            s = s.strip()
            if "_"+self.size+".jpg" in s:
                print "imgurl: %s" % s
                self.downloadImage(s, imgnum)

    def downloadImage(self, imgurl, imgnum):
        fpath = self.destdir + "/" + imgnum + ".jpg" 
        dlimage = file(fpath, "wb")
        img = urllib.urlopen(imgurl)
        while True:
            buf = img.read(65536)
            if len(buf) == 0:
                break
            dlimage.write(buf)
        dlimage.close()
        img.close()


if __name__ == "__main__":
    test = True

    if test:
        print "-- Testing Getter Class --"
        PAGEMIN = 1
        PAGEMAX = 1
        SIZE = "o"
        URLBASE = "http://www.flickr.com/photos/gracepointaustin/page"
        DESTDIR = "/Users/seth/Pictures/KoinoniaFlickr"
        IMGBASE = "http://www.flickr.com/photos/gracepointaustin/"
        IMGEND = "/sizes/o/in/photostream/"

        
        g = Getter(PAGEMIN,PAGEMAX,URLBASE,SIZE,DESTDIR,IMGBASE,IMGEND)
        g.executeGets()

    else:
        pass
        # run normal mode
