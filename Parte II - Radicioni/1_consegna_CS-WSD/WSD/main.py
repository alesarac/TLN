from prettytable import PrettyTable
import utils
import my_lesk
from nltk.wsd import lesk
from statistics import mean

N_WORDS = 50
N_ATTEMPTS = 10

mean_accuracy_my_LESK = []
mean_accuracy_nltk_LESK = []

if __name__ == "__main__":

    for attempt in range(N_ATTEMPTS):
        print(f"\nIterazione #{attempt+1}")
        my_correct_wsd = 0
        ntlk_correct_wds = 0

        results_table = PrettyTable()
        results_table.field_names = ["Termine", "Synset (SemCor)", "Synset (my_LESK)", "Synset (nltk_LESK)", "my_LESK", "nltk_LESK"]

        terms = utils.process_corpus(N_WORDS)

        for elem in terms:
            my_disambiguation = my_lesk.lesk(elem[0], elem[2]) # LESK mio
            nltk_disambiguation = lesk(elem[2], elem[0], 'n') # LESK NLTK
            results_table.add_row([elem[0], str(elem[1]), str(my_disambiguation), str(nltk_disambiguation), True if (my_disambiguation is not None and elem[1] == my_disambiguation) else False, True if (nltk_disambiguation is not None and elem[1] == nltk_disambiguation) else False])
            my_correct_wsd = my_correct_wsd + 1 if elem[1] == my_disambiguation else my_correct_wsd
            ntlk_correct_wds = ntlk_correct_wds + 1 if (nltk_disambiguation is not None and elem[1] == nltk_disambiguation) else ntlk_correct_wds
        results_table.add_row(["","","","","",""])
        results_table.add_row(["","Correttezza:",str(my_correct_wsd) + " su " + str(N_WORDS), str(ntlk_correct_wds) + " su " + str(N_WORDS), str(int((my_correct_wsd/N_WORDS)*100))+"%", str(int((ntlk_correct_wds/N_WORDS)*100))+"%"])
        mean_accuracy_my_LESK.append(my_correct_wsd/N_WORDS)
        mean_accuracy_nltk_LESK.append(ntlk_correct_wds/N_WORDS)
        print(results_table)
    print(f"\n\nAccuratezza media \'my_LESK\': {str(round((mean(mean_accuracy_my_LESK)*100),2))}%")
    print(f"\nAccuratezza media \'nltk_LESK\': {str(round((mean(mean_accuracy_nltk_LESK)*100),2))}%")
