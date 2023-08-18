from nltk.corpus import semcor
from nltk.corpus.reader.wordnet import Lemma
import random
import re
from nltk.corpus import wordnet as wn

LEN_SEMCOR = 37176 #len(semcor.sents())
SEMCOR_TAGGED_SENTS = semcor.tagged_sents(tag='both') # mi salvo tutte le 37176 frasi con postag,synsets,eccc.. di semcor
SEMCOR_SENTS = semcor.sents() # mi salvo tutte le 37176 frasi di semcor
STOP_WORDS_FILE =  open(r"../resources/stop_words_FULL.txt", 'r')

def process_corpus(n_words):
    terms = []
    list_index = []
    while(len(terms) < n_words):
        rand_index = random.randrange(0, LEN_SEMCOR-1)
        if rand_index not in list_index: #per evitare che si prenda una frase già presa in precedenza
            list_index.append(rand_index)
            for tagged_chunks in SEMCOR_TAGGED_SENTS[rand_index]:
                if isinstance(tagged_chunks.label(), Lemma): #prendo solo i termini con Lemma
                    if tagged_chunks[0].label() == 'NN': #controllo se il POS del termine è un sostantivo
                        if len(wn.synsets(tagged_chunks[0][0])) > 1: #controllo se il termine ha più di un synset su WordNet
                            terms.append([tagged_chunks[0][0], tagged_chunks.label().synset(), SEMCOR_SENTS[rand_index]]) #aggiungo il termine, il synset di SemCor e la frase del termine
                            #print(f"Sono alla frase {len(terms)}\n")
                            break
    return terms

def process_stop_words():
    return set([line.strip() for line in STOP_WORDS_FILE])


def clean_sentence(sentence):
    sentence_lower = [elem.lower() for elem in sentence] #porto in minuscolo
    sentence_no_stop = list(set(sentence_lower).difference(process_stop_words())) #rimuvo le stopwords
    sentence_only_letters = [re.sub(r'[^A-Za-z]+', '', x) for x in sentence_no_stop] # rimuovo la punteggiatura
    sentence_no_spaces = [ele for ele in sentence_only_letters if ele.strip()] # rimuovo gli spazi vuoti
    sentence_lemmatized = [wn.morphy(elem) for elem in sentence_no_spaces] # lemmatizzo
    return set(sentence_lemmatized)
