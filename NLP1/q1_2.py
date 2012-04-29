import  nltk
from nltk.corpus import brown

def performance(cfd, wordlist):
    lt = dict((word, cfd[word].max()) for word in wordlist)
    baseline_tagger = nltk.UnigramTagger(model=lt, backoff=nltk.DefaultTagger('NN'))
    return baseline_tagger.evaluate(brown.tagged_sents(categories='news'))

def display():
    import pylab
    words_by_freq = list(nltk.FreqDist(brown.words(categories='news')))
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    sizes = 2 ** pylab.arange(15)
    perfs = [performance(cfd, words_by_freq[:size]) for size in sizes]
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()

def displayPlot1():
    import pylab
    sizes = 2 ** pylab.arange(15)
    perfs = []
    pylab.plot(sizes, perfs, '-bo')
    pylab.title('Lookup Tagger Performance with Varying Model Size')
    pylab.xlabel('Model Size')
    pylab.ylabel('Performance')
    pylab.show()
    
def countWordsWithNTags(n):
    d=nltk.FreqDist(brown.words(categories='news'))
    words_by_freq = list(d)
    c =brown.tagged_words(categories='news')
    cfd = nltk.ConditionalFreqDist(brown.tagged_words(categories='news'))
    print cfd
    
def main():
#    display()
#    displayPlot1(2);
    countWordsWithNTags(2);
    
if __name__ == '__main__':
    main() 