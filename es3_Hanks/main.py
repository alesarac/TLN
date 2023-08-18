import matplotlib.pyplot as plt
from collections import Counter
import utils as ut


if __name__ == "__main__":

    parse_result = ut.parse_corpus()

    fillers_result = ut.extract_fillers(parse_result)

    #conto le coppie di semantic type
    counter_pairs = Counter(fillers_result).most_common(15)
    print(f"Frequenza Semantic Type coppie: {counter_pairs}\n")
    #conto i tipi di semantic type singoli
    count_subj, count_obj = map(list, zip(*[elem.split('-') for elem in fillers_result]))
    print(f"Frequenza Semantic Type del Soggetto: {Counter([elem.strip() for elem in count_subj]).most_common()}\n")
    print(f"Frequenza Semantic Type dell'oggetto: {Counter([elem.strip() for elem in count_obj]).most_common()}")

    #creo il grafico per le coppie
    data = dict(counter_pairs)
    sem_type_pairs = list(data.keys())
    freq = list(data.values())

    fig = plt.figure(figsize = (10, 5))
    plt.bar(sem_type_pairs, freq, color ='blue',width = 0.4)

    plt.xlabel("semantic types pairs")
    plt.ylabel("occurrences")
    plt.title("Semantic cluster of verb CREATE")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
