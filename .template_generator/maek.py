#!/usr/bin/python3

# maek.py by William Welna is marked CC0 1.0. To view a copy of this mark, visit https://creativecommons.org/publicdomain/zero/1.0/ 

import configparser
from markdown2 import Markdown

markdown = Markdown()

class Page:
    def __init__(self, config, afile):
        self.page_main = ""
        self.page_header = ""
        self.config = config
        self.afile = afile
        with open('template/page_main.html', 'r') as page: self.page_main = page.read()
        with open('template/page_header.html', 'r') as header: self.page_header = header.read()
        self.__config_replace()

    def render(self):
        self.__maek(self.afile)
        self.__writetofile(self.afile)

    def __config_replace(self):
        self.page_main = self.page_main.replace('%WEBSITE_TITLE%', self.config.get('DEFAULT', 'WEBSITE_TITLE'))
        self.page_main = self.page_main.replace('%AUTHOR%', self.config.get('DEFAULT', 'AUTHOR'))
        self.page_main = self.page_main.replace('%KEYWORDS%', self.config.get('DEFAULT', 'KEYWORDS'))
        self.page_main = self.page_main.replace('%DESCRIPTION%', self.config.get('DEFAULT', 'DESCRIPTION'))
        self.page_main = self.page_main.replace('%ANGRY_FACE%', self.config.get('DEFAULT', 'ANGRY_FACE'))

    def __maek(self, afile):
        md = ""
        with open(f"pages/{afile}", 'r') as i: md = i.read()
        self.page_main = self.page_main.replace('%BODY_CONTENT%', markdown.convert(md))

    def __writetofile(self, afile):
        with open(f"../{afile[:-3]}.html", 'w') as o: o.write(self.page_main)

def dopage(config, afile):
    p = Page(config, afile)
    p.render()

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read(['template_variables.ini'])

    dopage(config, 'index.md')
    dopage(config, 'blog.md')
    dopage(config, 'snippets.md')
    dopage(config, 'resources.md')
    dopage(config, 'about.md')