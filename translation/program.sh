#!/bin/bash

#This is only used for translation on multiple GPUs. You don't need it otherwise.
echo ARGS are $@
echo Input filename: $1
echo Output filename: $2
echo Stdout file: $3
echo GPU: $4
set -e

GPUID=$4 #default CPU

if [ "${OPENNMT}ABC" == "ABC" ];then
  echo "Please set OPENNMT variable, that points to OPENNMT dir"
  exit -1
fi
export EXP_DIR=`pwd`
echo Translating ${1}
source ~/torch/install/bin/torch-activate

cd ${OPENNMT};th translate.lua -batch_size 32 -gpuid ${GPUID} -src ${1} -output ${2} -model ${EXP_DIR}/model.t7 > ${3}

