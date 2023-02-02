import os
import docx2txt

FOLDER_PATH = os.path.dirname(__file__)

completeDictionary = ""
for root, dirs, files in os.walk(FOLDER_PATH):
    for file in files:
        if file.endswith("docx"):
            print(os.path.join(FOLDER_PATH, file))
            docToAdd = docx2txt.process(str(os.path.join(FOLDER_PATH, file)))
            completeDictionary = completeDictionary + docToAdd

with open(os.path.join(FOLDER_PATH, "dict_created.txt"), "w", encoding='utf-8') as f:
    f.write(completeDictionary)