import pandas as pd
import re
from collections import OrderedDict

#
# This file includes functions, used in training procedure. The functions are simple and self-explaining.
# Please use README, that describes the sequence of steps.
#

def helper_sentence_to_tokens(snt):
    step1 = []
    for token in snt.split(' '):
        handled = False
        if '-' in token:
            subkns = token.split('-')
            for i in range(0, len(subkns) - 1):
                step1.append(subkns[i])
                step1.append('-')
            step1.append(subkns[len(subkns) - 1])
            handled = True
        if not handled:
            step1.append(token)
    step2 = []
    for token in step1:
        m = re.search("^([0-9:\.,½¼¾⅛⅔⅓$¥€£]+)([/А-яа-яA-Za-z²³2\"\'\.\,]+)$", token)
        if m:
            num = m.group(1)
            suffix = m.group(2)
            step2.append(num)
            step2.append(suffix)
        else:
            step2.append(token)
    return step2


def sentence_to_words_and_chars(input_file, output_file):
    sentences = open(input_file, "r+", encoding='utf-8').readlines()
    processed_sentences = []

    for snt in sentences:
        new_snt = []
        for token in helper_sentence_to_tokens(snt):
            if not re.match("\<T[0-9]*\>", token) and not re.match("\</T[0-9]*\>", token) and \
                    re.match("^[A-Za-z0-9+-г\./]*$", token) or re.match(
                "^[A-Za-z#0+-9½¼¾⅛⅔⅓_—\-\,\.\$¥€£\:\%\(\)\\\/]*$",
                token) or re.match("^[А-Я]*$", token) or \
                    (re.match("^[А-Яа-я]*$", token) and (sum(1 for c in token if c.isupper()) > 2)) or \
                    re.match("^[А-Я]\.[А-Я]\.$", token) or re.match("^[А-Я]\.[А-Я]\.[А-Я]\.$", token):
                new_snt = new_snt + list(token)
            else:
                new_snt = new_snt + [token]
        processed_sentences.append(" ".join(new_snt))
    res_out = open(output_file, "w+", encoding='utf-8')
    res_out.writelines(processed_sentences)
    res_out.close()


def disjoin_source_target(data_file, src_file, tgt_file):
    data = pd.read_csv(data_file, encoding='utf-8')
    in_df_l = []  # pd.DataFrame(index=False, columns=["sentence_id","token_id","before"])
    out_df_l = []  # pd.DataFrame(index=False, columns=["id","after"])
    for (sid, tid, before, after) in data[['sentence_id', 'token_id', 'before', 'after']].values:
        in_df_l.append([sid, tid, before])
        out_df_l.append(["%s_%s" % (sid, tid), after])

    in_df = pd.DataFrame(data=in_df_l, columns=["sentence_id", "token_id", "before"])
    out_df = pd.DataFrame(data=out_df_l, columns=["id", "after"])
    in_df.to_csv(src_file, encoding='utf-8', index=False)
    out_df.to_csv(tgt_file, encoding='utf-8', index=False)


def source_to_sentences(input_file, output_file):
    # Processing 'in' file first - writing it into sentences.
    source_data = pd.read_csv(input_file, encoding='utf-8')
    sentences_dataset = OrderedDict()
    for (sid, tid, before) in source_data[['sentence_id', 'token_id', 'before']].values:
        if (not isinstance(before, str)):
            before = str(before)
        if sid not in sentences_dataset:
            sentences_dataset[sid] = [];

        wrap = True

        if wrap: sentences_dataset[sid].append("<T%d>" % tid)

        for key in before.split(" "):
            sentences_dataset[sid].append(key)

        if wrap: sentences_dataset[sid].append("</T%d>" % tid)

    out_f = open(output_file, "w+", encoding='utf-8')
    for snt in sentences_dataset.values():
        out_f.write("%s\n" % " ".join(snt))
    out_f.close()


def target_to_sentences(input_file, output_file):
    # Processing 'out' file now - writing it into sentences.
    target_data = pd.read_csv(input_file, encoding='utf-8')
    sentences_dataset = OrderedDict()
    for (id, after) in target_data[['id', 'after']].values:
        sid, tid = id.split('_')
        after = str(after)
        if sid not in sentences_dataset:
            sentences_dataset[sid] = [];

        wrap = True

        if wrap: sentences_dataset[sid].append("<T%s>" % tid)
        sentences_dataset[sid].append(after)
        if wrap: sentences_dataset[sid].append("</T%s>" % tid)

    res_f = open(output_file, "w+", encoding='utf-8')
    for sid, snt in sentences_dataset.items():
        res_f.write("%s\n" % " ".join(snt))
    res_f.close()
