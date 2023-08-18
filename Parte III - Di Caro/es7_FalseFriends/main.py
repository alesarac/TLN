import re
from fuzzywuzzy import fuzz
from prettytable import PrettyTable
from nltk.corpus import wordnet as wn

CORPUS = "./resources/wikisent2.txt"
STOP_WORDS_FILE = open("./resources/stop_words_FULL.txt", 'r')
STOP_WORDS_SET = set([line.strip() for line in STOP_WORDS_FILE])

NUMBER_OF_FALSE_FRIENDS = 15
LEX_SIMILARITY_THRESHOLD = 90
SEM_SIMILARITY_THRESHOLD = 0.10


"""
data una lista di parole, restituisce un BoW
lasciando le parole che contengono solo lettere
"""
def bag_of_words(sentence):
    only_words = re.findall(r'\b[A-Za-z][A-Za-z]*\b', sentence)
    sent_no_stopwords = [elem for elem in only_words if elem.lower() not in STOP_WORDS_SET]
    return sent_no_stopwords


"""
legge e parsifica il coprus ritornando in output
un unica lista contenente le BoW del corpus (senza parole duplicate)
"""
def parse_corpus():
    bow_list = []
    with open(CORPUS, "r", encoding='utf-8') as file:
        for line in file.readlines():
            bow_list.append(bag_of_words(line))
    flat_bow_list = list(set([item for sublist in bow_list for item in sublist])) #len = 1507779

    for elem in flat_bow_list:
        if wn.synsets(elem) == []:
            flat_bow_list.remove(elem)
    return flat_bow_list


"""
dato un coprus di parole, restituisce una lista con le coppie di parole che
presentano una veste lessicale con una similarità maggiore di 80 (LEX_SIMILARITY_THRESHOLD)
"""
def lex_similar_words(word_list):
    word_pairs = []
    print(len(word_list))
    for i in range(len(word_list)):
        for j in range(i+1,len(word_list)):
            fuzz_ratio = fuzz.ratio(word_list[i],word_list[j])
            if fuzz_ratio > LEX_SIMILARITY_THRESHOLD:
                word_pairs.append((word_list[i],word_list[j],fuzz_ratio))
        print(i)
    return sorted(word_pairs, key=lambda t: t[2], reverse=True)


"""
data una lista di coppie di parole, restituisce una lista con le coppie di parole
che presentano una similarità semantica minore di 10 (SEM_SIMILARITY_THRESHOLD)
"""
def false_friends(pairs_list):
    false_friends_list = []
    for pair in pairs_list:
        try:
            synset1 = wn.synsets(pair[0])[0]
            synset2 = wn.synsets(pair[1])[0]

            wup = wn.wup_similarity(synset1,synset2)
            if wup <= SEM_SIMILARITY_THRESHOLD:
                false_friends_list.append((pair[0],pair[1],pair[2],wup))
        except:
          continue

    return sorted(false_friends_list, key=lambda t: t[2])




#### MAIN ##############################################################################

if __name__ == '__main__':

    coprus_parsed = parse_corpus()

    lex_sim_word_pairs = lex_similar_words(coprus_parsed)

    sem_sim_word_pairs = false_friends(lex_sim_word_pairs)

    result_table = PrettyTable()
    result_table.field_names = ["word pairs", "lex sim", "sem sim"]


    for elem in sem_sim_word_pairs[:NUMBER_OF_FALSE_FRIENDS]:
        result_table.add_row([(elem[0] +' - '+elem[1]),elem[2],round(elem[3],2)])

    print(result_table)
