import csv
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from collections import Counter
from prettytable import PrettyTable

FILE = "./resources/definizioni.csv"
N_WORDS = 5 #numero di parole da tenere con frequenza maggiore
N_DEFINITIONS = 32
STOP_WORDS_FILE = open("./resources/stop_words_FULL.txt", 'r')
STOP_WORDS_SET = set([line.strip() for line in STOP_WORDS_FILE])

def process_defs(defs):
    defs_cleaned=[]
    for sentence in defs:
        sent_no_punct = re.sub('\s\s+', ' ', re.sub(r'[^\w\s]', '', sentence))
        sent_lemmatizzed = lemmatization(sent_no_punct)
        #sent_no_stopwords = [elem for elem in sent_lemmatizzed if elem not in STOP_WORDS_SET] #versione con file
        sent_no_stopwords = [elem for elem in sent_lemmatizzed if not elem.lower() in set(stopwords.words('english'))] #versione nltk
        defs_cleaned.append(sent_no_stopwords)
    return defs_cleaned

def lemmatization(sentence):
    sentence_lemmatizzed = []
    lemmatizer = WordNetLemmatizer()
    for tag in nltk.word_tokenize(sentence):
        sentence_lemmatizzed.append(lemmatizer.lemmatize(tag).lower())
    return sentence_lemmatizzed

def parse_input():
    definizioni_dict = {}
    n_term=4
    with open(FILE, "r", encoding='utf-8') as file:
        csv_reader=csv.reader(file,delimiter=";")
        next(csv_reader) #per skippare la prima riga dell'header

        for row in csv_reader:
            if n_term > 0:
                concetto=row[0]
                definizioni=process_defs(row[1:]) #ripulisco le definizioni
                flat_definizioni = [item for sublist in definizioni for item in sublist] # unisco le def in un'unica lista
                word_freq = list(Counter(flat_definizioni).items()) #associo la frequenza ad ogni parola
                definizioni_dict[concetto]=sorted(word_freq,key=lambda t: t[1],reverse=True) #definisco il dizionario con chiave=concetto e valori=lista di tuple (parola,freq) in ordine descrescente
                n_term-=1
    return definizioni_dict

def similarity(definizioni_dict):
    mean_list=[]
    for key in definizioni_dict.keys():
        fisrt_n_words=definizioni_dict[key][:N_WORDS]
        print(f"Parole più frequenti {key.upper()}: {fisrt_n_words}")
        mean=0
        for elem in fisrt_n_words:
            mean+=elem[1]/N_DEFINITIONS
        mean_list.append(round(mean/N_WORDS,2))
    return mean_list


# MAIN #########################################################################
if __name__ == "__main__":

    result = similarity(parse_input())
    table = PrettyTable()
    table.field_names = ["Emotion (generico-astratto)", "Person (concreto-generico)", "Revenge (specifico-astratto)", "Brick (concreto-specifico)"]
    table.add_row(result)
    print(table)
