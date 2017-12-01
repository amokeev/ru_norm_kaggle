import pandas as pd
import re
from collections import OrderedDict
import time

#This file has various helper functions. Checkout README for the flow.

def helper_input_snt_to_tkn(snt):
    step1 = []
    for token in snt.split(' '):
        handled = False
        if '-' in token:
            subkns = token.split('-')
            for i in range(0,len(subkns) - 1):
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


def input_snt_to_tkn(in_file, resulting_in_file):
    inData = open(in_file, "r+", encoding='utf-8').readlines()
    outData = []

    for snt in inData:
        newSnt = []
        for token in helper_input_snt_to_tkn(snt):
            if not re.match("\<T[0-9]*\>", token) and not re.match("\</T[0-9]*\>", token) and \
                re.match("^[A-Za-z0-9+-г\./]*$", token) or re.match("^[A-Za-z#0+-9½¼¾⅛⅔⅓_—\-\,\.\$¥€£\:\%\(\)\\\/]*$",
                                                                 token) or re.match("^[А-Я]*$",token) or \
                    (re.match("^[А-Яа-я]*$", token) and (sum(1 for c in token if c.isupper()) > 2)) or \
                    re.match("^[А-Я]\.[А-Я]\.$", token) or re.match("^[А-Я]\.[А-Я]\.[А-Я]\.$", token):
                newSnt = newSnt + list(token)
            else:
                newSnt = newSnt + [token]
        outData.append(" ".join(newSnt))
    res_out = open(resulting_in_file, "w+", encoding='utf-8')
    res_out.writelines(outData)
    res_out.close()


def service_match_tokens(sentence, source_tokens):
    translated_tokens = {}
    for tid in source_tokens.keys():
        m = re.search('<T%d> (.+?) </T%d>'%(tid,tid), sentence)
        if m:
            token = m.group(1)
            translated_tokens[tid] = token
        else:
            translated_tokens[tid] = source_tokens[tid]

    if (len(translated_tokens) != len(source_tokens)):
        print("Consistency issue %d vs. %d: %s"%(len(translated_tokens), len(source_tokens), sentence))

    return translated_tokens

#NOTE: this doesn't do any work, since we chnaged the format.
def eliminate_unks(org, enc, trn):
    if len(org) != len(trn) or len(trn) != len(enc):
        print(
            "Error: Provided file sizes(%d,%d,%d) are not equal. Check the parameters" % (len(org), len(enc), len(trn)))
        exit(-1)
    for i in range(len(org)):
        org_tokens = org[i].split(" ")
        enc_tokens = enc[i].split(" ")
        trn_tokens = trn[i].split(" ")

        unks = []
        for j in range(len(enc_tokens)):
            if enc_tokens[j] == "<unk>":
                unks.append(org_tokens[j])
        #print(unks)
        upointer = 0
        for j in range(len(trn_tokens)):
            if trn_tokens[j] == "<unk>":
                if upointer < len(unks):
                    trn_tokens[j] = unks[upointer]
                else:
                    trn_tokens[j] = "" #""<unk %d>"%upointer #Ignore unmatched unks
                upointer += 1

        trn[i] = " ".join(trn_tokens)
    return trn


def restore_from_translation(original_in_file, token_in_file, encoded_in_file, translation_file, output_file):
    token_in = open(token_in_file, "r+", encoding='utf-8').read().splitlines()
    encoded_in = open(encoded_in_file, "r+", encoding='utf-8').read().splitlines()
    sentences = open(translation_file, "r+", encoding='utf-8').read().splitlines()

    sentences = eliminate_unks(token_in, encoded_in, sentences)

    original_input = pd.read_csv(original_in_file, encoding='utf-8')

    valid_keys = set()

    src_dataset = {}
    for (sid, tid, before) in original_input[['sentence_id', 'token_id', 'before']].values:
        if (not isinstance(before, str)):
            before = str(before)
        if sid not in src_dataset:
            src_dataset[sid] = {};
        src_dataset[sid][tid] = before
        valid_keys.add("%d_%d"%(sid,tid))

    print("Read original source.")
    count2sid = list(src_dataset.keys())

    result = []
    now = time.time() * 1000
    acc = 0;
    for id, source_tokens in enumerate(src_dataset.values()):
        acc += len(source_tokens)
        matched_tokens = service_match_tokens(sentences[id], source_tokens)
        for tid, token in matched_tokens.items():
            cid = "%s_%s" % (count2sid[id], tid)
            if cid in valid_keys: #Just drop everything that is not in
                result.append([cid, token])
            else:
                print("WARNING: Dropping %s!", cid)
        if id % 10000 == 0:
            print("10000 sentences took %d ms. Acc %d" %((time.time()*1000 - now), acc))
            acc =0;
            now = time.time() * 1000

    out_df = pd.DataFrame(data=result, columns=["id", "after"])
    out_df.to_csv(output_file, encoding='utf-8', index=False)




