import lxml.html as lhtml

class HtmlCleaner:
    def _deleteElementsWithoutText(self, html):
        elements = list(filter(lambda x: x.getparent() != None,
                               html.xpath("//*[not(normalize-space()) and not(self::a or self::br)]")))

        for e in elements:
            e.getparent().remove(e)

        return html
        
    def _applyCleaner(self, html): 
        from lxml.html.clean import Cleaner
        
        cleaner = Cleaner(
            scripts=True,
            javascript=True,
            comments=True,
            style=True,
            inline_style=None,
            links=False,
            meta=False,
            page_structure=True,
            processing_instructions=True,
            embedded=True,
            frames=True,
            forms=True,
            annoying_tags=True,
            remove_tags=None,
            allow_tags={'a', 'p', 'h1', 'h2', 'h3', 'br'},
            kill_tags=None,
            remove_unknown_tags=False,
            safe_attrs_only=True,
            safe_attrs={"href"},
            add_nofollow=False)
        
        return cleaner.clean_html(html)
                   
    def clean(self, html):
        html = self._deleteElementsWithoutText(html)
        html = self._applyCleaner(html)
        return html

class ParserTemplates(object):
    __loaded = False
    _templates = None
    
    def __loadTemplates(self):
        if self.__loaded == False:
            import json
            
            with open("templates.txt", "r") as read_file:
                self._templates = json.load(read_file)
            self.__loaded = True
        
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super(ParserTemplates, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.__loadTemplates()

    def getTemplateByUrlOrDefault(self, url):
        from urllib.parse import urlparse
        path = urlparse(url)[1]
        if path in self._templates:
            return self._templates[path]
        else:
            return self._templates['default']
        
class MainInformationParser:
    def _getElementTreeRoot(self, url):    
        import lxml.html.soupparser as soupparser
        import urllib.request
        
        _url = urllib.request.urlopen(url)
        tree = soupparser.parse(_url)
        return tree.getroot()

    def getHtml(self, url):
        template = ParserTemplates().getTemplateByUrlOrDefault(url)
        elements = self._getElementTreeRoot(url).xpath(template)

        root = lhtml.Element("root")
        [root.append(item) for item in elements]
        return root

class TextDecorator:
    def _getXsl(self):
        from lxml import etree
        with open("decorator.txt", "r") as file:
            xsl = file.read()
        xsl = etree.XML(xsl)    
        return etree.XSLT(xsl)

    def _removeBlankText(self, string):
        import re
        regex = re.compile(rb'\n{2,}')
        return regex.sub(rb'\n', string).strip(rb'\n');
        
    def getDecoratedTextFromHtml(self, html):
        root = HtmlCleaner().clean(html)
        xsl = self._getXsl()
        root = xsl(root)
        return self._removeBlankText(
            lhtml.tostring(root, method='text', encoding='utf-8'))    
        
class MainInformation:
    _url = None
    
    def __init__(self, url):
        self._url = url
        
    def getText(self):
        html = MainInformationParser().getHtml(self._url)
        return TextDecorator().getDecoratedTextFromHtml(html)

    def getFolder(self):
        from urllib.parse import urlparse
        import os

        data = urlparse(self._url)
        path = data[1] + data[2]
        for char in ['\\', '*' '?', ':', '"', '<', '>', '|']:
            path = path.replace(char, '')
        #path = path[1:]
        path = 'tests\\' + path
        os.makedirs(path, exist_ok = True)
        return path
                   
    def saveToFile(self):
        file = open(self.getFolder() + '\\index.txt', mode = 'wb')
        file.write(self.getText())
        file.close()
    
