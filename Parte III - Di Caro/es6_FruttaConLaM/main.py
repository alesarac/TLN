import nltk
from nltk.corpus import wordnet as wn
from time import sleep

"""
data una parola in input ritorna
la lista dei synset associati
"""
def get_topic_synsets(word):
    return wn.synsets(word)


def get_synsets_hypo_dict(synsets_list):

    synsets_hypo_dict = {}
    for synset in synsets_list:
        synsets_hypo_dict[synset]=get_hyponyms(synset)
    return synsets_hypo_dict

"""
dato un synset in input ritorno la gerarchia di tutti i suoi iponimi
"""
def get_hyponyms(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms |= set(get_hyponyms(hyponym))
    return hyponyms | set(synset.hyponyms())

"""
data una lista di iponimi (synset) e un synset di riferimento
ritorno la distanza tra ogni synset della lista di iponimi e il synset di riferimento
il valore della distanza è definito come un "rank": più la distanza è minore più il synset
delle lista degli iponimi sarà "vicino" al synset di riferimento
la lista viene restituita ordinata dal valore più piccolo di rank
"""
def rank_hyponyms(hyponyms_list, synset):
    hyponyms_rank = []

    for hyponym in hyponyms_list:
        if hyponym.lexname() == 'noun.food':
            hyponyms_rank.append((hyponym,0))
        else:
            hyponyms_rank.append((hyponym,hyponym.shortest_path_distance(synset)))
    return sorted(hyponyms_rank, key = lambda x: x[1], reverse=False)

"""
data una lista di synset ritorna una
lista di lemma dei synset mantenendo il rank
"""
def synset_to_lemma(synsets_list):
    return [[elem[0].lemmas()[0].name().lower(),elem[1]] for elem in synsets_list]

"""
controlla se nella lista di parole data in input
ci sia una parola che inizi con la lettera data in input
"""
def find_word_by_start_letter(word_list,letter):
    word_found = []
    for word in word_list:
        if word[0].lower().startswith(letter.lower()):
            word_found.append(word[0])
    return word_found


letter, topic = input("Write a letter and a topic\nThan i'll return a word about your topic, that start with your letter\n\nEXAMPLE: \'a fruit\'\n\n").split()

topic_synsets = get_topic_synsets(topic)

hyponym_hierarchy = get_hyponyms(topic_synsets[0])

hyponyms_rank = rank_hyponyms(hyponym_hierarchy,topic_synsets[0])

lemma_list = synset_to_lemma(hyponyms_rank)

word_found = find_word_by_start_letter(lemma_list,letter)

if word_found:

    word_found = [elem.replace('_', ' ') for elem in word_found] # per togliere gli uderscore dai risultati

    print(f"\nThe word found is: {word_found[0]}")
    if len(word_found) > 2:
        sleep(2)
        other = input("\nDo you want to see other possible words?\nType y or n: ")
        if other == 'y':
            print(f"\nOther word are: {word_found[1:]} ecc..")
        else:
            print("\nOk, good bye!")
else:
    print("\nI'm sorry.\nI couldn't find a word :(")
