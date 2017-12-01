import pandas as pd
import sys

#This script does transformation of the external(GitHub) data into the competition format.

def transform11(in_file, target_file):
    sid = 0
    tid = 0
    output = []
    print("Processing %s " % in_file)
    df = pd.read_csv(in_file, sep="\t", header=None, quoting=3, encoding='utf-8', engine="python")
    total_rows = df.shape[0]
    for source_row in range(total_rows):
        if (df.at[source_row, 0] != "<eos>"):
            # We have to fill
            sentence_id = sid
            token_id = tid
            class_f = df.at[source_row, 0]
            before = df.at[source_row, 1]

            if (df.at[source_row, 2] == "<self>") or (df.at[source_row, 0] == "PUNCT") or (
                            df.at[source_row, 0] == "ELECTRONIC" and df.at[source_row, 2] == "sil") or (
                            df.at[source_row, 0] == "VERBATIM" and df.at[source_row, 2] == "sil"):
                after = df.at[source_row, 1]
            else:
                if (df.at[source_row, 0] == "ELECTRONIC"):
                    after = df.at[source_row, 2].replace("_letter  ", "")
                    after = after.replace("_letter ", " ")
                    after = after.replace("_letter", "")
                    after = after.replace("s l a s h", "slash")
                    after = after.replace("c o l o n", "colon")
                    after = after.replace("c o m dot", "com dot")
                else:
                    after = df.at[source_row, 2]

            tid += 1
        else:
            sid += 1
            tid = 0
        output.append([sentence_id, token_id, class_f, before, after])
    outputDF = pd.DataFrame(data=output, columns=['sentence_id', 'token_id', 'class', 'before', 'after'])
    outputDF.to_csv(target_file, encoding='utf-8', index=False, quoting=0)


def transform(in_file, target_file):
    sid = 0
    tid = 0
    output = []
    print("Processing %s " % in_file)
    df = pd.read_csv(in_file, sep="\t", header=None, quoting=3, encoding='utf-8', engine="python")
    total_rows = df.shape[0]
    for source_row in range(total_rows):
        if (df.at[source_row, 0] != "<eos>"):
            sentence_id = sid
            token_id = tid
            class_f = df.at[source_row, 0]
            before = df.at[source_row, 1]
            if (df.at[source_row, 2] == "<self>") or (df.at[source_row, 0] == "PUNCT") \
                    or (df.at[source_row, 0] == "ELECTRONIC" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "MEASURE" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "CARDINAL" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "DATE" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "TIME" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "DECIMAL" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "ORDINAL" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "MONEY" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "FRACTION" and df.at[source_row, 2] == "sil") \
                    or (df.at[source_row, 0] == "VERBATIM" and df.at[source_row, 2] == "sil"):
                after = df.at[source_row, 1]
            else:
                handled = False
                if (df.at[source_row, 0] == "PLAIN"):
                    after = df.at[source_row, 2].replace("_letter_latin", "_latin")
                    handled = True
                if not handled and (df.at[source_row, 0] == "ELECTRONIC"):
                    after = df.at[source_row, 2].replace("_letter  ", "")
                    after = after.replace("_letter ", " ")
                    after = after.replace("_letter", "")
                    after = after.replace("s l a s h", "slash")
                    after = after.replace("c o l o n", "colon")
                    after = after.replace("c o m dot",
                                                                                                  "com dot")
                    handled = True
                if not handled:
                    after = df.at[source_row, 2]
                    handled = True
            tid += 1
        else:
            sid += 1
            tid = 0
        output.append([sentence_id, token_id, class_f, before, after])
    outputDF = pd.DataFrame(data=output, columns=['sentence_id', 'token_id', 'class', 'before', 'after'])
    outputDF.to_csv(target_file, encoding='utf-8', index=False, quoting=0)



if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Usage: external2competition_ru.py external_file output_file")
        exit(-1)
    else:
        external_file = sys.argv[1]
        output_file = sys.argv[2]
    transform(external_file, output_file)
