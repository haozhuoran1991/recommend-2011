'''
- Articles
- Each article links to other articles (outgoing links)
- Categories (in hebrew, these are called "�������")
- Redirect (in hebrew, "�����")
- Disambiguation links (in hebrew, "���������")
- A template of the article (in hebrew, "�����")
'''

class Article(object):

    def __init__(self):
        self.links = []
        self.Categories = []
        self.Redirect = []
        self.Disambiguation_links  = []
        self.template = []
