import string
import spacy
import random
from nltk.wsd import lesk

GENERAL_CORPUS="wikisent2.txt" #Collection of 7.8 million sentences from the August 2018 English Wikipedia dump
LEN_GENERAL_CORPUS = 7871825 # len(content)
LEN_CORPUS_SENT = 1000 # dovrebbe essere almeno 1000 frasi

VERB = 'create'
POSSIBLE_SUBJ = ['subj', 'nsubj']
POSSIBLE_OBJ = ['pobj', 'dobj', 'obj']
SEMANTIC_TYPE_PRONOUNS = ["i", "you", "he", "she", "we", "they", "me", "him", "her", "his", "them", "someone", "us", "people", "anyone"]


nlp = spacy.load('en_core_web_trf')


def parse_corpus():
    corpus_parsed=[]

    with open(GENERAL_CORPUS, "r", encoding='utf-8') as file:
        content = file.readlines()
        while len(corpus_parsed)<LEN_CORPUS_SENT:
            rand_index = random.randint(0, (LEN_GENERAL_CORPUS-1)) # prendo un indice randomicamente
            if VERB in content[rand_index]: # per ogni fase in cui c'è il verbo d'interesse
                sentence_tokens = nlp(content[rand_index])  # faccio il parsing per vedere
                subj_obj_result = exist_subj_obj(sentence_tokens) # se esiste un soggetto e un complemento oggetto
                if (subj_obj_result[0]): #il valore di verità è in prima posizione
                    if(verb_is_trans_verb(sentence_tokens,subj_obj_result[1],subj_obj_result[2])): # e se il verbo in questione è davvero un verbo o altro (tipo un sostantivo)  e se è legato con il soggetto e il complemento trovati prima
                        corpus_parsed.append([sentence_tokens,subj_obj_result[1],subj_obj_result[2]]) # se tutto è soddisfatto allora aggiungo alla lista corpus_parsed: la frase, il soggetto e il complemento
                        print(f"mancano: {LEN_CORPUS_SENT-len(corpus_parsed)} frasi")
    return corpus_parsed

def exist_subj_obj(tokens):
    subj=False
    obj=False
    subj_value=''
    obj_value=''
    for token in tokens:
        if(token.dep_ in POSSIBLE_SUBJ):
            subj_value=token.text
            subj=True
        if(token.dep_ in POSSIBLE_OBJ):
            obj_value=token.text
            obj=True
    return [(subj and obj),subj_value,obj_value]

def verb_is_trans_verb(tokens,subj,obj):
    is_verb = False
    for token in tokens:
        if (token.lemma_ == VERB) and (token.pos_ == 'VERB'):
            child = [str(child) for child in token.children]
            if (subj in child) and (obj in child):
                is_verb=True
    return is_verb

#esegue la WSD con lesk e poi ritorna il semantic_type del synset trovato
def semantic_type(sentence, word):
    if word.lower() in SEMANTIC_TYPE_PRONOUNS: #le parole che sono pronomi le categorizzo subito come person
        return 'noun.person'
    lesk_result = lesk(sentence, word)
    if lesk_result:
        return lesk_result.lexname()
    return None

def extract_fillers(corpus):
    result_list = []
    for elem in corpus:
        subj_lex = semantic_type(elem[0],elem[1])
        obj_lex = semantic_type(elem[0],elem[2])
        if subj_lex != None and obj_lex != None:
            result_list.append(str(subj_lex) + ' - ' + str(obj_lex))
    return result_list
