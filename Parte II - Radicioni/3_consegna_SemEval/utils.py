import requests
import csv
import numpy as np

PATH_SENSE2SYN = r'./resources/SemEval17_IT_senses2synsets.txt'
PATH_NASARI = r'./resources/mini_NASARI.tsv'
PATH_IT_TEST_DATA = r'./resources/it.test.data.tsv'
BABELNET_API_KEY = 'c69de83e-2cfa-44f5-93de-20b29032628e'
#fattore per avere i valori della cos_sim della stessa scala dei valori annoatati a mano
NORMALIZER_FACTOR = 4


#### Parte 1 ###################################################################

def parse_mini_nasari():
    '''
    Parsifichiamo il file 'mini_NASARI.tsv'
    e ritorniamo un dizionario
        {synset:vector}
        (chiave = synset e valore = vettore)
    '''
    dict = {}
    with open(PATH_NASARI, 'r', encoding='utf-8') as fd:
        rd = csv.reader(fd, delimiter="\t", quotechar='"')
        for row in rd:
            synset= row[0]
            index = synset.index('_')
            synset = synset[:index]
            dict[synset] = row[1:]

    return dict

NASARI = parse_mini_nasari()

def parse_it_test_data():
    with open(PATH_IT_TEST_DATA, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    pairs, score = [], []
    for line in lines:
        terms = line.split('\t')
        pairs.append((terms[0].lower().strip(), terms[1].lower().strip()))
        score.append(float(terms[2].strip()))
    return pairs, score

def get_synsets_from_term(term):
    """
    Dato il termine trova i suoi babelSynsetIDs nel file 'SemEval17_IT_senses2synsets.txt'
    :param term: il termine di cui cercare i babelSynsetIDs
    :return: la lista di babelSynsetIDs del termine o la lista vuota se il termine non viene trovato
    """
    start = False  # flag per quando iniziano i babelSynsetIDs
    res = []
    with open(PATH_SENSE2SYN, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if start:  # iniziamo a raccogliere gli id
                if line[0] == '#':  # se la linea inizia per '#' vuol dire che iniziano gli ID di un nuovo termine e che quindi dobbiamo fermarci
                    return res
                res.append(line.rstrip('\n'))
            elif line.rstrip('\n').lower() == '#'+term:  # quando troviamo il termine possiamo iniziare a raccogliere i babelSynsetIDs (start = True)
                start = True
    return res

"""
dati i synset di due termini restituisce
la massima similarità (max cosine similarity) con il metodo
cosine_similarity
"""
def get_max_similarity(synset_of_term_1, synset_of_term_2):
    max_sim = 0
    for syn_t1 in synset_of_term_1: #'bn:03353031n'
        for syn_t2 in synset_of_term_2: #'bn:00010543n'
            if syn_t1 in NASARI and syn_t2 in NASARI: #controllo se il synsey del termine 1 e quello del termine 2 che sto trattando attualmente siano presenti nel dizionario di Nasari
                nasari_vect_t1 = NASARI[syn_t1] #memorizzo i valori di quel synset del termine 1
                nasari_vect_t2 = NASARI[syn_t2] #memorizzo i valori di quel synset del termine 2
                similarity = cosine_similarity(nasari_vect_t1, nasari_vect_t2) #calcolo la cos_sim tra i due vettori con i valori all'interno
                if similarity > max_sim: #controllo se cambiare la max sim
                    max_sim = similarity
    return max_sim

"""
cicla sui babelSynsetIDs di ciascuna coppia di termini in input
e restituisce la massima similarità (max cosine similarity).
Tale metodo quindi si avvale su altri due metodi:
    - get_synsets_from_term
    - get_max_similarity
"""
def max_nasari_similarity(terms):
    cos_similarity_values = []
    for t1, t2 in terms:
        synset_of_term_1 = get_synsets_from_term(t1)
        synset_of_term_2 = get_synsets_from_term(t2)
        if (synset_of_term_1 and synset_of_term_2):
            similarity = get_max_similarity(synset_of_term_1,synset_of_term_2)
            cos_similarity_values.append(round((similarity * NORMALIZER_FACTOR),2))

    return cos_similarity_values



#### Parte 2 ###################################################################


#Output List(V) -> V = [Term1 Term2 B_ID1 B_ID2 Term_BID1 Term_BID2]
def parse_bn_syns_annotated():
    bid_annotated = []
    with open(PATH_IT_TEST_DATA, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        bid_annotated.append(line.split('\t'))
    return bid_annotated

def cosine_similarity(v1, v2):
    v1 = np.array(v1, dtype=np.float32)
    v2 = np.array(v2, dtype=np.float32)
    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)
    return num / den

"""
lavora in maniera analoga al metodo "get_synsets_from_term"
ma questa volta ritorna i babelSynsetIDs che hanno
portato alla massima cosine similarity
"""
def get_best_syns_by_term(t1, t2):
    max_sim, best_s1, best_s2 = 0, None, None
    for syn_t1 in get_synsets_from_term(t1):
        for syn_t2 in get_synsets_from_term(t2):
            if syn_t1 in NASARI and syn_t2 in NASARI:
                nasari_vect_t1 = NASARI[syn_t1]
                nasari_vect_t2 = NASARI[syn_t2]
                sim = cosine_similarity(nasari_vect_t1, nasari_vect_t2)
                if sim > max_sim:
                    max_sim = sim
                    best_s1 = syn_t1
                    best_s2 = syn_t2
    return best_s1, best_s2
    
"""
metodo che dato un babelSynset consente di
ricavare i suoi termini grazie alle API di BabelNet
"""
def get_terms_by_synset(bn_synset):
    terms_list = []
    res = requests.get('https://babelnet.io/v7/getSynset?id={}&targetLang=IT&key={}'.format(bn_synset, BABELNET_API_KEY))
    response = res.json()
    if 'senses' in response:
        senses_list = response['senses']
        for s in senses_list:
            if s['type'] == 'WordNetSense' or s['type'] == 'BabelSense':
                terms_list.append(s['properties']['fullLemma'])
    #prendiamo solo i primi 5
    return list(set(terms_list))[:5]
