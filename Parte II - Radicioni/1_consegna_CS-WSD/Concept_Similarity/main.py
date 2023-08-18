import metrics
from nltk.corpus import wordnet
from scipy import stats
import pandas as pd


if __name__ == "__main__":

    #leggo il csv
    wordSim353 = pd.read_csv(r'../resources/WordSim353.csv', sep=',')

    #liste con i valori delle metriche per ciascuna coppia di parole del csv
    wup_list = []
    sp_list = []
    lc_list = []
    human_score_list = []

    for row in wordSim353.itertuples():
        wup_list.append(metrics.wu_palmer(row[1], row[2]))
        sp_list.append(metrics.shortest_path(row[1], row[2]))
        lc_list.append(metrics.leacock_chodorow(row[1], row[2]))
        human_score_list.append(row[3])

    #stampa dei valori con le funzioni implementate
    print('\n---------- WU & PALMER SIMILARITY ----------')
    print('Pearson correlation: {:.4f}'.format(stats.pearsonr(wup_list, human_score_list)[0]))
    print('Spearman correlation: {:.4f}'.format(stats.spearmanr(wup_list, human_score_list)[0]))

    print('\n---------- SHORTEST PATH ----------')
    print('Pearson correlation: {:.4f}'.format(stats.pearsonr(sp_list, human_score_list)[0]))
    print('Spearman correlation: {:.4f}'.format(stats.spearmanr(sp_list, human_score_list)[0]))

    print('\n---------- LEACOCK CHODOROW ----------')
    print('Pearson correlation: {:.4f}'.format(stats.pearsonr(lc_list, human_score_list)[0]))
    print('Spearman correlation: {:.4f}'.format(stats.spearmanr(lc_list, human_score_list)[0]))



    # #stampa dei valori con le funzioni built-in di NLTK
    
    # max_value_similarity_of_wup = []
    # max_value_similarity_of_sp = []
    # max_value_similarity_of_lc = []
    #
    # for row in wordSim353.itertuples():
    #     true_value_of_wup=[]
    #     true_value_of_sp=[]
    #     true_value_of_lc=[]
    #
    #     for s1 in wordnet.synsets(row[1]):
    #         for s2 in wordnet.synsets(row[2]):
    #             if s1.pos()==s2.pos():
    #                 true_value_of_wup.append(s1.wup_similarity(s2))
    #                 true_value_of_sp.append(s1.shortest_path_distance(s2))
    #                 true_value_of_lc.append(s1.lch_similarity(s2))
    #
    #             #caso: investor e earning (earning è un verbo mentre investor è un sostantivo)
    #             else:
    #                 true_value_of_wup.append(0)
    #                 true_value_of_sp.append(0)
    #                 true_value_of_lc.append(0)
    #
    #     #caso: Maradoona e football (Maradona non ha synset)
    #     if ((wordnet.synsets(row[1]) or wordnet.synsets(row[2])) == []):
    #         true_value_of_wup.append(0)
    #         true_value_of_sp.append(0)
    #         true_value_of_lc.append(0)
    #
    #     max_value_similarity_of_wup.append(max([0 if i is None else i for i in true_value_of_wup]))
    #     max_value_similarity_of_sp.append(max([0 if i is None else i for i in true_value_of_sp]))
    #     max_value_similarity_of_lc.append(max([0 if i is None else i for i in true_value_of_lc]))
    #
    # # Pearson correlation coefficient con le metriche di NLTK
    # print(f"wup_Pearson: {round(stats.pearsonr(max_value_similarity_of_wup, human_score_list)[0],5)}")
    # print(f"sp_Pearson: {round(stats.pearsonr(max_value_similarity_of_sp, human_score_list)[0],5)}")
    # print(f"lc_Pearson: {round(stats.pearsonr(max_value_similarity_of_lc, human_score_list)[0],5)}\n\n")
    #
    # # Spearman's rank correlation coefficient con le metriche di NLTK
    # print(f"wup_Spearman: {round(stats.spearmanr(max_value_similarity_of_wup, human_score_list)[0],5)}")
    # print(f"sp_Spearman: {round(stats.spearmanr(max_value_similarity_of_sp, human_score_list)[0],5)}")
    # print(f"lc_Spearman: {round(stats.spearmanr(max_value_similarity_of_lc, human_score_list)[0],5)}")


"""
#NLTK RESULT
wup_Pearson: 0.29475
sp_Pearson: -0.13089
lc_Pearson: 0.32598


wup_Spearman: 0.33825
sp_Spearman: -0.10506
lc_Spearman: 0.30119


#MY RESULT
wup_Pearson: 0.2675
sp_Pearson: 0.08635
lc_Pearson: 0.23804


wup_Spearman: 0.31788
sp_Spearman: 0.22591
lc_Spearman: 0.22591
"""
