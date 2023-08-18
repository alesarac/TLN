import pickle
from pathlib import Path
import random
from time import sleep
import spacy
from spacy import displacy
from datetime import datetime
import json
import simpleNLG as sp
from termcolor import colored

'''
    Funzioni Utility --> inizializzazione
'''

#nlp = spacy.load("en_core_web_trf")
nlp = spacy.load("en_core_web_sm") #Carico la KB

# dizionario globale delle pozioni
pozioni = {}

# Caricamento JSON con le pozioni
def load_json():
    global pozioni
    with open('pozioni.json') as json_file:
        pozioni = json.load(json_file)

#inizializzo i file per la memory e li svuoto nel caso ci siano già
with open('memory/questions.txt', 'wb') as f:
    pickle.dump([], f)

with open('memory/answers.txt', 'w+') as f:
    f.write('')

'''
    Funzioni Utility --> Pre-interrogazione
'''

def parser_ne(frase):

    frase_parsata = nlp(frase)
    dict = {}
    for token in frase_parsata.ents:
        dict[token.text] = [token.text, token.start_char, token.end_char, token.label_]
    for key, value in dict.items():
        if "PERSON" in value:
            return key
    return None

def answer_casata(casata_nome):
    casata_nome =  casata_nome.lower()
    if casata_nome == "gryffindor" or casata_nome == "hufflepuff" or casata_nome == "ravenclaw" or casata_nome == "slytherin":
        print("\n" + "Ok let's proceed!")
        return casata_nome
    else:
        print("You must tell me a valid house name!")
        casata_nome = input("\n" + sp.ask_info("house") + "\n")
        return answer_casata(casata_nome)



'''
    Funzioni Utility --> Gestione dei file di Memory
'''
#le domande vengono serializzate (pickle), infatti il flusso di byte viene conservato, e nel caso ricostruito (repeat_question()).
def write_question(question):
    #apro il file delle domande e mi salvo in una lista (qst_list) le domande già presenti
    with open('memory/questions.txt', 'rb') as f:
        qst_list = pickle.load(f)

    with open('memory/questions.txt', 'wb') as f:
        # se la domanda non era ancora presenre la aggiungo
        if not qst_list:
            qst_list = [question]
        else:
            qst_list.append(question)

        pickle.dump(qst_list, f)

def repeat_question():
    with open('memory/questions.txt', 'rb') as f:
        qst_list = pickle.load(f)
    return str(qst_list[-1])


def write_answer(answer, score):
    with open('memory/answers.txt', 'a+') as f:
        score = str(score)

        if score == 'separator':
            f.write(answer)
        elif 'SBAGLIATA' in score:
            f.write("Risposta utente: " + answer + ' ' + score)
        else:
            f.write("Risposta utente: " + answer + ' - score: ' + score)
        f.write('\n')

'''
    Funzioni Utility --> Interrogazione
'''

# scelgo una pozione da chiedere all'utente in base alla dificoltà da 1 a 10
def selectPoison(difficolta):
    while True:
        pozionicopia = pozioni
        pozione = random.choice(list(pozionicopia))
        if pozionicopia[pozione][0] == difficolta:
            pozioneScelta = {pozione: pozionicopia[pozione]}
            break
    return pozioneScelta

#ritorno una lista di tutti gli ingredienti delle pozioni
def get_all_ingredients():
    load_json()
    ingredients = []
    for p in pozioni:
        for ingredient in pozioni[p][1]:
            if ingredient not in ingredients:
                ingredients.append(ingredient.lower())
    return ingredients

# parsifico la risposta data dall'utente, andando a controllare dove si trova la parola
# ingrediente ovvero se è soggetto (nsubj) oppure complemento (attr).
def get_ingredient(frase):

    sent_dict = {}
    frase_parsificata = nlp(frase)
    displayParser(frase_parsificata)

    position = 'nsubj'

    for chunk in frase_parsificata.noun_chunks:
        if 'ingredient' in chunk.text and chunk.root.dep_ == 'nsubj':
            position = 'attr'
        if chunk.root.dep_ == 'nsubj' or chunk.root.dep_ == 'attr':
            sent_dict[chunk.root.dep_] = chunk
    displayParser(frase_parsificata)
    return sent_dict[position]

# quando l'utente sbaglia l'ingrediente nella risposta
def wrong_ingredient():
    sentences = [
        'Is this Avanti un Altro?! I\'m not Paolo Bonolis!\n',
        'Good answer... but it\'s wrong!\n',
        'That\'s a pity, try again\n'
    ]
    print(random.choice(sentences))

# metodo per controllare se l'ingrediente scritto dall'utente
# sia uno di quelli che doveva dire (ovvero se sia presente nella lista degli ingredienti)
def check_ingredient(ingrediente, ingredienti):

    if ingrediente in ingredienti:
        print(colored('Correct!', 'blue') + "\n")
        sp.printAskIngredient(len(ingredienti))+" "
        ingredienti.remove(ingrediente)
        return ingredienti, True
    else:
        return ingredienti, False

