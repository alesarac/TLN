import numpy as np
import math

PATH_NASARI_VECT = './resources/dd-nasari.txt'


def parse_nasari():

    with open(PATH_NASARI_VECT, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    result, nasari_parsed = [], {}

    for line in lines:
        result.append(line.strip().split(';'))

    for row in result:
        b_id = row[0]
        word = row[1].lower()
        synsets = row[2:]
        nasari_parsed[word] = []
        tmp = {}

        for syn in synsets:
            syn_splitted = syn.strip().split('_')
            if len(syn_splitted) > 1:
                tmp[syn_splitted[0]] = float(syn_splitted[1])
        nasari_parsed[word].append({'b_id': b_id, 'synsets': tmp})
    return nasari_parsed


def get_nasari_vect(words, nasari_parsed):
    vectors = []
    for word in words:
        if word in nasari_parsed.keys():
            vectors.append(nasari_parsed[word][0]['synsets'])
    return vectors


def evaluate_similarity(token_of_sentences, nasari):
    similarities = []

    current_window = get_nasari_vect(token_of_sentences[0], nasari)
    follow_window = get_nasari_vect(token_of_sentences[1], nasari)
    similarities.append(get_similarity_wo(current_window, follow_window)/2)

    for index in range(1, len(token_of_sentences) - 1):
        prev_window = get_nasari_vect(token_of_sentences[index - 1], nasari)
        current_window = get_nasari_vect(token_of_sentences[index], nasari)
        follow_window = get_nasari_vect(token_of_sentences[index + 1], nasari)

        sim_prev = get_similarity_wo(current_window, prev_window)
        sim_follow = get_similarity_wo(current_window, follow_window)
        #print((sim_prev + sim_follow) / 2)
        similarities.append((sim_prev + sim_follow) / 2)

    prev_window = get_nasari_vect(token_of_sentences[len(token_of_sentences) - 2], nasari)
    current_window = get_nasari_vect(token_of_sentences[len(token_of_sentences) - 1], nasari)
    similarities.append(get_similarity_wo(current_window, prev_window)/2)

    return similarities

def rank(q, v1):
    for index, item in enumerate(v1):
        if list(item)[1] == q:
            return index + 1

def weighted_overlap(w1, w2):
    O = set(w1.keys()).intersection(w2.keys())
    rank_acc, den = 0, 0
    if len(O):
        for i, q in enumerate(O):
            den += 1. / (2 * (i + 1))
            # ( rank of q in_w1 + rank of q in_w2 ) ^ (-1)
            rank_acc += 1. / (rank(q, [(v, k) for k, v in w1.items()]) + rank(q, [(v, k) for k, v in w2.items()]))
        return np.sqrt(pow(rank_acc, -1) / den)
    else:
        return 0.0

def get_similarity_wo(v1, v2):
    similarity = []
    for word1 in v1:
        for word2 in v2:
            similarity.append(weighted_overlap(word1, word2))

    if len(similarity) > 0:
        return sum(similarity)/(len(v1)*len(v2)+2)*10
    else:
        return 0