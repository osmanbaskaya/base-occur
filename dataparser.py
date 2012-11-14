#! /usr/bin/python
# -*- coding: utf-8 -*-
#PQ11536636 yapikredi

__author__ = "Osman Baskaya"

from bs4 import BeautifulSoup
from os import listdir
import re
import string

wordlist_file = 'words.txt'
corpus = 'english.xml'
PATH = '/home/tyr/playground/base-occur/corpus/'


class DataParser(object):

    def __init__(self, filename, wordlist, parser_type='low_nopunc', ws=5):
        self.filename = filename
        self.wordlist = wordlist
        self.soup = None
        self.worddict = {}
        self.headwords = {}
        self.ws = ws

        if parser_type == 'low_nopunc':
            self.inp_path = 'input/low_nopunc/'
            self.corpus_path = PATH + parser_type + '/'
            self.neigh_path = 'neighbors/low_nopunc/'


    def cook_soup(self):
        self.soup = BeautifulSoup(open(self.filename), 'xml')
        
    
    def get_headwords(self):
        f = open('words-headwords.txt', 'w')
        for key, elements in self.headwords.iteritems():
            f.write(key+' ')
            f.write(' '.join(elements))
            f.write('\n')
        f.close()
        

    def seperate(self):
        """ Seperate all words into some directory"""

        for word in self.wordlist:
            f = open(self.corpus_path, 'w')
            item = self.soup.find(item=word)
            self.worddict[word] = []
            self.headwords[word] = []
            count = 1
            while(True):
                instance = item.find(id=word+'.'+str(count))
                if instance is None:
                    break
                instance.contents[1] = instance.contents[1].contents[0]
                c = ''.join(instance.contents)
                c = c.strip()
                self.headwords[word].append(instance.head.get_text().strip())
                self.worddict[word].append(c)
                f.write(c)
                f.write('\n')
                count += 1
                
            f.close()

    def create_input_file_with_tw(self):
        
        f = open('words-headwords.txt')
        for line in f.readlines():
            line = line.split()
            word = line[0]
            g = open(self.corpus_path + word)
            h = open(self.inp_path + word, 'w')
            count = 1
            for instance in g.readlines():
                hw = line[count]

                table = string.maketrans("","")
                hw = hw.translate(table, string.punctuation).lower()
                
                regex = r'(^\W*|\w+\W+){1,%d}%s(\W+\w+|\W*$){1,%d}' % \
                                                             (self.ws, hw, self.ws)

                newline = [hw] 
                context = re.search(regex, instance)
                newline.append(context.group().strip())
                newline.append('\n')
                h.write(' '.join(newline))
                count += 1

    def remove_tw_input_file(self):

        files = self.wordlist
        for filename in files:
            f = open(self.inp_path + filename)
            g = open(self.neigh_path+filename+'.neigh', 'w')
            n = self.ws
            for line in f.readlines():
                #line = line.split()
                neighbors = re.split('[ -]', line)
                if neighbors[0] == neighbors[n+1]:
                    neighbors.pop(n+1)
                    #print filename, counter, line
                else:
                    for i, word in enumerate(line):
                        if neighbors[0] == word:
                            neighbors.pop(i)
                neighbors.pop(0)

                g.write(' '.join(neighbors))
            g.close()
            f.close()
    
def translator(words, source_path = PATH + 'original/', dest_path = PATH + 'low_nopunc/'):
    
    for word in words:
        text = open(source_path + word).readlines()
        text = ''.join(text)
        table = string.maketrans("","")
        c = text.translate(table, string.punctuation).lower()
        f = open(dest_path + word, 'w')
        f.write(c)
        f.close()

def create_key_file(fname='/home/tyr/Desktop/datasets/key/keys/senseinduction.key'):
    with open(fname) as f:
        d = {}
        for line in f.readlines():
            line = line.strip()
            line = line.split()
            word = line[0]
            
            inst_no = int(line[1].split('.')[-1])
            clust_no = int(line[2].split('.')[-1])
            if d.has_key(word):
                d[word].append((inst_no, clust_no,))

            else:
                d[word] = [(inst_no, clust_no,)]


    for key in d.keys():
        f = open('keys/'+key, 'w')
        r = d[key]
        r.sort()
        for t in r:
            f.write(' '.join(map(str, t)))
            f.write('\n')
        f.close()


def create_cluster_dist():
    words = open('words.txt').readlines()
    f = open('sense.distribution', 'w')
    for fname in words:
        fname = fname.strip()
        lines = open('keys/' + fname).readlines()
        labels = set()
        for line in lines:
            ins, label = line.split()
            labels.add(label)

        f.write(fname + ' ')
        f.write(str(len(labels)))
        f.write('\n')


    f.close()





    
    



def main():
    words = open(wordlist_file).readlines()
    words = [word.strip() for word in words]
    #parser = DataParser(corpus, words, ws=5)
    #parser.cook_soup()
    #parser.seperate()
    #parser.get_headwords()
    #parser.create_input_file_with_tw()
    #parser.remove_tw_input_file()
    #translator(words)
    #create_key_file()
    create_cluster_dist()

        
if __name__ == '__main__':
    main()

