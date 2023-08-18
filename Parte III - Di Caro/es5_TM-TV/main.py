from nltk.corpus import webtext
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
import pyLDAvis
from pprint import pprint

N_TOPICS = 6

def retrive_coprus():

    corpus_file = nltk.corpus.webtext.fileids()
    corpus_merge = []

    for elem in corpus_file:
        for sent in webtext.sents(elem):
            corpus_merge.append(sent)

    return corpus_merge

def clean_sentences(sentences):
    # Initialize the WordNet lemmatizer
    lemmatizer = WordNetLemmatizer()

    # Get the list of stop words
    stop_words = set(stopwords.words('english'))

    # Define a list to store the cleaned sentences
    cleaned_sentences = []

    # Iterate over each sentence
    for sentence in sentences:

        # Remove punctuation and lemmatize the tokens
        tokens = [lemmatizer.lemmatize(token.lower()) for token in sentence if token.isalpha()]

        # Remove stop words
        tokens = [token for token in tokens if token not in stop_words]

        # Add the cleaned sentence to the list
        cleaned_sentences.append(tokens)

    return cleaned_sentences

def extract_topics(text):

    # Dictionary: Association between token and unique id
    dict_LoS = corpora.Dictionary(text)

    #per vedere gli id associati ad ogni token delle frasi
    #print(dict_LoS.token2id)


    # We can create the bag-of-word representation for a document using the doc2bow method of the dictionary,
    # which returns a sparse representation of the word counts
    BoW_corpus = [dict_LoS.doc2bow(text) for text in text]

    #human readable
    corpus_readable = [[(dict_LoS[id], count) for id, count in line] for line in BoW_corpus]

    # Build LDA model
    lda_model = LdaModel(corpus=BoW_corpus,id2word=dict_LoS,num_topics=N_TOPICS)

    topics = []

    pprint(lda_model.print_topics(N_TOPICS))

    for topic in lda_model.show_topics(num_topics=N_TOPICS, formatted=False):

        topic_dict = {'words':[],'probs':[]}

        for word, prob in topic[1]:
            topic_dict['words'].append(word)
            topic_dict['probs'].append(prob)

        topics.append(topic_dict)

    # topics visualization
    vis = pyLDAvis.gensim_models.prepare(lda_model, BoW_corpus, dict_LoS)
    pyLDAvis.save_html(vis, 'LDA_Visualization.html')

    return topics


## MAIN ###########################################################################################

if __name__ == '__main__':

    coprus = retrive_coprus()

    bag_of_words = clean_sentences(coprus)

    topics = extract_topics(bag_of_words)
