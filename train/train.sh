#!/bin/bash

set -e

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

echo The experiment is starting.
echo Input data:${EXP_DIR}/training_data.t7
echo Output Model: ${EXP_DIR}/model.*
echo Progress is in  ${EXP_DIR}/training.progress.txt

cd ${OPENNMT};th train.lua -gpuid ${GPUID} -brnn_merge concat -dropout 0 -optim adam -learning_rate 0.0002 -enc_layers 1 -dec_layers 1 -encoder_type brnn -src_word_vec_size 500 -tgt_word_vec_size 500 -rnn_size 500 -data ${EXP_DIR}/input-train.t7 -save_model ${EXP_DIR}/model  > ${EXP_DIR}/training.progress.txt

echo Training finished.
cd ${EXP_DIR}

