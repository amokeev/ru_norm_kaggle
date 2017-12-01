#!/bin/bash

set -e

#Once the input is prepared, execute this file to do the actual translation. It will take 1-2 hours on single Tesla GPU
#To make it in 10-20 minutes, consider multi-GPU options.

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

echo The experiment is starting. Please monitor ${EXP_DIR}/translated.output.txt for progress.

cd ${OPENNMT};th translate.lua -batch_size 32 -gpuid ${GPUID} -src ${EXP_DIR}/input.prepared.txt -output ${EXP_DIR}/translated.txt -model ${EXP_DIR}/model.t7 > ${EXP_DIR}/translated.output.txt

echo Finished.
cd ${EXP_DIR}

