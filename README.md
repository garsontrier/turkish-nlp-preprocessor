# turkish-nlp-preprocessor

This project was implemented in December 2020 as an assignment for Natural Language Processing Course in Bogazici University.
This a two person project: Mansur Yeşilbursa and Güray Baydur

This is a basic text preprocessing tool for Turkish. It includes the following functionalities with different methods:
1) Tokenization
    * Rule based tokenization
    * Logistic Regression based tokenization
2) Sentence Boundary Detection
    * Rule based sentence splitting
    * Logistic Regression based sentence splitting 
3) Stemming
    * Greedy matching
    * Suffix checking
4) Normalization
    - Normalization steps
      - Letter case transformation
      - Accent normalization
      - Deascification
      - Spelling error correction
5) Stopword Removal
    * Static stopword removal
    * Dynamic stopword removal

There already available text processing tools for Turkish and this project doesn't claim to outperform any other toolbox.
It is implemented solely for educational purposes. 

A detailed report about the implementation and the methodology can be read at [here](https://docs.google.com/document/d/1JIIki6IpFYcaYSIHpJ4qsKuXGmspikYfwMoJbbsNmYA/edit?usp=sharing)

Python 3.6
# Required Libraries
* matplotlib
* numpy
* scikit-learn
* conllu



There are many auxilary files accompanying the source code. The program highly relies on those files as they include various data extracted from the datasets.
There is a missing auxilary file that couldn't be uploaded to this repository due to size concerns, but it will be generated once normalization applied. Execution may take long  to finish as the program generates a corpus for spelling correction. But it is necessary since there is no publicly available spelling correction datasets for Turkish.

3 different datasets were used in the project. A subset of these datasets can be found in the dataset folder. '42 bin haber' dataset is not available but it is not required for program to run as long as auxilary files are present.
