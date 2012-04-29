import sys
import nltk 
from urllib import urlopen
import urllib2
from urlparse import urlparse
from xgoogle.search import GoogleSearch, SearchError
import justext
from nltk.corpus import brown
      
def main():
#    s = Start()
#    text = s.getTextFromWeb()
#    clean_file = open('cleanText.txt', 'w')
#    clean_file.write(text)
#    clean_file.close()
#    s.createCorpusFile(s.tagText(text))
    x =  brown.tagged_sents(categories='news')
    print x 
    
if __name__ == '__main__':
    main() 
        
class Start(object):
    brown_news_tagged = brown.tagged_sents(categories='news')
    brown_train = brown_news_tagged[100:]
    brown_test = brown_news_tagged[:100]
    nn_tagger = nltk.DefaultTagger('NN')
    regexp_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
                                       (r'(The|the|A|a|An|an)$', 'AT'),   # articles
                                       (r'.*able$', 'JJ'),                # adjectives
                                       (r'.*ness$', 'NN'),                # nouns formed from adjectives
                                       (r'.*ly$', 'RB'),                  # adverbs
                                       (r'.*s$', 'NNS'),                  # plural nouns
                                       (r'.*ing$', 'VBG'),                # gerunds
                                       (r'.*ed$', 'VBD'),                 # past tense verbs
                                       (r'.*', 'NN')                      # nouns (default)
                                       ],backoff=nn_tagger)
    
    affix_tagger = nltk.AffixTagger(brown_train, backoff=regexp_tagger)
    ut3 = nltk.UnigramTagger(brown_train, backoff=affix_tagger)
    ct2 = nltk.NgramTagger(2, brown_train, backoff=ut3)
    
    def getTextFromWeb(self):
        num_results = 10
        search_list = ["nana" ]
        sites = [] 
        text = ""
        try:
            while len(search_list)!=0 :
                search = search_list.pop()
                gs = GoogleSearch(search)
                gs.results_per_page = 10
                results = gs.get_results()
                domains = [r.url.encode('utf8') for r in results]
                for d in domains:
                    sites.append(d)
                    if len(sites) == num_results:
                        break
    #            print "for \"%s\" " % search + "Found %d websites:" %  len(sites)
                for url in sites:
                    print url
                    page = urllib2.urlopen(url).read()
                    paragraphs = justext.justext(page, justext.get_stoplist('English'))
                    for paragraph in paragraphs:
                        if paragraph['class'] == 'good':
                            text = text + paragraph['text'].encode('utf8')
    #                print text   
    #            print "---------------------------------------------"
                sites = []
                    
        except SearchError, e:
            print "Search failed: %s" % e 
        return text

    def tagText(self,text):      
        return self.ct2.tag(text.split())
    
    def createCorpusFile(self,tag_text):      
        tag_file = open('tagText.txt', 'w')
        for w,t in tag_text:
            tag_file.write(w+"/"+t+" " )
        tag_file.close()

       

