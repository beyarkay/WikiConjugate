import re

import wikipedia as w
from wikipedia import WikipediaPage

CONJUGATION_FORMS = [
    "preterite",
    "present",
    "imperative"
]


def main():
    with open("WikiConjugate/wikipages.txt", "r") as textfile:
        pages = textfile.readlines()

    for page in pages[:3]:
        try:
            wiki = w.page(page)
            print("{}: {}".format(wiki.title, wiki.url))
            make_exercises_of(wiki)
        except KeyError as e:
            print("There was a KeyError: " + str(e))

    # make_exercises_of(w.page("Nueva York"))


def get_conjugations(verb, form):
    if form == CONJUGATION_FORMS[0]:
        ar_conj = ["ar", "é", "aste", "ó", "amos", "asteis", "aron"]
        er_conj = ["er", "í", "iste", "ió", "imos", "isteis", "ieron"]
        ir_conj = ["ir", "í", "iste", "ió", "imos", "isteis", "ieron"]

    elif form == CONJUGATION_FORMS[1]:
        ar_conj = ["ar", "o", "as", "a", "amos", "áis", "an"]
        er_conj = ["er", "o", "es", "e", "emos", "éis", "en"]
        ir_conj = ["ir", "o", "es", "e", "imos", "ís", "en"]

    elif form == CONJUGATION_FORMS[2]:
        ar_conj = ["ar", "_", "a", "e", "emos", "ad", "en"]
        er_conj = ["er", "_", "e", "a", "amos", "ed", "an"]
        ir_conj = ["ir", "_", "e", "a", "amos", "id", "an"]
    else:
        raise ValueError("form '" + form + "' is not in CONJUGATION_FORMS=" + str(CONJUGATION_FORMS))

    if verb[-2:] == "ar":
        return [verb[:-2] + conj for conj in ar_conj]
    elif verb[-2:] == "er":
        return [verb[:-2] + conj for conj in er_conj]
    elif verb[-2:] == "ir":
        return [verb[:-2] + conj for conj in ir_conj]
    else:
        raise ValueError("Verb '" + verb + "' is not formatted properly")


def make_exercises_of(wikipage: WikipediaPage, buffer=50):
    w.set_lang("es")
    text = wikipage.content.replace("\n", " ")
    with open("WikiConjugate/regular_verbs.txt", "r") as textfile:
        infinitives = textfile.readlines()
    verbs = [get_conjugations(verb.strip(), CONJUGATION_FORMS[0]) for verb in infinitives]

    # verbs = [conj for sublist in verbs for conj in sublist]
    for conjugations in verbs:
        for conjugation in conjugations[1:]:
            match = re.search(r"\W" + conjugation + r"\W", text)
            if match:
                start = max(0, match.start() - buffer)
                end = min(len(text), match.start() + buffer)

                print("\t{} ({}) ____ {}\t\t\t\t{}".format(
                    text[start:match.start()].strip(),
                    conjugations[0],
                    text[match.end():end].strip(),
                    conjugation))


if __name__ == '__main__':
    main()
