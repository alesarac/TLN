from prettytable import PrettyTable
from nltk.corpus import wordnet as wn
import utils as ut

# MAIN #########################################################################
if __name__ == "__main__":

    #risultati per onomasiological_by_word_freq
    result_by_word_freq = ut.onomasiological_by_word_freq()

    table = PrettyTable()
    table.field_names = ["Concetto", "correct synset", "best synsets found", "correct gloss", "best gloss found"]

    for key in result_by_word_freq:
        best_synsets_found=' '.join([str(item) for item in [(item[1],item[2]) for item in result_by_word_freq[key]]])
        best_gloss_found=' '.join([str(item) for item in [item[0] for item in result_by_word_freq[key]]])
        row_result = [key, str(wn.synsets(key)[0]), best_synsets_found, wn.synsets(key)[0].definition(), best_gloss_found]
        table.add_row(row_result)
    print(table)

    #risultati per onomasiological_by_sentences_sim
    result_by_sentences_sim = ut.onomasiological_by_sentences_sim()
    print(result_by_sentences_sim)
