from ebooklib import epub

def make_epubs(posts, lang, dest, author, basename=None):

    book = epub.EpubBook()

    # add metadata
    book.set_title(author)
    book.set_language(lang)

    book.add_author(author)

    chapters = []

    for post in posts:
        c1 = epub.EpubHtml(title=post.title(lang=lang), file_name='%s.xhtml' % post.meta[lang]['slug'])
        c1.content=u'<html><head></head><body><h1>%s</h1>%s</body></html>' % (post.title(lang=lang), post.text(lang=lang, show_read_more_link=False))
        book.add_item(c1)
        chapters.append(c1)


    book.toc = tuple(chapters)

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())


    # define css style
    style = '''
@namespace epub "http://www.idpf.org/2007/ops";

body {
font-family: Cambria, Liberation Serif, Bitstream Vera Serif, Georgia, Times, Times New Roman, serif;
}

h2 {
text-align: left;
text-transform: uppercase;
font-weight: 200;     
}

ol {
    list-style-type: none;
}

ol > li:first-child {
    margin-top: 0.3em;
}


nav[epub|type~='toc'] > ol > li > ol  {
list-style-type:square;
}


nav[epub|type~='toc'] > ol > li > ol > li {
    margin-top: 0.3em;
}

'''

    # add css file
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)

    # create spine
    if(len(posts) > 1):
        book.spine = ['nav'] + chapters
    else:
        book.spine = chapters

    #output_path = os.path.join(output_folder,
    #                            self.site.path("epub_dir", None, lang))
    # create epub file
    epub.write_epub(dest, book, {})

    return dest

