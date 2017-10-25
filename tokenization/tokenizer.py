import re
import pickle
from segtok.segmenter import split_multi
from segtok.tokenizer import split_contractions, web_tokenizer, word_tokenizer, space_tokenizer
from nose.tools import assert_equal

def tokenize():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    f = open('tokenization/tokenized_data.txt', 'w+')

    posts = posts[:100]
    post_no = 1
    for post in posts:
        f.write('POST {}\n\n'.format(post_no))
        f.write('{}\n\n'.format(post))
        f.write('{}\n\n'.format('-' * 72))

        tokens = []
        for token in SimpleTokenizer(post):
            if token:
                tokens.append(token)

        f.write('[{}]\n\n'.format(', '.join(('"' + token + '"' for token in tokens))))
        f.write('{}\n\n\n\n'.format('=' * 72))

        post_no += 1

def SimpleTokenizer(text):
    for sentence in split_multi(text):
        for token in split_contractions(space_tokenizer(sentence)):
            yield token
        yield None  # None to signal sentence terminals

def main():
    test = TestTokenizer()
    test.Test_Against_GTruth()

class TestTokenizer(object):

    def Test_Against_GTruth(self):
        tokenize()
        with open('tokenization/ground_truth.txt', 'r') as file:
            ground_truth = file.readlines()
        
        with open('tokenization/tokenized_data.txt', 'r') as file:
            tokenized_data = file.readlines()
        
        for result, actual in zip(tokenized_data, ground_truth):
            assert_equal(result, actual)
        
        print('Success...')


if __name__ == '__main__':
    main()