import pandas as pd
import sys

def generate_dictionary(src_file, out_dir):
    generate_dictionary_drom_train_data(src_file, out_dir + "/dictionary.csv")


def generate_dictionary_drom_train_data(source_file, dictionary_file):


    train = pd.read_csv(source_file, encoding='utf-8')

    candidates = {} #word:list format initially

    for (sid,tid, before, after) in train[['sentence_id','token_id', 'before', 'after']].values:
        if (not isinstance(before, str)):
            before = str(before)
        if (not isinstance(after, str)):
            after = str(after)

        if before not in candidates.keys():
            candidates[before] = set()

        candidates[before].add(after)


    dict = {}
    #anti_dict = {}
    for word in candidates.keys():
        vals = candidates[word]
        if len(vals) == 1:
            dict[word] = vals.pop()
        #else:
        #    anti_dict[word] = vals

    dict_f = open(dictionary_file, "w+", encoding='utf-8')
    for word, val in dict.items():
        dict_f.write("%s=%s\n"%(word, val))
    dict_f.close()

    #anti_dict_f = open(out_dir + '/anti_dictionary.csv', "w+", encoding='utf-8')
    #for word, val in anti_dict.items():
    #    anti_dict_f.write("%s=" % word)
    #    anti_dict_f.write("|".join(val))
    #    anti_dict_f.write("\n")
    #anti_dict_f.close()

def load_dictionary(dictionary_file):
    dictionary={}
    dict_lines = open(dictionary_file, "r+", encoding='utf-8').read().splitlines()
    for line in dict_lines:
        word, val = line.split("=",maxsplit=1)
        dictionary[word] = val
    return dictionary


if __name__ == "__main__":
    if (len(sys.argv) !=3):
        print("Usage: build_dictionary.py train_file dictionary_file")
        exit(-1)
    else:
        train_file = sys.argv[1]
        dictionary_file = sys.argv[2]

        generate_dictionary_drom_train_data(train_file, dictionary_file)
