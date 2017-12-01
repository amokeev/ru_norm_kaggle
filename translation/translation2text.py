from functions import *
from names import *

#This file have to executed after the translation. It takes the translation and converts it into the competition submision format.


if __name__ == "__main__":

    enc = []
    output = open(translation_output_file, "r+", encoding='utf-8').read().splitlines()

    for line in output:
        m = re.search("^.*SENT\ [0-9]*:\ (.*)", line)
        if m:
            enc.append(m.group(1))

    resOut = open(tmp1_enc, "w+", encoding='utf-8')
    resOut.write("\n".join(enc))
    resOut.close()

    restore_from_translation(input_csv, input_txt,
                             tmp1_enc, translation_file,
                             restored_file)

    #post_process_translation(competitions_input_file, competitions_restored_file, competitions_restored_file_pp)
    #competitionOutputToRawText(restored_file, output_file)