# metodo principale che gestisce le domande relative all'interrogazione
def ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta, domande_pozione, aiuto):

    # separatore per distinguere una domanda dall'altra nel file answers.txt
    if domande_pozione == 0 and domande_fatte >= 1:
        write_answer('\n--------------------------\n', 'separator')

    # chiede una domanda senza "aiuto"
    if not aiuto:
        risposta = input(sp.printAskPotion(pozione, ingredienti_pozione, domande_fatte, domande_pozione))


    # ---- Modalità con AIUTO -----> domanda vero/falso
    else:
        #prendo randomicamente un ingrediente da tutte le pozioni
        ingrediente = random.choice(get_all_ingredients())

        risposta_giusta = 'no'

        #se l'ingrediente che ho preso randomicamente è negli ingredienti dell'attuale pozione
        if ingrediente in [ingr.lower() for ingr in ingredienti_pozione]:
            risposta_giusta = 'yes'
        # pongo il quiz all'utente (vero/falso)
        risposta = str(input(colored(ingrediente, 'yellow') + ' is an ingredient of ' + colored(pozione, 'yellow') + '?\n')).lower()
        # l'utente chiede di ripetere la domanda
        while 'again' in risposta.lower() or 'repeat' in risposta.lower() or 'what?' in risposta.lower():
            risposta = input(repeat_question()).lower()

        else:
            # se l'utente risponde correttamente al vero/falso
            if risposta == risposta_giusta:
                print(colored('Correct!', 'blue') + "\n")

                score = difficolta * len(ingrediente.split()) / 2
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 1, float(score)

            # l'utente sbaglia il quiz e risponde in modo sensato
            elif risposta == 'yes' or risposta == 'no' or 'don\'t know' in risposta:
                if 'don\'t know' in risposta.lower():
                    print('-Don\'t know- it\'s not in my vocabulary!')
                else:
                    wrong_ingredient()
                score = float(-(difficolta * len(ingrediente.split()) / 3))
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 2, score

            # l'utente sbaglia il quiz e risponde in modo insensato
            else:
                print('You must answer to me with valid answer!')
                score = float(-20)
                write_answer(risposta, score)

                return ingredienti_pozione, domande_pozione + 2, score

    # ---- Modalità senza AIUTO ---
    # verifica la risposta dell'utente, scenari possibili:

    # l'utente chiede di ripetere la domanda
    while 'again' in risposta.lower() or 'repeat' in risposta.lower() or 'what?' in risposta.lower():
        risposta = input(repeat_question())

    # l'utente non conosce la risposta -> salta alla domanda successiva
    if 'don\'t know' in risposta.lower():
        score = float(-(difficolta * len(ingredienti_pozione) * 2))
        write_answer(risposta, score)
        ingredienti_pozione = []

        return ingredienti_pozione, len(ingredienti_pozione) + 1, score

    # CASO 1: l'utente risponde indicando la parola "ingredient" nella risposta
    # a questo punto si richiama get_ingredient per parsificare la risposta dell'utente
    if 'ingredient' in risposta:

        risposta_completa = risposta

        # necessario in quanto spacy non li classifica come attr
        if 'lavender' in risposta:
            risposta = 'lavender'
        elif 'mint' in risposta:
            risposta = 'mint'
        else:
            risposta = str(get_ingredient(risposta)) #

        #controllo se l'ingrediente dell'utente sia uno di quelli che doveva dire
        ingredienti_pozione, is_correct = check_ingredient(risposta, ingredienti_pozione)

        # se l'utente ripete un ingrediente che aveva già dato prima, si passa a una prossima domanda
        if risposta in ingredienti_indovinati:
            score = -10.0
            write_answer("Risposta utente: " + risposta + " -> ingrediente ripetuto - score: " + str(score), "separator")
            print("Correct, but you have already guessed this ingredient!\n")
            return ingredienti_pozione, domande_pozione + 1, score

        # se la risposta è corretta
        if is_correct:
            score = difficolta * len(risposta.split())
            write_answer(risposta_completa, score)
            ingredienti_indovinati.append(risposta)

            return ingredienti_pozione, domande_pozione + 1, score

        # se la risposta non è corretta, richiamo questo metodo e metto aiuto=True
        else:
            wrong_ingredient()
            write_answer(risposta, '- è SBAGLIATA -> aiuto')
            return ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta,
                                domande_pozione, True)

    # CASO 2: l'utente risponde senza indicare la parola "ingredient"
    # a questo punto si controlla solo che l'ingrediente sia giusto senza parsificare la risposta
    else:
        # se l'utente ripete un ingrediente che aveva già dato prima
        if risposta in ingredienti_indovinati:
            score = -10.0
            write_answer("Risposta utente: " + risposta + " -> ingrediente ripetuto - score: " + str(score), "separator")
            print("Correct, but you have already guessed this ingredient!\n")
            return ingredienti_pozione, domande_pozione + 1, score

        # se l'ingrediente scritto è giusto
        if risposta in ingredienti_pozione:
            ingredienti_pozione.remove(risposta)
            ingredienti_indovinati.append(risposta)

            score = difficolta * len(risposta.split())
            write_answer(risposta, score)
            print(colored('Correct!', 'blue') + "\n")

            return ingredienti_pozione, domande_pozione + 1, score

        # se l'ingrediente non è corretto, richiamo questo metodo e metto aiuto=True
        else:
            wrong_ingredient()
            write_answer(risposta, '- è SBAGLIATA -> aiuto')

            return ask_question(pozione, domande_fatte, ingredienti_pozione, ingredienti_indovinati, difficolta,
                                domande_pozione, True)



'''
    Funzioni Utility --> Metodi supplementari
'''

def loading():
    for i in range(1, 4):
        print(".", end='')
        sleep(0.3)
    print(".", end='\r')
    sleep(0.1)

def getTime():
    return int(datetime.now().strftime("%H"))

# Metodo per creare l'immagine del parsing
def displayParser(frase):
    svg = displacy.render(frase, style="dep")
    output_path = Path("result_spacy.svg")
    output_path.open("w", encoding="utf-8").write(svg)

def checkScream(frase):
    if frase.isupper():
        print("\nDon't scream!\n")
        sleep(2)
def checkQuestion(frase):
    if "?" in frase:
        print("I'm asking the questions, not you!\n")
        sleep(2)

def checkFrase(frase):
    checkScream(frase)
    checkQuestion(frase)