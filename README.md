# ru_norm_kaggle: Text Normalization Challenge - Russian Language

This is the winning solution to
[Text Normalization Challenge - Russian Language](https://www.kaggle.com/c/text-normalization-challenge-russian-language)


The project is composed of two subprojects: 
* train
* translation

The first is used to train the model.  Its output is a binary model file.
The second is used to apply trained model to the input and do postprocessing.

Please checkout out corresponding READMEs in these projects for details on theirs execution.


## REFERENCE FILES
These files were generated by the projects above. They can be used to jump over a few steps.

The files are in this [folder on Goggle Drive](https://drive.google.com/drive/folders/1QE-U2We2ZYT3GQF4cBvmLfaHOD9su97h?usp=sharing)

* model.t7 - trained model, you can use it to translate
* dictionary.csv - full dictionary, created according to the steps from translation/README
* restored.csv - translation output, w/o any postprocessing. You can use it to verify your training+translation procedure
* restored.pp.csv - postprocessed translation output, equal to the winning submission