from utils import *

def blue_metric(document, summary_document):
    """
        Implementazione della metrica BLUE che considera le bag of words
        del documento originale al del documento riassunto
        è una metrica di precisione data dalla seguente formula:
        |{relevant_document} & {retrieved_document}| / |{retrieved_document}|

    """

    # prendo i termini rilevanti dal documento originale e i termini candidati del documento riassunto
    relevant_document = get_gold_terms(document) #sono le gold words
    retrieved_document = get_summary_gold_terms(summary_document)

    numerator = len(list(relevant_document.intersection(retrieved_document)))
    denominator = len(list(retrieved_document))

    if denominator > 0: return 100 * round(numerator / denominator, 2)
    else: return 0


def rouge_metric(document, summary_document):
    """
        Implementazione della metrica ROUGE che considera le bag of words
        del documento originale al del documento riassunto
        è una metrica di recall data dalla seguente formula:
        |{relevant_document} & {retrieved_document}| / |{relevant_document}|
    """

    relevant_document = get_gold_terms(document)
    retrieved_document = get_summary_gold_terms(summary_document)

    numerator = len(list(relevant_document.intersection(retrieved_document)))
    denominator = len(list(relevant_document))

    if denominator > 0: return 100 * round(numerator / denominator, 2)
    else: return 0
