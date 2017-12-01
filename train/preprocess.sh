#!/bin/bash

set -e


#NOTE: To resume training, use something like below
#th train.lua -brnn_merge concat -dropout 0 -optim adam -learning_rate 0.0002 -enc_layers 1 -dec_layers 1 -encoder_type brnn -src_word_vec_size 500 -tgt_word_vec_size 500 -rnn_size 500 -data ~/wd/r2rv8-lua-train.t7 -save_model ~/wd/models/r2rv8-model -train_from ~/wd/r2rv5-model_acc_96.88_ppl_1.29_e2.pt -start_epoch 3

GPUID=1 #default GPU
if [ "${1}" == "cpu" ];then
    GPUID=0;
fi

if [ "${OPENNMT}ABC" == "ABC" ];then
  echo "Please set OPENNMT variable, that points to OPENNMT dir"
  exit -1
fi

EXP_DIR=`pwd`
source ~/torch/install/bin/torch-activate

#Here goes script that reads the data from the current directory and prepares it for training.
python3 datasets2data.py 10000 ${EXP_DIR}/datasets ${EXP_DIR}


#Let's transform input data into OpenNMT Torch format
#This command takes train src and target, validation src and target
echo Transforming data into OpenNMT format and saving to  ${EXP_DIR}/training_data.t7
cd ${OPENNMT};th preprocess.lua -src_seq_length 200 -tgt_seq_length 200 -src_vocab_size 25000 -tgt_vocab_size 25000 -train_src ${EXP_DIR}/train.src.txt -train_tgt ${EXP_DIR}/train.tgt.txt -valid_src ${EXP_DIR}/validation.src.txt -valid_tgt  ${EXP_DIR}/validation.tgt.txt -save_data ${EXP_DIR}/input


