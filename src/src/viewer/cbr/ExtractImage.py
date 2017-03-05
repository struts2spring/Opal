import rarfile
import traceback
import os
import zipfile
import tarfile
import shutil

filename = '1.cbr'

class Extractor():
    """Extractor is a threaded class for extracting different archive formats.

    The Extractor can be loaded with paths to archives (currently ZIP, tar,
    or RAR archives) and a path to a destination directory. Once an archive
    has been set it is possible to filter out the files to be extracted and
    set the order in which they should be extracted. The extraction can
    then be started in a new thread in which files are extracted one by one,
    and a signal is sent on a condition after each extraction, so that it is
    possible for other threads to wait on specific files to be ready.

    Note: Support for gzip/bzip2 compressed tar archives is limited, see
    set_files() for more info.
    """
    def __init__(self, filePath=None):
        self.filePath = filePath
        self.fileType=None
        if os.path.exists("/tmp/1"):
            shutil.rmtree("/tmp/1")
        self.archiveMimeType()
        
    def extractCbrImage(self):
        print rarfile.is_rarfile(self.filePath)
        rar = rarfile.RarFile(self.filePath)
        print rar.namelist()
        infoList = rar.infolist()
        for info in infoList:
            print info
        # print rar.printdir()
        if not os.path.exists("/tmp/1"):
            os.mkdir("/tmp/1")

        try:
            rar.extractall("/tmp/1")
        except:
            traceback.print_exc()
    
    def extractFirstPageCbrImage(self):
        print rarfile.is_rarfile(self.filePath)
        rar = rarfile.RarFile(self.filePath)
        nameList= rar.namelist()
        infoList = rar.infolist()
        nameList.sort()
        firstPage=None
        for name in nameList:
            firstPage= name
            break
        # print rar.printdir()
        if not os.path.exists("/tmp/1"):
            os.mkdir("/tmp/1")
        try:
            rar.extractall("/tmp/1")
        except:
            traceback.print_exc()   
        return firstPage   
    def archiveMimeType(self):
        """Return the archive type of <path> or None for non-archives."""
        
        try:
            if os.path.isfile(self.filePath ):
                if not os.access(self.filePath , os.R_OK):
                    return None
                if zipfile.is_zipfile(self.filePath ):
                    self.fileType='zip'
                fd = open(self.filePath, 'rb')
                magic = fd.read(4)
                fd.seek(60)
                magic2 = fd.read(8)
                fd.close()
                if tarfile.is_tarfile(self.filePath) and os.path.getsize(self.filePath) > 0:
                    if magic.startswith('BZh'):
                        self.fileType='bzip2' 
                    if magic.startswith('\037\213'):
                        self.fileType='gzip' 
                    self.fileType='tar'
                if magic == 'Rar!':
                    self.fileType='rar'
                if magic == '7z\xbc\xaf':
                    self.fileType='7zip'
                if magic2 == 'BOOKMOBI':
                    self.fileType='mobi'
        except Exception:
            print '! Error while reading', self.filePath
        return None   
    def getFileNameList(self):
        """Return a list of names of all the files the extractor is currently
        set for extracting. After a call to setup() this is by default all
        files found in the archive. The paths in the list are relative to
        the archive root and are not absolute for the files once extracted.
        """
        return self._files[:]
if __name__ == '__main__':
    extractor=Extractor(filePath='/docs/github/Opal/src/viewer/cbr/1.cbr')
    extractor.extractFirstPageCbrImage()
    pass
