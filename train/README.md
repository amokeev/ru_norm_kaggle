## REQUIREMENTS:

1. [Torch](http://torch.ch/docs/getting-started.html). The hardcoded location is used: ~/torch
2. [OpenNMT](https://github.com/OpenNMT/OpenNMT). Follow its README for the installation spec. The training logic expects OPENNMT environment variable to be set and pointiung to OpenNMT installation location.
3. Python 3.5 pre-installed

All the steps were verified on Ubuntu 16.04 LTS. Torch version: master branch, Git hash 20e523, OpenNMT: master branch, Git has f3a9343.


## STEPS:

1. Place competitions's original *ru_train.csv* file into *datasets* folder
2. export *OPENNMT* environment variable, pointing to local OpenNMT installation
3. Initiate data tokenization and preparation by running ./preprocess.sh

  * Preprocessing defines following important parameters:
    * sequence length is set to 200 for source and target sentences
    * two separate vocabularies are used for input and output
    * Size of the vocabularies is set to 25000 words.
  * Preprocessing may take 5-10 minutes to run.
  * Once preprocessing is complete, you can check out *train.src.txt*, *train.tgt.txt*, *validation.src.txt*, *validation.tgt.txt*. These are tokenized left and right parts of the training dataset. 

*NOTE:* 
  * For the purpose of this project, the validation set uses hardcoded sentence ids to exactly repeat the winning submission content. You may want to change that.
  * To proceed with training, you need only input-train.t7, input.src.dict, input.tgt.dict so you can remove all other generated files.

4. Start model training by executing ./train.sh
Training uses following important parameters:
  * sequence length and vocabulary sizes were defined during preprocessing.
  * hidden layer sizes for encoder and decoder: 500
  * number of layers in encoder and decoder : 1
  * embeddings size: 500
  * optimization: ADAM, with initial LR 0.0002
  * Learning rate decay of 0.7 at every epoch after epoch 9
  * no regularization of any kind.

the training runs for 13 epochs and finish. Once finished, we need to copy model_epoch13_1.00.t7 as model.t7 into the translation project directory. Note: 1.00 is perplexity value. It must be 1.00 given the above steps.