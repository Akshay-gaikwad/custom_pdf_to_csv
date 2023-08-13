from random import randint

import pandas as pd
import pdfplumber

if __name__ == "__main__":
    input_file = "ONe words Substitution - 2_249341.pdf"
    # input_file = "Vocab Test - 3_254709.pdf"
    # input_file = "Vocabulary_(Synonyms_and_Antonyms)_-_Study_Notes.pdf"
    # input_file = "Idioms_and_Phrases_-_Study_Notes.pdf"
    # input_file = "Phrasal_Verbs_-_Study_Notes.pdf"

    output_file = f"{input_file.lower().rstrip('.pdf')}.csv"
    final_data = []
    columns = []
    pre_col = []
    multi_table = False
    previous_col_list = ['Made of', 'Made up of', 'Phrasal Verbs', 'Usage', 'Example']

    with pdfplumber.open(input_file) as pdf:
        for page in pdf.pages:
            main_tables_data = page.extract_table()
            if main_tables_data:
                for row in main_tables_data:
                    # print(row)
                    if not columns:
                        # pdf wise column name setting
                        if len(row) == 2 and "One Word Substitution" in row[0]:
                            columns = ["One Word Substitution", "Phrases"]

                        elif len(row) == 4 and "Hindi Meaning 1600 List" in row[1]:
                            columns = ['Present', 'Hindi Meaning 1600 List of Verb in hindi क्रिया', 'Past',
                                       'Past Participle']

                        elif len(row) == 5 and "Word" in row[0]:
                            columns = ['Word', 'Meaning', 'Synonym', 'Antonym', 'Sentence']

                        elif len(row) == 3 and "Idiom / Phrase" in row[0]:
                            columns = ['Idiom / Phrase', 'Meaning', 'Example Sentence']

                        else:
                            # special case: for multiple tables with different column size in pdf
                            columns = [i for i in row]
                            multi_table = True

                    if row and columns and row[0] is not None and str(row[0]) not in columns[0] and str(row[1]) not in columns[1]:
                        final_data.append(row)

                else:
                    # special case: for multiple tables with different column size in pdf
                    if multi_table:
                        if not any([True if p in previous_col_list else False for p in columns]):
                            columns = pre_col
                        else:
                            pre_col = columns

                        print(df)
                        df = pd.DataFrame(final_data, columns=columns or pre_col)
                        final_data = []
                        columns = []
                        df.to_csv(f'multitable{randint(0,100)}_{output_file}', index=False, encoding="utf-8")
                        df.to_csv()

        if final_data and not multi_table:
            df = pd.DataFrame(final_data, columns=columns)
            print(df)
            # Save DataFrame to CSV file
            df.to_csv(output_file, index=False, encoding="utf-8")
            df.to_csv()
