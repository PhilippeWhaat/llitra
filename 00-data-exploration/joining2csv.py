import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

CUR_PATH = os.path.dirname(__file__)
CUADER = pd.read_excel(os.path.join(CUR_PATH, "EXPEDIENTES LLITRA - Cuadernos principales.xlsx"))
CUADER_REC = pd.read_excel(os.path.join(CUR_PATH, "EXPEDIENTES LLITRA - Cuadernos recursos.xlsx"))
ANONYMAP = pd.read_csv(os.path.join(CUR_PATH, "parameters.csv"), encoding = 'latin-1')


CUADER = CUADER.append(CUADER_REC)
CUADER.columns = [c.replace(' ', '_') for c in CUADER.columns]
CUADER = CUADER[CUADER.Tipo_de_Juicio.isin(["Divorcio Incausado", "Divorcio Bilateral"])]
print(CUADER.columns)

CUADER = CUADER.reset_index().drop(column
s=['Document_Link',
       'Modified', 'Created', 'Quota', 'Modified_By', 'Last_viewed_by_me',
       'Owner', 'Google_System_Property_ID',
       'Google_System_Property_Permissions',
       'Google_System_Property_Mimetype'])

#ANONYMAP = ANONYMAP.applymap(lambda x: 1 if x == np.nan else 0)

ANONYMAP.to_csv(os.path.join(CUR_PATH, "anonym.csv"))
CUADER.to_csv(os.path.join(CUR_PATH, "cuader.csv"))

CUADER = CUADER.rename(columns={'Name': 'DOC_NAME'})

#print(ANONYMAP.head())
#visual_df = CUADER.join(ANONYMAP, "DOC_NAME")
#visual_df = pd.concat([ANONYMAP, CUADER], join="inner")
visual_df = CUADER.join(ANONYMAP.set_index('DOC_NAME'), on='DOC_NAME')
visual_df.to_csv(os.path.join(CUR_PATH, "visual_df.csv"))