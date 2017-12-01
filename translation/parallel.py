import os
import sys
import glob
import time
from multiprocessing import Process
import random
import subprocess
import shlex
from pathlib import Path


#You don't really need this file, unless you are trying to run the translation in parallel


def split_file(num_of_files, input_file):
    f = open(input_file, encoding='utf-8')
    allLines = f.readlines()
    l = len(allLines)
    if (l % num_of_files > 0):
        N = int(l/num_of_files) + 1
    else:
        N = int(l / num_of_files)
    for i in range(num_of_files):
        nlines = allLines[i*N : (i + 1)*N]
        file_split = open(work_dir + "/splitData%s.txt"  % i, 'w', encoding='utf-8')
        for line in nlines:
            file_split.write("%s" % line)

    return l, N

def add_file(current_file, new_file):
    f1 = open(current_file, 'a', encoding='utf-8')
    f = open(new_file, encoding='utf-8')
    new_lines = f.readlines()
    for line in new_lines:
        f1.write("%s" % line)

def sleep_func(f_in, f_out, f_stdout, gpu):
    #print("start_sleep%s" %i)
    subprocess.call(shlex.split('./program.sh %s %s %s %d' %(f_in, f_out, f_stdout, gpu)))


if __name__ == '__main__':
    print("start")

    if (len(sys.argv) < 5):
        print("You should write 5 arguments")
        print("1. name of work directory")
        print("2. name of input file with original text")
        print("3. name of output file with translation text")
        print("4. name of stdout file")
        print("5. number of splitted files")
        exit(-1)

    else:
        work_dir = sys.argv[1]
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        stdout_file = sys.argv[4]
        num_of_files = sys.argv[5]

    files = glob.glob(work_dir + '/*')
    for f in files:
        os.remove(f)

    # N = number of lines in the separated files
    num_of_files = int(num_of_files)
    l, N = split_file(num_of_files, input_file)

    processes = []

    for i in range(num_of_files):
        in_file_path = os.path.normpath(work_dir + "/splitData%s.txt" % i)
        out_file_path = os.path.normpath(work_dir + "/splitDataOut%s.txt" % i)
        stdout_file_path = os.path.normpath(work_dir + "/splitDataStdOut%s.txt" % i)
        p = Process(target = sleep_func, args = (in_file_path, out_file_path, stdout_file_path, (int(i)+1)))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    if Path(output_file).is_file():
        os.remove(output_file)
    if Path(stdout_file).is_file():
        os.remove(stdout_file)

    for i in range(num_of_files):
        add_file(output_file, work_dir + "/splitDataOut%s.txt" % i)
        add_file(stdout_file, work_dir + "/splitDataStdOut%s.txt" % i)


# python3 split_combine5.py "/Users/tasha/Desktop/Kaggle/RusDigital/SplitCombineData" "/Users/tasha/Desktop/Kaggle/RusDigital/text_rus_2translate.txt" "/Users/tasha/Desktop/Kaggle/RusDigital/SplitCombineData/finalData.txt" "/Users/tasha/Desktop/Kaggle/RusDigital/SplitCombineData/stdOutData.txt" 3
