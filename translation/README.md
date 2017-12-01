## REQUIREMENTS:

1. [Torch](http://torch.ch/docs/getting-started.html). The hardcoded location is used: ~/torch
2. [OpenNMT](https://github.com/OpenNMT/OpenNMT). Follow its README for the installation spec. The training logic expects OPENNMT environment variable to be set and pointiung to OpenNMT installation location.
3. Python 3.5 pre-installed
4. Model have to be trained and placed into translation folder as model.t7

All the steps were verified on Ubuntu 16.04 LTS. Torch version: master branch, Git hash 20e523, OpenNMT: master branch, Git has f3a9343.


## DICTIONARY PREPARATION:

All the below actions are done in dicts subdirectory. You need only copy the resulting dictionary.csv to the parent translation dicretory.

1. Generate dictionary from training data:
   `python3 build_dictionary.py <full_path_to_ru_train.csv> dictionary0.csv`
   The train data dictionary is saved to dictionary0.csv
2. Generate dictionary from external data:
   NOTE: You need to have at least 512Gb of RAM and multiple CPUs to run this script.
   `./consume_external.sh`
   The resulting file is RussianExternalDictionary1.csv.gz
   Extract and copy it into `dicts` for future processing.
3. Postprocess this dictionnary by replacing double spaces
   `cat RussianExternalDictionary1.csv|sed s/\ \ /\ /g >RussianExternalDictionary2.csv`
4. Concatenate dictionaries from training data and from external data:
   `cat RussianExternalDictionary2.csv dictionary0.csv >dictionary.csv`
   NOTE: This operation is not 100% correct as it doesn't care about key duplication, but that's what I did at the time.
5. Copy `dictionary.csv` into the translation folder - it will be consumed by translation step 5: postprocess

## TRANSLATION:
1. Copy the `ru_test.csv` as `./input.csv` into the translation dir
2. Preprocess the input by running `python3 ./text2translation.py`
The prepared tokenized sentences are placed into input.prepared.txt

3. Run the translation by executing `./translate.sh`
  * By default translation is started on GPU #1.
  * Use `./translate.sh cpu` to start translation on CPU.
  * Explicit conversion of GPU-based model is required for CPU execution.
  * translate.sh command creates "translated.txt" - this is the normalization (still with tokens and requires postporcessing). Additionally translate.sh creates translated.output.txt, which contains full output from translation and it was used in some of the versions to help with out of the vocabulary words handling. It should not be needed now but is left for compatibility reasons.
(parallel.py, program.sh can be used to do MULTI-GPU translation, but they have to be edited for each particular config and are there for reference only.)

4. Convert translation into competition output forma by executing `python3 translation2text.py`
This command creates restored.csv which is already in competition submission format. Yet, it has to be analysed and postprocessed.

5. Execute postprocessing by `python3 postprocess.py`
This command reads restored.csv and does postprocessing by
  * copying missed out of the vocabulary words/values from the input
  * loading the dictionary and replacing values from it

Simply speaking, the dictionary contains keys, that there were never seen to have two distinct values. So the assumption is that these keys are always normalize to the same value.

