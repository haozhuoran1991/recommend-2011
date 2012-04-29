import sys
import nltk 
from urllib import urlopen
import urllib2
from urlparse import urlparse
from xgoogle.search import GoogleSearch, SearchError
import justext
        
class Start(object):
   
    num_of_sentences = 50
    num_results = 10
    search_list = ["nana" , "bbc", "wolf"]
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
            print "for \"%s\" " % search + "Found %d websites:" %  len(sites)
            for url in sites:
                print url
                page = urllib2.urlopen(url).read()
                paragraphs = justext.justext(page, justext.get_stoplist('English'))
                for paragraph in paragraphs:
                    if paragraph['class'] == 'good':
                        text = text + paragraph['text']
#                print text
                print "---------------------------------------------"
            sites = []
                
    except SearchError, e:
        print "Search failed: %s" % e
        
    words = nltk.word_tokenize(text)
    sent_tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
    sen = sent_tokenizer.tokenize(text)
    print len(sen)  
    
#    output_file = open('output.txt', 'w')
#    for word in text:
#        output_file.write(word + "\n")
