from functions import *
from names import *
import sys

# This file is used to take input in CSV format and prepare it for translation.
# Place ru_test.csv as input.csv into experiment's dir prior to executing this.

if __name__ == "__main__":

    if len(sys.argv) != 1:
        print("Usage: text2translation.py")
        exit(-1)

    competition_input_to_sentences(input_csv, tmp1_txt)
    input_snt_to_tkn(tmp1_txt, input_txt)



