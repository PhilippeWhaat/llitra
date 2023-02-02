from spellchecker import SpellChecker
import os
import re

spell = SpellChecker(language="es", distance=1)
spell.word_frequency.load_words("/Users/philippeprince/Python_Learning_Curve/OCR/textos_ext_dicc/dict_created.txt")
LISTE_PATH = "/Users/philippeprince/Python_Learning_Curve/OCR/DOCUMENTO 10.txt"
CUR_PATH = os.path.dirname(__file__)

completeDoc = open(LISTE_PATH, 'r', encoding='latin-1').read()

completeDocListLines = completeDoc.split("\n")
completeDocListLinesWords = []
for frase in completeDocListLines:
    x = re.search("[A-Z]|[a-z]", frase)
    if frase != "" and x is not None:
        completeDocListLinesWords.append(frase.split(" "))

#print(completeDocListLinesWords)

correctedListLineWord = []
correctedListLine = []
for line in completeDocListLinesWords:
    for mot in line:
        i = spell.correction(mot)
        if i != mot:
            correctedListLineWord.append(i)
        else:
            correctedListLineWord.append(mot)
    correctedListLine.append(correctedListLineWord)
    correctedListLineWord = []

#print("\n\n")
#print(correctedListLine)
finalListCorrected = []
for line in correctedListLine:
    finalListCorrected.append(" ".join(line))

finalListCorrected = "\n".join(finalListCorrected)
#print(finalListCorrected)

with open(os.path.join(CUR_PATH, "DOCUMENTO 10 CORRECTED.txt"), "w", encoding='utf-8') as f:
    f.write(finalListCorrected)