def competition_input_to_sentences(inFile, resultingInFile):
    # Processing 'in' file first - writing it into sentences.
    inData = pd.read_csv(inFile, encoding='utf-8')
    srcDataset = OrderedDict()
    for (sid, tid, before) in inData[['sentence_id', 'token_id', 'before']].values:
        if (not isinstance(before, str)):
            before = str(before)
        if sid not in srcDataset:
            srcDataset[sid] = [];

        wrap = True

        if wrap: srcDataset[sid].append("<T%d>"%tid)

        for key in before.split(" "):
            srcDataset[sid].append(key)

        if wrap: srcDataset[sid].append("</T%d>"%tid)

    resIn = open(resultingInFile, "w+", encoding='utf-8')
    for snt in srcDataset.values():
        resIn.write("%s\n" % " ".join(snt))
    resIn.close()


def post_process_translation(original_input, translated_csv, out_file, dict_file):
    source_dataset = pd.read_csv(original_input, encoding='utf-8')
    translation = pd.read_csv(translated_csv, encoding='utf-8')

    original_data = {}
    for (sid, tid, before) in source_dataset[['sentence_id', 'token_id', 'before']].values:
        if (not isinstance(before, str)):
            before = str(before)
        if sid not in original_data:
            original_data[sid] = {};
        if tid not in original_data[sid]:
            original_data[sid][tid] = before
        else:
            print("ERROR: In the source %d sid, %d tid is not uniq"%(sid,tid))

    #print(original_data[1183][2])

    translated_data = {}
    for (id, after) in translation[['id', 'after']].values:
        if (not isinstance(after, str)):
            after = str(after)
        sid,tid = id.split('_')
        sid = int(sid)
        tid = int(tid)
        if sid not in translated_data:
            translated_data[sid] = {};
        if tid not in translated_data[sid]:
            translated_data[sid][tid] = after
        else:
            print("ERROR: In transaltion %d sid, %d tid is not uniq" % (sid, tid))
        if tid not in original_data[sid]:
            print("WARNING: we have tid that is not in the source. tid: %d, sid:%d "%(sid,tid))


#Handle multiple consequent unks
    for sid in translated_data.keys():
        extra_for_current_sid = {}
        for tid in translated_data[sid].keys():
            if '<unk>' in translated_data[sid][tid]:
                utokens=translated_data[sid][tid].split(' ')
                for i in range(len(utokens)):
                    if (i == 0) or (tid + i not in translated_data[sid].keys()):
                        extra_for_current_sid[tid + i] = utokens[i]
                    else:
                        print("WARNING: Consistency issue with '<unk>', sid %d, tid %d" % (sid, tid+i))
        for tid, val in extra_for_current_sid.items():
            translated_data[sid][tid] = val

    #End of multiple split

    for sid in translated_data.keys():
        tids_to_remove = []
        for tid in translated_data[sid].keys():
            if translated_data[sid][tid] == '<unk>':
                if tid in original_data[sid].keys() :
                    translated_data[sid][tid] = original_data[sid][tid]
                else:
                    tids_to_remove.append(tid)
        for tid in tids_to_remove:
            translated_data[sid].pop(tid, None)  # remove the token

    dictionary = load_dictionary(dict_file)

    corrected = 0;
    total = 0;
    for sid in original_data.keys():
        for tid in original_data[sid].keys():
            total += 1;
            before = original_data[sid][tid]
            if before in dictionary.keys():
                if tid in translated_data[sid]:
                    after = translated_data[sid][tid]
                else:
                    after = "<dumm>"
                dict_after = dictionary[before]
                if not after == dict_after:
                    print("%s => Correcting \"%s\" to \"%s\""%(before, after, dict_after))
                    translated_data[sid][tid] = dict_after
                    corrected +=1
    print("Corrected %d (%f percent) tokens from training dictionary"%(corrected, 100.0*corrected/total))


    result = []
    for sid in sorted(translated_data.keys()):
        for tid in sorted(translated_data[sid].keys()):
            cid = "%s_%s" % (sid, tid)
            result.append([cid, translated_data[sid][tid]])
    outDF = pd.DataFrame(data=result, columns=["id", "after"])
    outDF.to_csv(out_file, encoding='utf-8', index=False)


def load_dictionary(dictionary_file):
    dictionary={}
    dict_lines = open(dictionary_file, "r+", encoding='utf-8').read().splitlines()
    for line in dict_lines:
        rr = line.split("=",maxsplit=1)
        if len(rr) == 2 and (not re.match(".*[0-9].*", rr[0]) or re.match(".*[0-9][0-9][0-9][0-9][0-9][0-9].*", rr[0] )): # and (rr[0] not in dictionary):
            word, val = rr
            dictionary[word] = val
        #else:
            #print("Ignoring : %s"%rr[0])
    return dictionary

