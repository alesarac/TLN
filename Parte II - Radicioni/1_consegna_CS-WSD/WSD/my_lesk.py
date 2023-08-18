import re
from nltk.corpus import wordnet as wn
import utils

def lesk(term, sentence):
    best_sense = wn.synsets(term)[0] #all'inizio metto best_sense al primo synset del termine in questione
    max_overlap = 0
    context = utils.clean_sentence(sentence) #pulisco la frase passata al metodo
    for sense in wn.synsets(term): #cicliamo sui synset del termine in questione
        signature = []
        for example in sense.examples():
            signature = signature + example.split() #salviamo in signature le info sugli esempi del synset trattato
        for glos in sense.definition().split():
            signature = signature + re.sub(r"[^a-zA-Z0-9]", "", glos).split() #salviamo in signature le info sulla definizione del synset trattato
        filtered = utils.clean_sentence(signature) #pulisco la segnature
        overlap = len(filtered.intersection(context)) #guardo gli elementi in comune tra signature e la frase passata in input
        if overlap > max_overlap: #chi ha più termini in comune farà si che il synset trattato diventi il best_synset
            max_overlap = overlap
            best_sense = sense

    return best_sense
