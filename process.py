#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from scipy.linalg import svd
from sklearn import metrics
import logging
from optparse import OptionParser
import sys
from time import time

wordlist_file = 'words.txt'
PATH = '/home/tyr/playground/base-occur/'
INPUT_DIR = "%s/neighbors/original/" % PATH

def get_vector_from_neigh(filenames):

    vectorizer = CountVectorizer(min_df=0)
    f = open(INPUT_DIR + filenames + ".neigh") #neighbor words
    instances = f.readlines()
    return vectorizer.fit_transform(instances)

def get_vector_from_vec(word, vec_type='original'):
    return np.loadtxt('vectors/%s/' % vec_type + word + '.vec', delimiter=',')

def write_vectors(words):
    for word in words:
        X = get_vector_from_neigh(word)
        np.savetxt('vectors/original/'+word+'.vec', X.todense(), delimiter=',')

def write_vectors_aft_svd(words, factors=40):
    for word in words:
        print word
        X = get_vector_from_vec(word)
        U, S, V = svd(X) 
        np.savetxt('vectors/svd%s/'%str(factors)+word+'.vec', U[:,:factors], delimiter=',')
        exit()
        
def get_labels(word):
    lines = open('keys/' + word).readlines()
    labels = []
    for line in lines:
        line = line.split()
        labels.append(int(line[1])-1)
    return labels

def get_k_values(fname='gapstat.k', fieldno=1):
    lines = open(fname).readlines()
    return [int(k.split()[fieldno]) for k in lines]
    

def calculate_MAE(list1, list2):
    
    total_error = 0
    m = len(list1)
    for i in xrange(m):
        total_error += abs(float(list1[i])- float(list2[i]))
    return total_error / m


def calculate_error(func, list1, list2):
    
    return func(list1, list2)


def discriminate(factorization=False, nfactor=40):
    
    
    
    #real_k = get_k_values(fname='words.k')
    predicted_k = get_k_values()
    #predicted_k = real_k
    #print "MAE between gapstats and real: " + str(calculate_error(calculate_MAE, predicted_k, real_k))

    
    words = open(wordlist_file).readlines()
    f = open('results/SVD%d'%nfactor, 'w')
    #f = open('results/total_results_gold_k', 'w')
    f.write("word, homogeneity_score, completeness_score, v_measure, randIndex, num_of_inst, num_of_feature\n")
    words = [word.strip() for word in words]
    total = [0, 0, 0, 0]
    nwords = len(words)



    for i, word in enumerate(words):

        f.write('%14s' % word)

        #print "Test on " + word
        X = get_vector_from_vec(word)
        
        if factorization:
            U, sigma, V = svd(X)
            Sigma = np.zeros_like(X)

            n = min(X.shape)
            Sigma[:n,:n] = np.diag(sigma)
            #print np.dot(U,np.dot(Sigma,V))
            X1 = np.dot(U[:, :nfactor], np.dot(Sigma[:nfactor,:], V[:, :]))
            m, n = X1.shape
            error = sum(sum(np.abs(X - X1))) / (m*n)
            #print "error is %0.4f" % error
            X = U[:, :nfactor]

        m, n = X.shape

        labels = get_labels(word)
        km = KMeans(predicted_k[i], init='random', max_iter=100, n_init=1, verbose=0)
        #print "Clustering sparse data with %s" % km
        #t0 = time()
        km.fit(X)
        #print "done in %0.3fs" % (time() - t0)
        #print



        homogeneity = metrics.homogeneity_score(labels, km.labels_)
        completeness = metrics.completeness_score(labels, km.labels_) 
        vmeasure = metrics.v_measure_score(labels, km.labels_)
        randIndex = metrics.adjusted_rand_score(labels, km.labels_)


        f.write('%10.5f' % homogeneity)
        f.write('%10.5f' % completeness)
        f.write('%10.5f' % vmeasure)
        f.write('%10.5f' % randIndex)
        f.write('%6d' % m)
        f.write('%6d' % n)
        f.write('%3d' % len(set(labels)))
        f.write('%3d' % len(set(km.labels_)))
        f.write("%6.4f" % error)
        f.write('\n')


        total[0] += homogeneity / nwords
        total[1] += completeness / nwords
        total[2] += vmeasure / nwords
        total[3] += randIndex / nwords


        #print "Homogeneity: %0.4f" % homogeneity
        #print "Completeness: %0.4f" % completeness
        #print "V-measure: %0.4f" % vmeasure
        #print "Adjusted Rand-Index: %.4f" % randIndex

    print total


words = open(PATH + 'words.txt').readlines()
words = map(str.strip, words)

def main():

    #words = open(wordlist_file).readlines()
    #words = [word.strip() for word in words]
    #write_vectors_aft_svd(words)
    discriminate(factorization=True, nfactor=40)
    #discriminate(factorization=False, nfactor=60)


if __name__ == '__main__':
    main()


#R
#X = matrix(scan(s, 0), nrow=162, ncol=679, byrow=TRUE)
#np.savetxt('deneme2', X)

