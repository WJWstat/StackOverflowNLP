"""
StackOverflowNLP 
=====================================================

Run this code with an argument 1, 2, 3, 4 or 5 to run the tasks for Assignment 3.1, 3.2, 3.3, 3.4 or 3.5. The codes are available in the subdirectories and are invoked when run with the argument.

Example: python main.py 1
"""

import sys

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        task = sys.argv[1]
    else:
        print(__doc__)
        sys.exit(0)

    if task == '1':
        subtask = 'retrieve_threads'
        if (len(sys.argv) > 2):
            subtask = sys.argv[2]

        if (subtask == 'retrieve_threads'):
            print('Running Task 1.1 - Retrieve Threads...')
            from dataset_collection.retrieve_threads import retrieve_threads
            retrieve_threads()
        elif (subtask == 'extract_clean_posts'):
            print('Running Task 1.2 - Extract Clean Posts...')
            from dataset_collection.extract_clean_posts import extract_clean_posts
            extract_clean_posts()
    elif task == '2':
        subtask = 'stemming'
        if (len(sys.argv) > 2):
            subtask = sys.argv[2]

        if (subtask == 'stemming'):
            print('Running Task 2.1 - Stemming...')
            from data_analysis.stemming import stem_posts
            stem_posts()
        elif (subtask == 'pos_tagging'):
            print('Running Task 2.2 - POS Tagging...')
            from data_analysis.pos_tagging import pos_tag_sentences
            pos_tag_sentences()
        elif (subtask == 'preliminary_tokenization'):
            print('Running Task 2.3 - Preliminary Tokenization...')
            from data_analysis.preliminary_tokenizer import tokenize
            tokenize()
