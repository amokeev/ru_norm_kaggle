from functions import *
import glob
import sys
import os
import numpy as np
from validation_ids import validation_ids


def save_data(file_name, data):
    res_out = open(file_name, "w+", encoding='utf-8')
    res_out.write("\n".join(data))
    res_out.close()

if __name__ == "__main__":

    num_validation = 10000
    datasets_dir = "./datasets"
    target_dir="./"
    np.random.seed(1234)

    if len(sys.argv) == 4:
        num_validation = int(sys.argv[1])
        datasets_dir = sys.argv[2]
        target_dir = sys.argv[3]
    else:
        if len(sys.argv) != 1:
            print("Usage: datasets2data.py num_validation_examples datasets_dir target_dir")
            exit(-1)

    train_src_file = os.path.join(target_dir, "train.src.txt")
    train_tgt_file = os.path.join(target_dir, "train.tgt.txt")
    validation_src_file = os.path.join(target_dir, "validation.src.txt")
    validation_tgt_file = os.path.join(target_dir, "validation.tgt.txt")


    csv_datasets = glob.glob("%s/*.csv"%datasets_dir)

    src_datasets = glob.glob("%s/*.src.txt"%datasets_dir)
    tgt_datasets = [f.replace(".src.txt", ".tgt.txt") for f in src_datasets]

    print("== Merging the below lists for CSV/TXT_SRC/TXT_TGT into single train/validation data.==")
    print(csv_datasets)
    print(src_datasets)
    print(tgt_datasets)

    tmp_dir = os.path.join(target_dir, "tmp")
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)


    src_files = []

    #Transform CSVs into src/tgt pairs of text sentences
    for ds in  csv_datasets:
        data_file = ds
        tmppath = os.path.join(tmp_dir, os.path.basename(ds))
        src_file = tmppath.replace(".csv", ".src.csv")
        tgt_file = tmppath.replace(".csv", ".tgt.csv")
        uris_file = tmppath.replace(".csv", ".uri.csv")


        #This is an interim representation, prior to the tokenization. Check out inputSnt2Tkn to tokenization details.
        src_raw_file = tmppath.replace(".csv", ".src.raw.txt")

        src_txt_file = tmppath.replace(".csv", ".src.txt")
        tgt_txt_file = tmppath.replace(".csv", ".tgt.txt")


        disjoin_source_target(data_file, src_file, tgt_file)
        source_to_sentences(src_file, src_raw_file)
        target_to_sentences(tgt_file, tgt_txt_file)
        sentence_to_words_and_chars(src_raw_file, src_txt_file)
        print("Produced %s and %s"%(os.path.basename(src_txt_file),os.path.basename(tgt_txt_file)))
        src_files.append(src_txt_file)

    #Note: processing of .src.txt and .tgt.txt is removed from this version.

    print("Merging..")
    print(src_files)

    examples_src=[]
    examples_tgt=[]

    for src_item in src_files:
        tgt_item = src_item.replace(".src.txt",".tgt.txt")
        examples_src = examples_src + open(src_item, "r+", encoding='utf-8').read().splitlines()
        examples_tgt = examples_tgt + open(tgt_item, "r+", encoding='utf-8').read().splitlines()


    print("Splitting..")


    #validation_idxs = np.random.randint(low=0, high=len(examples_src), size=num_validation).tolist()
    #Instead of random generation, we read the ids from hardcoded list.
    validation_idxs = [idx-1 for idx in validation_ids]

    validation_src = [examples_src[idx] for idx in validation_idxs]
    validation_tgt = [examples_tgt[idx] for idx in validation_idxs]

    #These are commented out for the final model
    #train_src = [examples_src[idx] for idx in range(len(examples_src)) if idx not in validation_idxs]
    #train_tgt = [examples_tgt[idx] for idx in range(len(examples_src)) if idx not in validation_idxs]

    #We know that model converges and want to use everything for training. Uncomment the above otherwise


    train_src = examples_src
    train_tgt = examples_tgt



    print("Size %d"%len(train_src))

    save_data(validation_src_file, validation_src)
    save_data(validation_tgt_file, validation_tgt)
    save_data(train_src_file, train_src)
    save_data(train_tgt_file, train_tgt)
