#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from sklearn.feature_extraction.text import CountVectorizer
from os import listdir

PATH = '/home/tyr/playground/base-occur/'
INPUT_DIR = "%input/" % PATH

def get_vectors(filenames):
    vectorizer = CountVectorizer(min_df=0)
    f = open(INPUT_DIR + filenames)
    instances = f.readlines()
    return vectorizer.fit_transform(instances)

def make_experiment():
    km = KMeans(2, init='random', max_iter=10, n_init=1, verbose=1)

def main():
    words = open(PATH + 'words.txt').readlines()
    words = map(str.strip, words)
    




if __name__ == '__main__':
    main()


#R
#X = matrix(scan(s, 0), nrow=162, ncol=679, byrow=TRUE)
#np.savetxt('deneme2', X)

