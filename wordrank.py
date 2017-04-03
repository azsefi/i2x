from nltk.stem import WordNetLemmatizer
from nltk import pos_tag_sents, pos_tag
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from collections import defaultdict

class WordRank:
    
    def __init__(self, nwords = 10):
        self.nwords      = nwords
        self.wfreq       = None
        self.transfreq   = defaultdict(int)
        self.rankedwords = None
      
    def __gettext(self, pth):
        f = open(pth, 'r', encoding="utf8")
        txt = ''
        for line in f:
            txt += line

        f.close()
        
        return txt
    
    def getrank(self, pth, *args):
        '''
            Ranks most popular words in a text file based on occurance of
            these words in the transcript files.
            
            Parameters:
                @pth  : Path to the script.txt file
                @*args: Paths to the transcript files
        '''

        self.wfreq       = None
        self.transfreq   = defaultdict(int)
        self.rankedwords = None
        
        txt = self.__gettext(pth)
        lemmas = self.__getlemmas(txt)
        self.__getfrequency(lemmas, ftype='script')
        
        for pth in args:
            txt = self.__gettext(pth)
            lemmas = self.__getlemmas(txt)
            self.__getfrequency(lemmas, ftype = 'transscript')
        
        self.rankedwords = [(w, self.transfreq[w]) for w, _ in self.wfreq]
        self.rankedwords.sort(key = lambda x:x[1], reverse = True)
        
        return self.rankedwords
    
    def __getlemmas(self, txt):
        '''
            Filters noun, adjective and verb from input text, lemmatize them 
            and returns as list of words(tokens)
            
            Parameters:
                @txt  : The text file (str format) which must be lemmatized
        '''
        
        lemma = WordNetLemmatizer()
        punkts = PunktParameters()
        punkts.abbrev_types = set(['dr', 'vs', 'mr', 'mrs', 'prof', 'inc'])
        sent_tokenizer = PunktSentenceTokenizer(punkts)
        sentences = sent_tokenizer.tokenize(txt)

        lemma_tokens = []
        for sentence in sentences:
            stoken = word_tokenize(sentence)
            pos_sent = pos_tag(stoken)

            for p in pos_sent:
                if p[1].startswith('N'):
                    pos = wordnet.NOUN
                elif p[1].startswith('J'):
                    pos = wordnet.ADJ
                elif p[1].startswith('V'):
                    pos = wordnet.VERB
                else:
                    pos = None

                if pos:
                    lemma_tokens.append(lemma.lemmatize(p[0].lower(), pos))

        return lemma_tokens

    def __getfrequency(self, lemmas, ftype = 'script'):
        '''
            Counts occurance count of each word and up to 3 ngram in the list of tokens.
            In case of "script" file it populates self.wfreq variable, but in case of 
            "transscript" it populates self.transfreq variable
            
            Parameters :
                @lemmas: List of tokens
                @ftype : Must be one of ("script", "transscript")
        '''
        vectorize = CountVectorizer(ngram_range=(1,3), stop_words='english')
        count_vector = vectorize.fit_transform([' '.join(lemmas)]).toarray()
        words = vectorize.get_feature_names()

        if ftype == 'script':
            keyword_rank = np.argsort(count_vector)[0][::-1]   
            self.wfreq = [(words[keyword_rank[i]], count_vector[0][keyword_rank[i]]) for i in range(self.nwords)]
        
        elif ftype == 'transscript':
            wordcount = len(words)
            for i in range(wordcount):
                self.transfreq[words[i]] += count_vector[0][i]
