#!/usr/bin/env python

# FlickrGetter.py
# Seth Hoenig April 2011

import sys 
import os
import urllib

class Getter:

    def __init__(self, size=None, destdir=None, album = None):
        if  size==None or album==None: 
            print 'Invlaid Setup: '
            print '\tsize: %s'    % str(size)
            print '\tdestdir: %s' % str(destdir)
            print '\talbum: %s' % str(album)
            print '...exiting'
            sys.exit(-1)
        
        self.urlbase =  'http://www.flickr.com/photos/' + album + '/page'
        self.pagemin = 0
        self.imgbase = 'http://www.flickr.com/photos/' + album + '/'
        self.destdir = destdir
        self.imgend = '/sizes/' + size + '/in/photostream/'
        self.size = size
        self.pagemax = self.getNumPages()
        print '(%r pages) --' % (self.pagemax)
#        print 'self.urlbase: ' + self.urlbase
#        print 'self.imgbase: ' + self.imgbase
#        print 'self.destdir: ' + self.destdir
#        print 'self.imgend: ' + self.imgend
#        print 'self.size: ' + self.size

        self.ignore = self.getIgnoreSet() 

    def getNumPages(self):
        f = urllib.urlopen(self.imgbase)
        content = f.read()
        f.close()
        splitted = content.split('/')
        maxpage = 0
        for s in splitted:
            s = s.strip()
            if len(s) >= 5 and s[0:4] == 'page':
                val = int(s[4:])
                if val > maxpage:
                    maxpage = val
        return maxpage

    def executeGets(self):
        for i in xrange(self.pagemin, self.pagemax+1):
            print 'Working on page: %d' % i
            all_ignored = self.doPage(i)
            if all_ignored:
                print 'Done.'
                break

    def getIgnoreSet(self):
        files = set()
        c = 0
        flist = os.listdir(self.destdir)
        for file in flist:
            files.add(file.strip('.jpg'))
        return files

    def doPage(self, curPage):
        urlstr = self.urlbase + str(curPage) + '/'
        f = urllib.urlopen(urlstr)
        content = f.read()
        f.close()
        splitted = content.split('"')
        all_ignored = True
        for s in  splitted:
            s = s.strip()
            if 'sv_title_' in s:
                imgnum = s.split('_')[2]
                #print '\timage: %s' % imgnum,
                if imgnum in self.ignore:
                    #print ' ...ignore'
                    pass
                else:
                    #print ' ...get'
                    self.getImage(imgnum)
                    all_ignored = False
        return all_ignored

    def getImage(self, imgnum):
        imgpageurl = self.imgbase + imgnum + self.imgend
        f = urllib.urlopen(imgpageurl)
        content = f.read()
        f.close()
        splitted = content.split('"')
        for s in splitted:
            s = s.strip()
            if '_'+self.size+'.jpg' in s:
                print 'imgurl: %s' % s
                self.downloadImage(s, imgnum)

    def downloadImage(self, imgurl, imgnum):
        fpath = self.destdir + '/' + imgnum + '.jpg' 
        dlimage = file(fpath, 'wb')
        img = urllib.urlopen(imgurl)
        while True:
            buf = img.read(65536)
            if len(buf) == 0:
                break
            dlimage.write(buf)
        dlimage.close()
        img.close()


if __name__ == '__main__':
    test = False

    if not test:
        print '-- RUNNING ',
        SIZE = 'o'
        #URLBASE = 'http://www.flickr.com/photos/gracepointaustin/page'
#       DESTDIR = '/Users/seth/Pictures/Ktemp'
        DESTDIR = '/Users/seth/Pictures/Koinonia'
        #IMGBASE = 'http://www.flickr.com/photos/gracepointaustin/'
        ALBUM = 'gracepointaustin'

        
        g = Getter(size=SIZE,destdir=DESTDIR, album=ALBUM)
        g.executeGets()

    else:  # test mode
        size = 'o'
        destdir = '/Users/seth/Pictures/Koinonia'
        album = 'gracepointaustin'
        g = Getter(size=size, destdir=destdir, album=album)
        n = g.getNumPages()
        print 'n: %r' % (n,)

