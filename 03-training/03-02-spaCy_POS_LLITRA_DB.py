import pandas as pd

# importing the dataframe
df = pd.read_csv('HERE GOES THE PATH TO THE DATAFRAME IN CSV', encoding = "UTF-8")

# Define the column you want to keep only letters and numbers
column = 'Word'

# Use the str.replace() method to remove all non-letter and non-number characters
df[column] = df[column].str.replace('[^a-zA-Z0-9]', '')

z = []
for i in df.index:
        if df['Word'][i] == "":
            z.append(i)
        if df['Word'][i] == " ":
            z.append(i)

print(len(z))

df = df.drop(z)

df['Sentence #'] = df['Sentence #'].astype(str)
df['Word'] = df['Word'].astype(str)

# Concatenate the words in each group
df_grouped = df.groupby(['Sentence #']).agg({'Word': ' '.join})

import spacy

# Load the spaCy model
nlp = spacy.load("es_core_news_lg")

# Group the dataframe by Sentence #
df_grouped = df.groupby("Sentence #")["Word"].apply(' '.join).reset_index()

# Iterate over the rows in the grouped dataframe
for index, row in df_grouped.iterrows():
    # Process the sentence with the spaCy model
    doc = nlp(row["Word"])
    # Iterate over the tokens in the sentence
    for token in doc:
        try:
            # Get the index of the corresponding row in the original dataframe
            word_index = df[(df['Sentence #'] == row["Sentence #"]) & (df['Word'].str.strip().str.lower() == token.text.strip().lower())].index.values[0]
            # Add the POS tag to the original dataframe
            df.at[word_index, "POS"] = token.pos_
        except IndexError:
            print(f"Word {token.text} not found in sentence {row['Sentence #']}")

df.to_csv('df_w_POS.csv')