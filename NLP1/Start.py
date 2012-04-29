import sys
import nltk 
from urllib import urlopen
import urllib2
from urlparse import urlparse
from xgoogle.search import GoogleSearch, SearchError
import justext
        
class Start(object):
   
    dst_keyword = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    num_results = 10
    final_results = [] 
    try:
        gs = GoogleSearch(dst_keyword)
        gs.results_per_page = 10
        print gs.num_results
#        while len(final_results) < num_results:
        results = gs.get_results()
        
        domains = [r.url.encode("utf8") for r in results]
        for d in domains:
            final_results.append(d)
            if len(final_results) == num_results:
                break
    except SearchError, e:
        print "Search failed: %s" % e  
            
    print "Found %d websites:" % len(final_results)
    for url in final_results:
        print "%s" % url
        page = urllib2.urlopen(url).read()
        raw = nltk.clean_html(page)
        tokens = nltk.word_tokenize(raw)

        paragraphs = justext.justext(page, justext.get_stoplist('English'))
        for paragraph in paragraphs:
            if paragraph['class'] == 'good':
                print paragraph['text']
        print "---------------------------------------------"