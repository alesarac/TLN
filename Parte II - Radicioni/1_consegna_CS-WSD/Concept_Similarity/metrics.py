import utils
from nltk.corpus import wordnet
from math import log

# DEPTH_MAX: è la profondità massima di WordNet, andando a trovare il max della distanza dei più lontani iperonimi ovvero: 20
DEPTH_MAX = max(max(len(hyp_path) for hyp_path in ss.hypernym_paths()) for ss in wordnet.all_synsets())

############### 1. WU & PALMER SIMILARITY ################
def wu_palmer(w1, w2):
    max_sim = 0
    for s1 in wordnet.synsets(w1):
        for s2 in wordnet.synsets(w2):
            wup_similariry = utils.wup_calculus(s1, s2)
            if wup_similariry > max_sim:
                max_sim = wup_similariry
    return max_sim

################ 2. SHORTEST PATH ################
def shortest_path(w1, w2):

    min_length = DEPTH_MAX * 2
    for s1 in wordnet.synsets(w1):
        for s2 in wordnet.synsets(w2):
            len = utils.len_path(s1,s2)
            if len:
                if len < min_length:
                    min_length = len
    return 2 * DEPTH_MAX - min_length


################ 3. LEACOCK-CHODOROW ################
def leacock_chodorow(w1, w2):
    max_sim = 0
    for s1 in wordnet.synsets(w1):
        for s2 in wordnet.synsets(w2):
            len = utils.len_path(s1,s2)
            if len:
                if len > 0:
                    sim = -(log(len / (2 * DEPTH_MAX)))
                else:
                    sim = -(log(len + 1 / (2 * DEPTH_MAX + 1)))
            else:
                sim = 0
            if sim > max_sim:
                max_sim = sim
    return max_sim
