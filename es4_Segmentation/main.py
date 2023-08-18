import nasari_utils as nu
import utils as ut
import numpy as np

CORPUS_PATH = './resources/doc_merge.txt'
WINDOWS_SIZE = 1


if __name__ == '__main__':

    # Parse corpus
    corpus = ut.get_corpus(CORPUS_PATH)

    # Parsing nasari vectors
    nasari_parsed = nu.parse_nasari()

    gold_break_points = [15, 29]

    # Splitting
    windows = ut.split_corpus(corpus, WINDOWS_SIZE)

    # Tokenizing
    clean_sentences = ut.clean_text(windows)

    # Evaluate similairty between windows
    similarities = nu.evaluate_similarity(clean_sentences, nasari_parsed)

    # Find break point
    break_point = ut.find_break_points(similarities, len(gold_break_points))

    # Get result
    ut.plot_result(break_point, gold_break_points, similarities, WINDOWS_SIZE)

    # Get cohesion_matrix
    matrix = ut.cohesion_matrix(clean_sentences)

    print(matrix)
