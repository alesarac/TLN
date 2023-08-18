from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import os
os.chdir('../es1_Defs')
from defs import parse_input
os.chdir('../es2_Content2Form')

from nltk.corpus import wordnet as wn
import csv


FILE = "./resources/definizioni.csv"
N_GENUS_WORDS = 6
N_DEFS = 32
N_SYNSETS = 5 #primi N_SYNSETS da restituire

#lista di tutte le gloss di WordNet formata da : [[synset, gloss], ...]
WN_SYNSET_DEFINITIONS = [(synset,synset.definition()) for synset in wn.all_synsets()]

"""
Metodo che misura la similarità
tra due frasi date in input tramite la cosine similarity
"""
def similarity(sent_1, sent_2):

    # tokenization
    X_list = word_tokenize(sent_1.lower())
    Y_list = word_tokenize(sent_2.lower())

    if X_list == Y_list:
        return 1
    # sw contains the list of stopwords
    sw = stopwords.words('english')
    l1 =[];l2 =[]

    # remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}

    if (not X_set) or (not Y_set):
        return 0
    # form a set containing keywords of both strings
    rvector = X_set.union(Y_set)
    for w in rvector:
    	if w in X_set: l1.append(1) # create a vector
    	else: l1.append(0)
    	if w in Y_set: l2.append(1)
    	else: l2.append(0)
    c = 0

    # cosine formula
    for i in range(len(rvector)):
            c+= l1[i]*l2[i]
    cosine = c / float((sum(l1)*sum(l2))**0.5)

    return cosine


"""
restituisce il synset data la glossa in input
"""
def find_synset_by_gloss(gloss):
    for elem in WN_SYNSET_DEFINITIONS:
        if(gloss==elem[1]):
            return elem[0]

"""
costruisce un dizionario con
    chiave = concetto
    e
    valore = lista delle definizioni del concetto
"""
def defs_dict():
    definizioni_dict = {}
    n_term=4
    with open(FILE, "r", encoding='utf-8') as file:
        csv_reader=csv.reader(file,delimiter=";")
        next(csv_reader) #per skippare la prima riga dell'header

        for row in csv_reader:
            if n_term > 0:
                concetto=row[0]
                definizioni=row[1:]
                definizioni_dict[concetto]=[elem for elem in definizioni if elem !='']
                n_term-=1
    return definizioni_dict

"""
calocla la similarità tra le definizioni e le gloss di WN
ritorna una lista con le prime N_SYNSETS migliori definizioni
"""
def best_def_similariry(list_sent):
    sent_sim=[]

    for sent in list_sent:
        print(f"sono slla frase : {list_sent.index(sent)}")
        max_score=0
        for elem in WN_SYNSET_DEFINITIONS:
            sim = similarity(sent,elem[1])
            if(sim > max_score):
                max_score=sim
                gloss_ref=elem[1]

        sent_sim.append((sent,gloss_ref,max_score,find_synset_by_gloss(gloss_ref)))
        #sent_sim è la lista che contiene il primo miglior risultato :
            # sent : la definizione annotata
            # gloss_ref : la glossa di riferimento
            # max_score : lo score ottenuto dalla similarità della sent e gloss_ref
            # find_synset_by_gloss(gloss_ref) : il synset relativo alla gloss_ref

    return sorted(sent_sim,key=lambda t: t[2],reverse=True)[:1]

def onomasiological_by_word_freq():

    freq_words_dict = parse_input()

    genus_dict ={}
    for key in freq_words_dict:
        genus_dict[key] = [(elem[0],round(elem[1]/N_DEFS,2)) for elem in freq_words_dict[key][:N_GENUS_WORDS]]

    result={}
    for key in genus_dict:
        syns_gloss=[]
        for synset in WN_SYNSET_DEFINITIONS:
            score = 0
            for genus in genus_dict[key]:
                if genus[0] in synset[1]:
                    score+=genus[1]
            if score != 0:
                syns_gloss.append((synset[1],synset[0],(score/N_GENUS_WORDS)))

        result[key]=sorted(syns_gloss,key=lambda t: t[2],reverse=True)[:N_SYNSETS]

    return result

def onomasiological_by_sentences_sim():
    # definizioni_dict = defs_dict()
    result={}
    for key in definizioni_dict:
        print(f"\nsono al concetto: {key}")
        result[key]=best_def_similariry(definizioni_dict[key])
    return result
