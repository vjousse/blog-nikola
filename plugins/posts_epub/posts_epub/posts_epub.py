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

from collections import defaultdict
from copy import copy
import os
import re

from nikola.plugin_categories import Task
from nikola import filters, utils
from nikola.utils import LOGGER, config_changed, get_translation_candidate
from . import epub_utils

def update_deps(post, lang, task):
    """Update file dependencies as they might have been updated during compilation.

    This is done for example by the ReST page compiler, which writes its
    dependencies into a .dep file. This file is read and incorporated when calling
    post.fragment_deps(), and only available /after/ compiling the fragment.
    """
    task.file_dep.update([p for p in post.fragment_deps(lang) if not p.startswith("####MAGIC####")])


class RenderPostsEpub(Task):
    """Build epub from metadata and text."""

    name = "render_posts_epub"

    def set_site(self, site):
        site.register_path_handler("post_epub", self.epub_path)
        site.register_path_handler("posts_epub", self.posts_epub_path)
        return super(RenderPostsEpub, self).set_site(site)


    def _get_filtered_posts(self, lang, show_untranslated_posts):
        """Return a filtered list of all posts for the given language.

        If show_untranslated_posts is True, will only include posts which
        are translated to the given language. Otherwise, returns all posts.
        """
        if show_untranslated_posts:
            return self.site.posts
        else:
            return [x for x in self.site.posts if x.is_translation_available(lang)]

    def posts_epub_path(self, section_name, lang):
        return [_f for _f in [
            self.site.config['TRANSLATIONS'][lang],
            section_name + ".epub"] if _f]


    def epub_path(self, post, lang):
        path = [_f for _f in [
            self.site.config['TRANSLATIONS'][lang],
            post.post_name + ".epub"] if _f]


        return path

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

        groups = defaultdict(set)

        for lang in kw["translations"]:
            deps_dict = copy(kw)
            deps_dict.pop('timeline')

            for post in kw['timeline']:
                if not post.is_translation_available(lang) and not self.site.config['SHOW_UNTRANSLATED_POSTS']:
                    continue
                # Extra config dependencies picked from config
                groups[(lang, post.section_slug(lang))].add(post)

                for p in post.fragment_deps(lang):
                    if p.startswith('####MAGIC####CONFIG:'):
                        k = p.split('####MAGIC####CONFIG:', 1)[-1]
                        deps_dict[k] = self.site.config.get(k)

                dest = post.translated_base_path(lang)
                #LOGGER.notice('Dest 1 {}'.format(dest))
                #LOGGER.notice('Dest 2 {}'.format(post.translated_source_path(lang)))
                dest = re.sub('html$', 'epub', dest)

                if lang  is not kw['default_lang']:
                    dest = re.sub('^cache', os.path.join(kw['output_folder'], lang), dest)
                else:
                    dest = re.sub('^cache', kw['output_folder'], dest)


                #LOGGER.notice('Dest 3 "{}" "{}"'.format(dest, lang))

                file_dep = [p for p in post.fragment_deps(lang) if not p.startswith("####MAGIC####")]
                task = {
                    'basename': self.name,
                    'name': dest,
                    'file_dep': file_dep,
                    'targets': [dest],
                    'actions': [(epub_utils.make_epubs, ([post], lang, dest, self.site.config['BLOG_AUTHOR'](lang), )),
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

        for section_slug, post_list in groups.items():
            lang, slug = section_slug
            epub_name = "{}.epub".format(slug)
            post_list = sorted(post_list, key=lambda p: p.date, reverse=True)

            if epub_name == ".epub":
                continue

            dest = os.path.join(kw['output_folder'], 
                                self.site.config['TRANSLATIONS'][lang], 
                                epub_name)

            file_dep = [p for p in post.fragment_deps(lang) if not p.startswith("####MAGIC####")]
            task = {
                'basename': self.name,
                'name': dest,
                'targets': [dest],
                'actions': [(epub_utils.make_epubs, (post_list, lang, dest, self.site.config['BLOG_AUTHOR'](lang), )),
                            ],
                'clean': True,
                'uptodate': [
                    utils.config_changed(deps_dict, 'nikola.plugins.task.posts_epub'),
                    lambda p=post, l=lang: self.dependence_on_timeline(p, l)
                ] + post.fragment_deps_uptodate(lang),
                'task_dep': ['render_posts_epub:timeline_changes']
            }

            yield task

    def dependence_on_timeline(self, post, lang):
        """Check if a post depends on the timeline."""
        if "####MAGIC####TIMELINE" not in post.fragment_deps(lang):
            return True  # No dependency on timeline
        elif self.tl_changed:
            return False  # Timeline changed
        return True


