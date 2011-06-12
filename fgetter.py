#!/usr/bin/env python

# FlickrGetter.py
# Seth Hoenig April 2011

import getopt
import os
import sys 
import urllib

class Getter:

    def __init__(self, size=None, destdir=None, album = None, verbose=False):
        if  size==None or album==None: 
            print 'Invlaid Setup: '
            print '\tsize: %s'    % str(size)
            print '\tdestdir: %s' % str(destdir)
            print '\talbum: %s' % str(album)
            print '...exiting'
            sys.exit(-1)
        
        self.verbose = verbose
        self.urlbase =  'http://www.flickr.com/photos/' + album + '/page'
        self.pagemin = 0
        self.imgbase = 'http://www.flickr.com/photos/' + album + '/'
        self.destdir = destdir
        self.imgend = '/sizes/' + size + '/in/photostream/'
        self.size = size
        self.pagemax = self.getNumPages()

        self.printV( '(%r pages) --' % (self.pagemax))
        self.printV( 'self.urlbase: ' + self.urlbase)
        self.printV( 'self.imgbase: ' + self.imgbase)
        self.printV( 'self.destdir: ' + self.destdir)
        self.printV( 'self.imgend: ' + self.imgend)
        self.printV( 'self.size: ' + self.size)

        self.ignore = self.getIgnoreSet() 

    def printV(self, m):
        if self.verbose:
            print m

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
        self.printV('Total Pages: %r' % (maxpage,))
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
                self.printV('\timage: %s' % imgnum)
                if imgnum in self.ignore:
                    self.printV('\t\tignoring')
                    pass
                else:
                    self.printV('\t\tgetting')
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
                self.printV('imgurl: %r' % (s,))
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

def helpit():
    print 'Getter [-vhdas]'
    print '\t[-v --verbose] print program execution'
    print '\t[-h --help] show this help page'
    print '\t[-d --dest [directory]] folder location where stuff goes'
    print '\t[-a --album [album]] name of album to be downloaded'
    print '\t[-s --size [o|l|m|s]] size of images to download'
    print 'example album: -a gracepointaustin'
    print 'example dest: -d /Users/bobby/Pictures/ChristmasPics'
    print 'example size: -s o'

if __name__ == '__main__':
    test = False

    if not test:
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'vhd:a:s:',
                                ['help','dest','album','verbose','size'])
        except getopt.GetoptError, err:
            print str(err)
            sys.exit(2)
        verbose = False
        helpme = False
        dest = None
        album = None
        size = None
        for o, a in opts:
            if o in ('-v', '--verbose'):
                verbose = True
            elif o in ('-h', '--help'):
                helpme = True
            elif o in ('-d', '--destdir'):
                dest = a
            elif o in ('-a', '--album'):
                album = a
            elif o in ('-s', '--size'):
                size = a
            else:
                print 'Unknown Option'
                helpit()
                sys.exit(0)

        if helpme or not dest or not album or not size:
            helpit()
            sys.exit(0)

        if not size in ('o', 'l', 'm', 's'):
            print 'invalid size'
            helpit()
            sys.exit(0)

        print '-- DOWNLOADING ',
        #size = 'o'
        #URLBASE = 'http://www.flickr.com/photos/gracepointaustin/page'
#       DESTDIR = '/Users/seth/Pictures/Ktemp'
        #destdir = '/Users/seth/Pictures/Koinonia'
        #IMGBASE = 'http://www.flickr.com/photos/gracepointaustin/'
        #album = 'gracepointaustin'

        
        g = Getter(verbose=verbose, size=size, destdir=dest, album=album)
        g.executeGets()

    else:  # test mode
        size = 'o'
        destdir = '/Users/seth/Pictures/Koinonia'
        album = 'gracepointaustin'
        g = Getter(size=size, destdir=destdir, album=album)
        n = g.getNumPages()
        print 'n: %r' % (n,)
