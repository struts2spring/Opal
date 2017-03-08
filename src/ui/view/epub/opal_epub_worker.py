import os
import xml.dom.minidom
import zipfile


class EpubBook:
    # class constants:
    subjectTag = 'dc:subject'
    image_exts = [ ".jpg", ".jpeg", ".gif", ".png", ".svg", ".pdf" ]

    def __init__(self):
        self.filename = None
        self.zip = None
        self.dom = None
        self.contentfile = None

    def open(self, filename):
        '''Open an epub file and set up handles to the zip archive
           and the DOM for the OPF file with all the metadata.
        '''
        if not zipfile.is_zipfile(filename):
            raise RuntimeError(filename + " isn't an epub file (not zipped)")

        self.filename = filename
        self.zip = zipfile.ZipFile(filename)
        self.replace_files = {}

    def namelist(self):
        return self.zip.namelist()

    def parse_contents(self):
        # Parse the OPF file into self.dom.
        if not self.zip:
            raise RuntimeError('Epub book not opened')

        for f in self.zip.namelist():
            if os.path.basename(f).endswith('.opf'):
                if self.contentfile:
                    raise RuntimeError("Multiple opf files in %s"
                                       % self.filename)
                self.contentfile = f
                content = self.zip.open(f)
                break
        if not content:
            raise RuntimeError('No .opf file in %s' % self.filename)
            return

        # Now content is a file handle on the content.opf XML file
        try:
            self.dom = xml.dom.minidom.parse(content)
        except IOError, e:
            raise IOError, self.filename + ': ' + str(e)

        content.close()

    def close(self):
        self.zip.close()
        self.filename = None
        self.zip = None
        self.dom = None
 
    def get_matches(self, elname, delete_tags=False):
        '''Find matching tags in the OPF DOM.
           If delete_tags is true, all such tags will be deleted
           along with any children.
        '''
        if not self.dom:
            self.parse_contents()

        elements = self.dom.getElementsByTagName(elname)
        parent = None
        matches = []
        for el in elements:
            # Obviously there should be more error checking here
            if not parent:
                parent = el.parentNode
            else:
                assert parent == el.parentNode

            if delete_tags:
                if el.childNodes:
                    print "Deleting:", el.childNodes[0].wholeText
                else:
                    print "Deleting empty", elname, "tag"
                el.parentNode.removeChild(el)

            elif el.childNodes:
                # el.childNodes[0].wholeText is the unicode.
                # Turn it into UTF-8 before returning.
                # Uncomment the next line and run on micromegas.epub
                # to test a weird thing: it happens if you run
                # epubtag.py micromegas.epub | cat
                # but not if you just run
                # epubtag.py micromegas.epub
                # See http://stackoverflow.com/questions/492483/setting-the-correct-encoding-when-piping-stdout-in-python
                # matches.append(el.childNodes[0].wholeText)
                matches.append(el.childNodes[0].wholeText.encode('utf-8',
                                                        'backslashreplace'))
            else:
                print "Empty", elname, "tag"

        return matches, elements, parent

    def get_titles(self):
        '''Get the title for this work. Returns a list since it's
           possible for an epub to have more than one title.
        '''
        titles, elements, parent = self.get_matches('dc:title')
        return titles

    def get_title(self):
        '''Get the first (perhaps only) title.
        '''
        return self.get_titles()[0]

    def set_title(self, newtitle):
        titles, elements, parent = self.get_matches('dc:title')
        for el in elements:
            if el.firstChild.nodeType == el.TEXT_NODE:
                el.firstChild.replaceWholeText(newtitle)
            else:
                print "Error: dc:title contains something other than text"

    def get_authors(self):
        '''Get the list of authors (perhaps only one of them).
        '''
        authors, elements, parent = self.get_matches('dc:creator')
        return authors

    def get_tags(self):
        '''Get all tags in this epub book.
        '''
        # Tags are inside <metadata> and look like this:
        # <metadata>
        #   <dc:subject>Presidents -- United States -- Biography</dc:subject>
        # Author (dc:creator) and Title (dc:title) are stored similarly.

        tags, elements, parent = self.get_matches(self.subjectTag)
        return tags

    def info_string(self, brief=False):
        '''Return an info string describing this book, suitable for printing.
        '''
        outstr = self.filename + '\n'

        # grab the title and author
        titles = self.get_titles()
        if brief:
            outstr += ', '.join(titles) + " | "
        else:
            for t in titles:
                outstr += "Title: " + t + "\n"

        authors = self.get_authors()
        if brief:
            outstr += ', '.join(authors) + ' | '
        else:
            if len(authors) > 1:
                outstr += "Authors: "
            else:
                outstr += "Author: "
            outstr += ', '.join(authors) + "\n"

        tags = self.get_tags()
        if brief:
            outstr += ', '.join(tags)
        else:
            if tags:
                outstr += "Tags: "
                for tag in tags:
                    outstr += '\n   ' + tag

        return outstr

    def delete_tags(self):
        '''Delete all tags in the book.
        '''
        tags, elements, parent = self.get_matches(self.subjectTag, True)

    def add_tags(self, new_tag_list):
        '''Add the given tags to any tags the epub already has.
        '''
        tags, elements, parent = self.get_matches(self.subjectTag)

        lowertags = [ s.lower() for s in tags ]

        # If we didn't see a dc:subject, we still need a parent,
        # the <metadata> tag.
        if not parent:
            print "Warning: didn't see any subject tags previously"
            parent = self.dom.getElementsByTagName("metadata")[0]

            # If there's no metadata tag, maybe we should add one,
            # but it might be better to throw an error.
            if not parent:
                raise RuntimeError("No metadata tag! Bailing.")

        # We'll want to add the new subject tags after the last one.
        if elements:
            last_tag_el = elements[-1]
        else:
            last_tag_el = None

        for new_tag in new_tag_list:
            # Don't add duplicate tags (case-insensitive).
            new_tag_lower = new_tag.lower()
            if new_tag_lower in lowertags:
                print "Skipping duplicate tag", new_tag
                continue

            # Make the new node:
            # newnode = tag.cloneNode(False)
            newnode = self.dom.createElement(self.subjectTag)

            # Make a text node inside it:
            textnode = self.dom.createTextNode(new_tag)
            newnode.appendChild(textnode)

            # Also add a newline after each new node
            textnode = self.dom.createTextNode('\n')

            # Append newnode after the last tag node we saw:
            if last_tag_el and last_tag_el.nextSibling:
                parent.insertBefore(textnode, last_tag_el.nextSibling)
                parent.insertBefore(newnode, textnode)
            # If we didn't see a tag, or the tag was the last child
            # of its parent, we have to do it this way:
            else:
                parent.appendChild(newnode)
                parent.appendChild(textnode)

            print "Adding:", new_tag

    def replace_file(self, oldfilename, newfile):
        '''When we save_changes, replace the contents of oldfilename
           (without changing its filename) with the contents of newfile,
           a filename on the local filesystem.
        '''
        self.replace_files[oldfilename] = newfile

    def save_changes(self):
        '''Overwrite the old file with any changes that have been
           made to the epub's tags. The old file will be backed
           up in filename.bak.
        '''
        # Open a new zip file to write to, and copy everything
        # but change the content.opf (or whatever.opf) to the new one:
        new_epub_file = self.filename + '.tmp'
        ozf = zipfile.ZipFile(new_epub_file, 'w')
        for info in self.zip.infolist():
            if info.filename in self.replace_files:
                fp = open(self.replace_files[info.filename])
                ozf.writestr(info, fp.read())
                fp.close()
            elif info.filename == "mimetype":
                # The mimetype file must be written uncompressed.
                ozf.writestr(info, self.zip.read(info.filename),
                             zipfile.ZIP_STORED)
            elif info.filename.endswith('.opf'):
                # dom.toprettyprintxml() returns unicode, which
                # zipfile.writestr() can't write. If you pass in
                # encoding= then it works ... but minidom gives us
                # no way to find out the encoding of the XML file
                # we just parsed! So the best we can do is force
                # it to UTF-8, barring re-opening the file and
                # parsing the first line manually. So crazy!
                encoding = 'UTF-8'
                ozf.writestr(info, self.dom.toprettyxml(encoding=encoding,
                                                        newl=''))
                # This also works:
                # ozf.writestr(info,
                #              self.dom.toprettyxml().encode(encoding,
                #                                      'xmlcharrefreplace'))
            else:
                # For every other file, just copy directly.
                ozf.writestr(info, self.zip.read(info.filename))

        ozf.close()

        # Now we have the new file in new_epub_file, old in filename.
        # Rename appropriately:
        bakfile = self.filename + ".bak"
        os.rename(self.filename, bakfile)
        os.rename(new_epub_file, self.filename)
        print "Wrote", self.filename
        os.remove(bakfile)

    def extract_cover_image(self, name=None, outdir=''):
        '''Extract just an image named cover.*.
           Return (newfilename, filename_in_zip_archive)
        '''
        '''
        Notes on covers: the epub format doesn't actually specify how to make
        a cover, so apparently there are all sorts of different conventions.

        Gutenberg books tend to have
        <metadata>
            <meta content="item8" name="cover"/>
        </metadata>
        <manifest>
            <item href="cover.jpg" id="item8" media-type="image/jpeg"/>
        </manifest>
        <guide>
            <reference href="cover.jpg" title="Cover Image" type="cover"/>
        </guide>

        A book converted from HTML with early Calibre has:
        <metadata>
            <meta content="cover" name="cover"/>
        </metadata>
        <manifest>
            <item href="Images/cover_image.jpg" id="cover" media-type="image/jpeg"/>
        </manifest>
        <guide>
            <reference href="Text/titlepage.xhtml" title="Title Page" type="cover"/>
        </guide>

        A StoryBundle book has:
        <metadata>
            <meta name="cover" content="cover"/>
        </metadata>
        <manifest>
            <item href="cover.jpeg" id="cover" media-type="image/jpeg"/>
        </manifest>
        <guide>
            <reference href="titlepage.xhtml" title="Cover" type="cover"/>
        </guide>

        A random commercial book has:
        <metadata>
            <meta content="coverimg" name="cover"/>
            <meta content="cover-image" name="cover"/>
        </metadata>
        <manifest>
            <item href="OEBPS/images/bookname_epub3_001_cvi.jpg" id="coverimg" media-type="image/jpeg" properties="cover-image"/>
        </manifest>
        <guide>
            <reference href="OEBPS/bookname_epub3_cvi_r1.xhtml" title="Cover" type="cover"/>
        </guide>

        What O'Reilly says to have:
        <metadata>
            <meta name="cover" content="cover-image" />
        </metadata>
        <manifest>
            <item id="cover" href="cover.html" media-type="application/xhtml+xml"/>
            <item id="cover-image" href="the_cover.jpg" media-type="image/jpeg"/>
        </manifest>
        <guide>
            <reference href="cover.html" type="cover" title="Cover"/>
        </guide>

        What the MobileRead Wiki says to have:
        <metadata>
             <meta name="cover" content="cover-image"/>
        </metadata>
        <manifest>
             <item id="cover" href="the-cover-filename.xhtml" media-type="application/xhtml+xml"/>
             <item id="cover-image" href="the_cover.jpg" media-type="image/jpeg"/>
        </manifest>
        <guide>
            <reference type="cover" href="the-cover-filename.xhtml" />
        </guide>

        Practically, what to look for:
        1. <item id="cover-image" in <manifest>  # O'Reilly/MobileReads rec
        2. <item id="coverimg" in <manifest>     # Commercial
        3. <item id="cover" in <manifest>        # Early Calibre
        4. <reference type="cover" in <guide>    # Gutenberg
        What a mess!

        Some URLs suggesting best practices:
        https://www.safaribooksonline.com/blog/2009/11/20/best-practices-in-epub-cover-images/
        http://wiki.mobileread.com/wiki/Ebook_Covers
        http://www.chickensinenvelopes.net/2013/01/setting-a-cover-image-on-an-epub-ebook/
        '''

        coverimg = None
        parent = self.dom.getElementsByTagName("manifest")[0]
        for item in parent.getElementsByTagName("item"):
            id = item.getAttribute("id").lower()
            if id.startswith("cover"):
                coverimg = item.getAttribute("href")
                base, ext = os.path.splitext(coverimg)
                if ext in self.image_exts:
                    break
                # If it doesn't end with an image type, we can't use it
                coverimg = None

        # If we didn't find one in the manifest, try looking in guide:
        if not coverimg:
            guide = self.dom.getElementsByTagName("guide")
            if guide:
                parent = guide[0]
                for item in parent.getElementsByTagName("reference"):
                    if item.getAttribute("type").lower() == "cover":
                        coverimg = item.getAttribute("href")
                        base, ext = os.path.splitext(coverimg)
                        if ext in self.image_exts:
                            break
                        # If it doesn't end with an image type, we can't use it
                        coverimg = None

        # If all else fails, go back to the manifest and look for
        # anything named cover.jpg. This is the only recourse for
        # many Project Gutenberg books.
        if not coverimg:
            parent = self.dom.getElementsByTagName("manifest")[0]
            for item in parent.getElementsByTagName("item"):
                href = item.getAttribute("href")
                base, ext = os.path.splitext(os.path.basename(href))
                if base.lower() == "cover":
                    coverimg = href

        if not coverimg:
            return None, None

        infp = None
        base = os.path.basename(coverimg)

        # If we get here, we think we have the name of the cover image file.
        # Unfortunately, it's not necessarily a full path.
        # We may need to search for it in the zip.
        try:
            infp = self.zip.open(coverimg)
        except KeyError:
            for f in self.zip.namelist():
                if os.path.basename(f) == base:
                    infp = self.zip.open(f)
                    coverimg = f
        if not infp:
            print "Couldn't find", coverimg, "in zip archive"
            return None, None

        outfilename = os.path.join(outdir, base)
        if name == None:
            return None, None
        else:
            outfp = open(name, 'w')
            outfp.write(infp.read())
            infp.close()
        outfp.close()
        return outfilename, coverimg

    def extract_images(self, outdir=''):
        '''Extract all images in the book.
        '''
        print "Extracting images from", self.filename,
        if outdir:
            print "to", outdir
        else:
            print

        for f in self.zip.namelist():
            ext = os.path.splitext(f)[-1].lower()
            if ext in self.image_exts:
                infp = self.zip.open(f)
                outfilename = os.path.join(outdir, os.path.basename(f))
                i = 1
                while os.path.exists(outfilename):
                    print os.path.basename(outfilename), "already exists"
                    se = os.path.splitext(outfilename)
                    outfilename = se[0] + '-' + str(i) + se[1]
                outfp = open(outfilename, 'w')
                outfp.write(infp.read())
                print "Extracted", f, "to", outfilename
                infp.close()
                outfp.close()

