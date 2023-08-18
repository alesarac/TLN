import math

############### WUP - funzioni di utility/supporto ###############

def wup_calculus(syns1, syns2):
    lcs = search_lcs(syns1, syns2)
    return ((2 * min_depth(lcs) / (min_depth(syns1) + min_depth(syns2))) if lcs else 0)

def all_hypernyms(s):
    hypernyms = s.hypernyms() + s.instance_hypernyms()
    for hypernym in hypernyms:
        hypernyms.extend(get_hypernyms(hypernym))
    return hypernyms

def get_hypernyms(s):
    if not s._all_hypernyms:
        s._all_hypernyms = all_hypernyms(s)
    return s._all_hypernyms

def intersection(hp1, hp2):
    return list(set(hp1).intersection(set(hp2)))

def shortest_len_hypernym(sense, hypernym):
    hypernyms_distance = [(sense, 0)]
    paths = {}

    while len(hypernyms_distance) > 0:
        sense_depth = hypernyms_distance[0]
        sense, depth = sense_depth[0], sense_depth[1]
        del hypernyms_distance[0]

        if sense in paths:
            continue

        paths[sense] = depth
        depth += 1
        hypernyms_distance.extend([(hyp, depth) for hyp in sense._hypernyms()])
        hypernyms_distance.extend([(hyp, depth) for hyp in sense._instance_hypernyms()])

    return paths[hypernym]


def min_depth(synset):
    highest_senses, distances = synset.root_hypernyms(), []

    for sense in highest_senses:
        distances.append(shortest_len_hypernym(synset, sense))

    return min(distances)

"""
Viene calcolato il Lowest Common Subsumer (LCS) tra i due sensi s1 e s2.
L'antenato comune ritornato dalla funzione è calcolato creando 2 insiemi
contenenti rispettivamente gli iperonimi di si e di s2
"""
def search_lcs(syns1, syns2):
    hp1 = get_hypernyms(syns1)
    hp2 = get_hypernyms(syns2)

    # prendiamo gli iperonimi che sono in comune tra i due synset e li mettiamo in questa lista chiamata common
    common = intersection(hp1, hp2)

    # ordiniamo l'intersezioni di iperonimi in base alla loro profondità (cioè alla distanza dalla radice e l'iperonimo in questione)
    lcs = sorted(common, key=lambda hp: hp.max_depth(), reverse=True)

    #ritorniamo il primo elemeno di lcs (se lcs non è vuota) ovvero l'iperonimo comune ai 2 sensi come la minore max_depth()
    return (None if len(lcs) == 0 else lcs[0])



############### SHORTEST PATH e LEACOCK-CHODOROW - funzioni di utility/supporto ###############

def get_paths(node):
    if node.name() == "*ROOT*":
        return {self: 0}
    todo = [(node, 0)]
    lista_path = {}
    while todo:
        nd, depth = todo.pop()
        if nd not in lista_path:
            lista_path[nd] = depth
            depth += 1
            todo.extend((hyp, depth) for hyp in nd.hypernyms())
            todo.extend((hyp, depth) for hyp in nd._instance_hypernyms())
    return lista_path


"""
    Calcola la lunghezza del percorso, se esiste, tra i due sensi.
    Nello specifico, conta la distanza tra i nodi associati ai 2
    synset dati in inpput. La distanza è calcolata come somma del numero di nodi
    da attraversare dal syn1 fino al LCS tra syn1 e syn2, (se esiste) +
    il numero dei nodi da attraversare dal syn2 al LCS tra syn1 e syn2.
"""
def len_path(s1, s2):
    if s1 == s2:
        return 0
    path1 = get_paths(s1)

    s1._shortest_hypernym_paths(False)
    s2._shortest_hypernym_paths(False)

    path2 = get_paths(s2)
    min_dist = float("inf")

    for synset, d1 in path1.items():
        d2 = path2.get(synset, float("inf"))
        min_dist = min(min_dist, d1 + d2)
    return None if math.isinf(min_dist) else min_dist
