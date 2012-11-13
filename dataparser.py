#! /usr/bin/python
# -*- coding: utf-8 -*-
#PQ11536636 yapikredi

__author__ = "Osman Baskaya"

from bs4 import BeautifulSoup
from os import listdir
import re


wordlist_file = 'words.txt'
corpus = 'english.xml'
PATH = '/home/tyr/playground/base-occur/corpus/'


class DataParser(object):


    def __init__(self, filename, wordlist, ws=5):
        self.filename = filename
        self.wordlist = wordlist
        self.soup = None
        self.worddict = {}
        self.headwords = {}
        self.ws = ws


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
            f = open(PATH + word, 'w')
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
            g = open(PATH + word)
            h = open('input/'+word, 'w')
            count = 1
            for instance in g.readlines():
                hw = line[count]

                
                regex = r'(^\W*|\w+\W+){1,%d}%s(\W+\w+|\W*$){1,%d}' % \
                                                             (self.ws, hw, self.ws)

                newline = [hw] 
                context = re.search(regex, instance)
                newline.append(context.group().strip())
                newline.append('\n')
                h.write(' '.join(newline))
                if word == 'part.n':
                    if count == 59 or count == 60:
                        print instance
                        print context.group()
                        print newline
                        print ' '.join(newline)

                count += 1

    def remove_tw_input_file(self):

        files = listdir('input/')
        for filename in files:
            f = open('input/'+filename)
            g = open('input/processed'+filename+'.p', 'w')
            n = self.ws
            counter = 1
            for line in f.readlines():
                #line = line.split()
                neighbors = re.split('[ -]', line)
                if neighbors[0] == neighbors[n+1]:
                    try:
                        neighbors.pop(n+1)
                    except:
                        print filename, counter, line
                else:
                    for i, word in enumerate(line):
                        if neighbors[0] == word:
                            try:
                                neighbors.pop(i)
                            except:
                                print "2 =>", filename, counter, line

                counter += 1
                try:
                    neighbors.pop(0)
                except:
                    print "3 =>", filename, counter, line

                g.write(' '.join(neighbors))
            g.close()
            f.close()


def main():
    words = open(wordlist_file).readlines()
    words = [word.strip() for word in words]
    parser = DataParser(corpus, words, ws=5)
    #parser.cook_soup()
    #parser.seperate()
    #parser.get_headwords()
    #parser.create_input_file_with_tw()
    parser.remove_tw_input_file()
    

        
if __name__ == '__main__':
    main()

