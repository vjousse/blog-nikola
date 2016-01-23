# -*- coding: utf-8 -*-

# Copyright © 2012-2016 Roberto Alsina and others.

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

"""Build HTML fragments from metadata and text."""

from copy import copy
import os
import re

from nikola.plugin_categories import Task
from nikola import filters, utils
from nikola.utils import LOGGER, config_changed
from ebooklib import epub


def update_deps(post, lang, task):
    """Update file dependencies as they might have been updated during compilation.

    This is done for example by the ReST page compiler, which writes its
    dependencies into a .dep file. This file is read and incorporated when calling
    post.fragment_deps(), and only available /after/ compiling the fragment.
    """
    task.file_dep.update([p for p in post.fragment_deps(lang) if not p.startswith("####MAGIC####")])


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


class RenderPostsEpub(Task):
    """Build epub from metadata and text."""

    name = "render_posts_epub"

    def gen_tasks(self):
        """Build HTML fragments from metadata and text."""
        self.site.scan_posts()
        kw = {
            "translations": self.site.config["TRANSLATIONS"],
            "timeline": self.site.timeline,
            "default_lang": self.site.config["DEFAULT_LANG"],
            "show_untranslated_posts": self.site.config['SHOW_UNTRANSLATED_POSTS'],
            "demote_headers": self.site.config['DEMOTE_HEADERS'],
            "output_folder": self.site.config["OUTPUT_FOLDER"],
        }
        self.tl_changed = False

        yield self.group_task()

        def tl_ch():
            self.tl_changed = True

        yield {
            'basename': self.name,
            'name': 'timeline_changes',
            'actions': [tl_ch],
            'uptodate': [utils.config_changed({1: kw['timeline']})],
        }

        for lang in kw["translations"]:
            deps_dict = copy(kw)
            deps_dict.pop('timeline')
            for post in kw['timeline']:
                if not post.is_translation_available(lang) and not self.site.config['SHOW_UNTRANSLATED_POSTS']:
                    continue
                # Extra config dependencies picked from config
                for p in post.fragment_deps(lang):
                    if p.startswith('####MAGIC####CONFIG:'):
                        k = p.split('####MAGIC####CONFIG:', 1)[-1]
                        deps_dict[k] = self.site.config.get(k)
                dest = post.translated_base_path(lang)
                dest = re.sub('html$', 'epub', dest)

                LOGGER.notice('Dest {}'.format(dest))

                file_dep = [p for p in post.fragment_deps(lang) if not p.startswith("####MAGIC####")]
                task = {
                    'basename': self.name,
                    'name': dest,
                    'file_dep': file_dep,
                    'targets': [dest],
                    'actions': [(make_epubs, ([post], lang, dest, self.site.config['BLOG_AUTHOR'](lang), )),
                                (update_deps, (post, lang, )),
                                ],
                    'clean': True,
                    'uptodate': [
                        utils.config_changed(deps_dict, 'nikola.plugins.task.posts_epub'),
                        lambda p=post, l=lang: self.dependence_on_timeline(p, l)
                    ] + post.fragment_deps_uptodate(lang),
                    'task_dep': ['render_posts_epub:timeline_changes']
                }

                # Apply filters specified in the metadata
                ff = [x.strip() for x in post.meta('filters', lang).split(',')]
                flist = []
                for i, f in enumerate(ff):
                    if not f:
                        continue
                    if f.startswith('filters.'):  # A function from the filters module
                        f = f[8:]
                        try:
                            flist.append(getattr(filters, f))
                        except AttributeError:
                            pass
                    else:
                        flist.append(f)
                yield utils.apply_filters(task, {os.path.splitext(dest)[-1]: flist})

    def dependence_on_timeline(self, post, lang):
        """Check if a post depends on the timeline."""
        if "####MAGIC####TIMELINE" not in post.fragment_deps(lang):
            return True  # No dependency on timeline
        elif self.tl_changed:
            return False  # Timeline changed
        return True


