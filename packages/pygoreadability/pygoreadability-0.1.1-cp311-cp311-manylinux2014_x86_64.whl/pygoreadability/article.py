from pygoreadability.ext import pygoreadability

def from_url(page_url, tiemout=0):
    return Article(pygoreadability.FromURL(page_url, tiemout))

def from_string(string):
    return Article(pygoreadability.Parse(string))


class Article:
    def __init__(self, article):
        self.article = article
        
    @property
    def title(self):
        return pygoreadability.GetTitle(self.article)
    
    @property
    def html(self):
        return pygoreadability.GetContent(self.article)
    
    @property
    def text(self):
        return pygoreadability.GetTextContent(self.article)
