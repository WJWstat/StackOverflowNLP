# NLP for Stack Overflow Posts

This repository contains the source code used to perform basic NLP tasks on posts extracted from Stack Overflow.

## Setup

This project is entirely written in Python 3 and depends on the packages listed in `requirements.txt`. In order to setup your development environment, please simply run:

```
$ pip install -r requirements.txt
```

You can also find a list of complete dependencies at the end of this document.

## How To Run?

### Dataset Collection

The first step is to download the Stack Overflow data dump (i.e. `stackoverflow.com-Posts.7z`) from [here](https://archive.org/details/stackexchange) and uncompress the file. Set the filepath to the uncompressed `Posts.xml` file in `dataset_collection/retrieve_threads.py` and run the following:

```
$ python dataset_collection/retrieve_threads.py
$ python dataset_collection/thread_stats.py
$ python dataset_collection/extract_clean_posts.py
$ python dataset_collection/post_stats.py
```

Alternatively, you can use the 500 extracted threads available in `pickles/threads.pkl` and sanitized posts in `pickles/posts.pkl`. These files are what the rest of the project uses and will be created if you run the above scripts.

### Dataset Analysis

To find the most frequent words & stems in the dataset, run:

```
$ python data_analysis/stemming.py
```

To run POS tagging on the first 10 sentences of the dataset, run:

```
$ python data_analysis/pos_tagging.py
```

### Tokenization

Since off-the-shelf tokenizers are not robust enough to handle tokens that are specific to a particular subject (in this case, computer programming), we built our own tokenizer.

The token definition can be found in `tokenization/annotation/token_definition.txt`. Based on this token definition, a ground truth is established for the first 100 posts in `tokenization/annotation/ground_truth.txt`, which will be used to benchmark the performance of our custom tokenizer. This ground truth is created by running a preliminary tokenizer (`tokenization/annotation/preliminary_tokenizer.py`) and manually correcting the tokenization, if needed.

The actual custom tokenizer is implemented in `tokenization/custom_tokenizer/tokenizer.py`.

### Further Analysis

Further analysis is performed by investigating irregular tokens (i.e. non-English words) using the custom tokenizer in `tokenization/custom_tokenizer/further_analysis.py`.
### Application: Detecting duplicate questions and computing question similarity

Our application computes question similarity by using a weighted ensemble of wordnet synonym distance, word vector distance and word mover's distance. 
We obtain stack exchange specific word vectors from https://github.com/taolei87/askubuntu, and further pruned it (to save memory) by only including word vectors for words in our corpus' vocabulary.

Our application's source code is located in `application/application.py`.

To use the application with terminal interface, run:

```
$ python application/application.py
```

Upon running, either press 1 to enter a question to find potential duplicates for, or press -1 to exit the program. 
Depending on the underlying processor, finding duplicate questions may take a time range of 10s to 1min. 

## Dependencies

- NLTK v3.2.5 (http://www.nltk.org/)
- Matplotlib v2.1.0 (https://matplotlib.org/)
- PyEnchant v1.6.11 (http://pythonhosted.org/pyenchant/)
- Gensim v3.0.1 (https://radimrehurek.com/gensim/) 
- scipy v0.18.1 (https://www.scipy.org/)
- pyemd v0.4.4 (https://github.com/wmayner/pyemd) 

> Please note that these Python packages may depend on other Python packages, so it is advised to simply use the `pip` command described in **Setup** above.
