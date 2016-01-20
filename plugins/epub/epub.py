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

from nikola.plugin_categories import Task
from nikola.utils import LOGGER, config_changed


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
        }

        LOGGER.notice('BYE EPUB')

        # Never fail because a config key is missing.
        bye = self.site.config.get('BYE_WORLD', False)


        self.site.scan_posts()
        yield self.group_task()

        for lang in kw["translations"]:
            for post in self.site.timeline:
                if not kw["show_untranslated_posts"] and not post.is_translation_available(lang):
                    continue
                if post.is_post:
                    context = {'pagekind': ['post_page']}
                else:
                    context = {'pagekind': ['story_page']}
                for task in self.site.generic_page_renderer(lang, post, kw["filters"], context):
                    task['uptodate'] = task['uptodate'] + [config_changed(kw, 'nikola.plugins.task.pages')]
                    task['basename'] = self.name
                    task['task_dep'] = ['render_posts']
                    yield task
