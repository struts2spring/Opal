from src.viewer.epub.epubtag import EpubBook




if __name__=='__main__':
    f='Coding for Beginners in Easy Steps - Basic Programming for All Ages (2015).epub'
    book = EpubBook()
    book.open(f)

    book.parse_contents()
    book.extract_cover_image(outdir='.')
    
    pass