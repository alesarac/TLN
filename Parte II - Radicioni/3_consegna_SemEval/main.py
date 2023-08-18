from scipy import stats
from prettytable import PrettyTable
from utils import *


if __name__ == '__main__':

    # Parte 1
    terms, gold_scores = parse_it_test_data()

    max_cos_similarity_scores = max_nasari_similarity(terms)

    print("Valutazione tra valori annotati da umani (gold) e valore calcolato di cos_similarity\n")
    pearsonr_coef = round(stats.pearsonr(gold_scores, max_cos_similarity_scores)[0],4) #0.7811
    spearmanr_coef = round(stats.spearmanr(gold_scores, max_cos_similarity_scores)[0],4) #0.8057
    print("Spearman: ", spearmanr_coef)
    print("Pearson: ", pearsonr_coef)

    table = PrettyTable()
    table_ridotta = PrettyTable()
    table.field_names = ["termine 1", "termine 2", "gold_score", "cos_sim_score", "BN syn annotato per term1", "BN syn calcolato per term1", "parole per term1 annotate", "parole per term1 calcolate", "BN syn annotato per term2", "BN syn calcolato per term2", "parole per term2 annotate", "parole per term2 calcolate"]
    table_ridotta.field_names = ["termine 1", "termine 2", "gold_score", "cos_sim_score", "BN syn annotato per term1", "BN syn calcolato per term1", "BN syn annotato per term2", "BN syn calcolato per term2"]

    # table.field_names = ["termine 1", "termine 2", "gold_score", "cos_sim_score"]
    # for i in range (len(terms)):
    #     table.add_row([terms[i][0], terms[i][1], gold_scores[i], max_cos_similarity_scores[i]])
    # print(table)

    # Parte 2
    correct_match_coplues, correct_match_term1, correct_match_term2 = 0, 0, 0
    #legge in input il file “it.test.data.tsv” e recupera i babelSynsetIDs  e i termini annotati a mano:  List(V) -> V = [Term1 Term2 B_ID1 B_ID2 Term_BID1 Term_BID2]
    all_annotation = parse_bn_syns_annotated()

    for i, row in enumerate(all_annotation):

        bn_syns1, bn_syns2 = get_best_syns_by_term(row[0].lower(), row[1].lower())
        terms_list_1 = get_terms_by_synset(bn_syns1)
        terms_list_2 = get_terms_by_synset(bn_syns2)

        table.add_row([terms[i][0], terms[i][1], gold_scores[i], max_cos_similarity_scores[i],row[3],bn_syns1,row[5],terms_list_1,row[4],bn_syns2,row[6],terms_list_2])
        table_ridotta.add_row([terms[i][0], terms[i][1], gold_scores[i], max_cos_similarity_scores[i],row[3],bn_syns1,row[4],bn_syns2])
        # misuro l'accuratezza
        #contando quante volte ho annotato un sysnet diverso (sia per il singolo termine che per le coppie di termini)
        #rispetto a quello trovato massimizzando la cosine similarity nel file mini_NASARI
        if bn_syns1 == row[3] and bn_syns2 == row[4]:
            correct_match_coplues = correct_match_coplues + 1
        if bn_syns1 == row[3]:
            correct_match_term1 = correct_match_term1 + 1
        if bn_syns2 == row[4]:
            correct_match_term2 = correct_match_term2 + 1

    accuracy_couples = (correct_match_coplues)
    accuracy_on_term1 = (correct_match_term1)
    accuracy_on_term2 = (correct_match_term2)

    print("\n\nAccuratezza tra BN synset annotati da umani (gold) e BN synset calcolati con \'cos_similarity\'\n")
    print(f"Accuratezza tra i singoli termini: {(correct_match_term1+correct_match_term2)}%")
    print(f"Accuratezza delle coppie di termini: {(accuracy_couples/50)*100}%")

    print(table_ridotta)
    #print(table)
