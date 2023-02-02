import pandas as pd
import chardet
import json
import os
from collections import Counter
import pathlib
import re

CUR_PATH = os.path.dirname(__file__)
df = pd.read_csv(os.path.join(CUR_PATH, "LLITRA_Visualization.csv"), encoding = 'latin-1')

for root, dirs, files in os.walk(CUR_PATH):
    for file in files:
        if file.endswith(".json"):
            concepts_list = []
            file = os.path.join(root, file)

            enc = chardet.detect(open(file,'rb').read())['encoding']
            with open(file,'r', encoding = enc) as f:
                line_json = json.load(f)["samples"]
                f.close()

            for x in line_json:
                print(x)
                
                annoted = x.get("brush")
                if annoted == "complete":
                    for y in x["annotation"]["entities"]:
                        
                        try:
                            concepts_list.append(y["label"])
                        except:
                            pass

            concepts_list = dict(Counter(concepts_list))
            concepts_list["DOC_NAME"] = os.path.basename(file).replace(".udt","").replace(".json","")
            #doc_dir = str(pathlib.Path(file).parent.absolute())
            doc_dir = os.path.dirname(file)
            concepts_list["DOC_DIR"] = re.sub('.*/', '', doc_dir)


            df = df.append(concepts_list, ignore_index=True)
df.to_csv("parameters.csv")