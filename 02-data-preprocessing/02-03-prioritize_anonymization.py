# -*- coding: utf-8 -*-
import os
import pandas as pd
from pprint import pprint

folder_w_anonym = "PATH TO THE FOLDER WE WANT TO LINK WITH THE METADATA"
#df = pd.read_excel('/Users/philippeprince/Downloads/Conceptos jurídicos MetaDrive.xlsx')
df = pd.read_csv('METADRIVE DATA.csv', encoding='utf8')
anonimizado = []
list_json = []
list_final_json = []

for root, dirs, files in os.walk(folder_w_anonym):
        for file in files:
            if file.endswith(".json"):
                file_json = str(os.path.join(root, file)).upper()
                list_json.append(file_json)

for x in list_json:
    x = str(x).replace("Ó","O").replace("Í", "I").replace("Á", "A").replace("Ñ", "N")
    list_final_json.append(x)
print(list_final_json)


for index, row in df.iterrows():
    file_from_list = str(row['Folder']).replace("/"," ") + "/" + str(row['Name'])[:-4]
    anonimizado.append("NO")
    for x in list_final_json:
        if file_from_list.upper() in str(x).upper():
            anonimizado[-1]="SI"
    # for root, dirs, files in os.walk(folder_w_anonym):
    #     for file in files:
    #         if file.endswith(".json"):
    #             file_json = str(os.path.join(root, file))
    #             if file_from_list.upper() in file_json.upper():
    #                 anonimizado[-1]="SI"
    #                 continue
    #             else:
    #                 print(file_from_list.upper())

#print(anonimizado)                   
df['Anonimizado'] = anonimizado
df.to_excel('TARGET FILES DATA WITH METADATA.xlsx')