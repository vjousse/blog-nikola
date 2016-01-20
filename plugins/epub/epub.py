# -*- coding: utf-8 -*-

# Copyright © 2012-2013 Roberto Alsina

# Permission is hereby granted, free of charge, to any
# person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the
# Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the
# Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice
# shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
# OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import tempfile
from nikola.plugin_categories import Task
from nikola.utils import LOGGER, config_changed
from ebooklib import epub

class Plugin(Task):

    name = "epub"

    def gen_tasks(self):
        """Build epub files from metadata and HTML fragments."""
        kw = {
            "post_pages": self.site.config["post_pages"],
            "translations": self.site.config["TRANSLATIONS"],
            "filters": self.site.config["FILTERS"],
            "show_untranslated_posts": self.site.config['SHOW_UNTRANSLATED_POSTS'],
            "demote_headers": self.site.config['DEMOTE_HEADERS'],
            "output_folder": self.site.config["OUTPUT_FOLDER"],
        }

        LOGGER.notice('BYE EPUB')

        # Never fail because a config key is missing.
        bye = self.site.config.get('BYE_WORLD', False)


        self.site.scan_posts()
        yield self.group_task()

        for lang in kw["translations"]:
            if kw["show_untranslated_posts"]:
                posts = self.site.posts
            else:
                posts = [x for x in self.site.posts if x.is_translation_available(lang)]

            ebook_file = self.make_epubs(posts, lang, kw)
            LOGGER.notice(lang + " - " + ebook_file.name)
            continue
            pass

            for post in self.site.timeline:
                if not kw["show_untranslated_posts"] and not post.is_translation_available(lang):
                    continue
                if post.is_post:
                    context = {'pagekind': ['post_page']}
                else:
                    context = {'pagekind': ['story_page']}

                LOGGER.notice(lang + " - " + post.title(lang=lang))
                LOGGER.notice(lang + " - " + post.text())
                for task in self.site.generic_page_renderer(lang, post, kw["filters"], context):
                    task['uptodate'] = task['uptodate'] + [config_changed(kw, 'nikola.plugins.task.pages')]
                    task['basename'] = self.name
                    task['task_dep'] = ['render_posts']
                    #yield task

    def make_epubs(self, posts, lang, kw):

        book = epub.EpubBook()

        # add metadata
        author=self.site.config['BLOG_AUTHOR'](lang)
        book.set_title(author)
        book.set_language(lang)

        book.add_author('Vincent Jousse')

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
        book.spine = ['nav'] + chapters

        output_path = os.path.join(kw["output_folder"],
                                    self.site.path("epub_dir", None, lang))
        tf = tempfile.NamedTemporaryFile()
        # create epub file
        epub.write_epub(os.path.join(output_path, 'test.epub'), book, {})

        return tf
