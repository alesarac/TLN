import utilities as util
import simplenlg
from termcolor import colored

"""
Lista di tutti i metodi implementati con la libreria SimpleNLG per stampare le risposte di Piton
"""

# inizializza la frase con la libreria SimpleNLG
def init():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    phrase = simplenlg.SPhraseSpec(nlgFactory)
    return phrase

# Costruisce una frase con solo un attributo
# es. sp.build_phrase("Good morning") --> "Good morning"
def build_phrase(complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setComplement(complemento)
    return realize_output(phrase)

# Costruisce una frase normale completa
# es. sp.build_phrase_complete("I", "be", "Severus Piton")
def build_phrase_complete(soggetto, verbo, complemento):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.FORM, featureValue=simplenlg.ABC)
    phrase.setTense(simplenlg.Tense.PRESENT)

    phrase.setVerb(verbo)
    phrase.setSubject(soggetto)
    phrase.setComplement(complemento)

    return realize_output(phrase)

# Costruisce una frase di tipo interrogativo, usato per chiedere il nome e la casata all'utente
# es. (sp.ask_info("name") --> "What is your name?"
def ask_info(complemento):
    phrase = init()

    phrase.setVerb("be")
    phrase.setObject("your")

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE,
                      featureValue=simplenlg.InterrogativeType.WHAT_SUBJECT)
    phrase.setTense(simplenlg.Tense.PRESENT)
    phrase.setComplement(complemento)

    return realize_output(phrase)

# Costruisce una frase relativa a una mancata o scorretta risposta da parte dell'utente.
# usato per ripetere all'utente di inserire il nome e la casata corretti
# es. sp.no_answer("your", "name") --> "You must tell me your name."
def no_answer(obj, complmentent):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.MODAL, featureValue="must")
    phrase.setVerb("tell")
    phrase.setObject(obj)
    phrase.setSubject("you")
    phrase.setComplement(complmentent)
    phrase.setIndirectObject("me")

    return realize_output(phrase)

# Costruisce una frase di tipo interrogativo con un verbo e un soggetto
# es. sp.verb_subj("study", "you") --> "Did you study?"
def verb_subj(verb, subject):
    phrase = init()

    phrase.setFeature(featureName=simplenlg.Feature.INTERROGATIVE_TYPE, featureValue=simplenlg.InterrogativeType.YES_NO)
    phrase.setTense(simplenlg.Tense.PAST)
    phrase.setVerb(verb)
    phrase.setSubject(subject)

    return realize_output(phrase)


# Costruisce la frase che da inizio all'interrogazione
# "I'll ask you for the ingredients of 3 potions"
def start_exam():
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    np_ingredients.setPlural(True)
    np_ingredients.addModifier("of")
    np_potion = nlgFactory.createNounPhrase("potion")
    np_potion.setPlural(True)
    np_potion.addPreModifier("3")
    proposition = nlgFactory.createClause("I", "ask for", np_ingredients)
    proposition.addComplement(np_potion)
    proposition.setFeature(simplenlg.Feature.TENSE, simplenlg.Tense.FUTURE)

    output = realize_output(proposition)
    return output

# Costruisce una frase di tipo interrogativo su una particolare pozione
# la domanda varia in base a certi scenari (ingrediente iniziale, e finale)
# es. "Let's start with the potion .... what are the ingredients?" (iniziale)
# es. "What is the last ingredient?" (finale)
def printAskPotion(potion, ingredienti_pozione, domande_fatte, domande_pozione):
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)
    '''What is the ingredient'''
    np_potion = nlgFactory.createNounPhrase("the", colored(potion, 'yellow'))
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    proposition = nlgFactory.createClause(np_ingredients, "be")
    proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)
    ingredienti_mancanti = len(ingredienti_pozione)
    if ingredienti_mancanti == 1:
        '''What is the last ingredient?'''
        np_ingredients.addModifier("last")
    else:
        '''What are the ingredients?'''
        np_ingredients.setPlural(True)
        if domande_fatte == 0 and domande_pozione == 0:
            '''Let's start with the potion, + What is the ingredient?'''
            output = realize_output(proposition)
            sentence = "Let's start with the " + colored(potion, 'yellow') + ', ' + output.lower() + "\n"
            util.write_question(sentence)
            return sentence
        else:
            if domande_pozione > 0:
                return printAskIngredient(ingredienti_mancanti)
            else:
                '''What are the ingredients of the potion?'''
                np_potion.setSpecifier("of")
                np_ingredients.addModifier(np_potion)

    sentence = realize_output(proposition) + "\n"
    util.write_question(sentence)
    return sentence

# Costruisce una frase di tipo interrogativo per chiedere gli ingredienti intermedi di una pozione e indicare quanti ne mancano
# es. "What are the other ingredients?"
def printAskIngredient(nIngredient):
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    np_number = nlgFactory.createNounPhrase(str(nIngredient))
    np_ingredients = nlgFactory.createNounPhrase("ingredient")
    np_missing = nlgFactory.createNounPhrase("missing")
    np_ingredients.addPreModifier(np_number)
    proposition = nlgFactory.createClause(np_ingredients, "be", np_missing)
    if nIngredient > 1:
        np_ingredients.setPlural(True)
        proposition.setPlural(True)
        np_missing.setPlural(True)

    np_ingr = nlgFactory.createNounPhrase("ingredient")
    if nIngredient > 1:
        np_ingr.setPlural(True)

    '''What are the other ingredients?'''
    np_ingredients = nlgFactory.createNounPhrase("the", "ingredient")
    np_ingredients.setPlural(True)
    np_ingredients.addModifier("other")
    continue_proposition = nlgFactory.createClause(np_ingredients, "be")
    continue_proposition.setFeature(simplenlg.Feature.INTERROGATIVE_TYPE, simplenlg.InterrogativeType.WHAT_OBJECT)

    sentence = realize_output(proposition) + "\n" + realize_output(continue_proposition) + "\n"
    util.write_question(sentence)
    return sentence

# Costruisce una frase per assegnare un punteggio all'utente dopo l'interrogazione
# es. "I award 5 points to Gryffindor" (punti guadagnati)
# es. "I subtract 5 points to Gryffindor" (punti sottratti)
def printScore(score, casata_nome):
    score = int(score)
    lexicon = simplenlg.Lexicon.getDefaultLexicon()
    nlgFactory = simplenlg.NLGFactory(lexicon)

    np_casata = nlgFactory.createNounPhrase(casata_nome)
    np_casata.addPreModifier("to")
    np_points = nlgFactory.createNounPhrase("point")

    proposition = nlgFactory.createClause("I", "award", np_points)
    proposition.addComplement(np_casata)
    if score < 0:
        score = str(score).strip("-")
        np_points.addPreModifier(str(score))
        proposition = nlgFactory.createClause("I", "subtract", np_points)
        proposition.addComplement(np_casata)
    else:
        np_points.addPreModifier(str(score))

    if int(score) != 1:
        np_points.setPlural(True)

    output = realize_output(proposition)
    return output


# Metodo che stampa la frase costruita in uno dei metodi precedenti
def realize_output(phrase):
    realizer = simplenlg.Realiser()
    output = realizer.realiseSentence(phrase)
    return output