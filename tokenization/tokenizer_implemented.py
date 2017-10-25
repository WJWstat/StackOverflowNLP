import re
import pickle

with open('tokenization/programming_languages.txt', 'r') as file:
    langs = file.readlines()
langs = [lang.strip().lower() for lang in langs]
xdef tokenize():
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

def _matches(regex):
    """Regular expression compiling function decorator."""
    def match_decorator(fn):
        automaton = re.compile(regex, 32)
        fn.split = automaton.split
        fn.match = automaton.match
        fn.search = automaton.search
        return fn

    return match_decorator


@_matches(r'\s+')
def space_tokenizer(sentence):
    return [token for token in space_tokenizer.split(sentence) if token]

@_matches(r'(<code>.*?<\/code>)')
def code_tokenizer(sentence):
    return [token.strip() for token in code_tokenizer.split(sentence) if token]

@_matches(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
def url_tokenizer(sentence):
    return [token.strip() for token in url_tokenizer.split(sentence) if token]

@_matches(r'(\W)')
def non_alphanum_tokenizer(sentence):
    return [token for token in non_alphanum_tokenizer.split(sentence) if token]

def SimpleTokenizer(text):
    for token in code_tokenizer(text):
        if not code_tokenizer.match(token):
            for sub_token in space_tokenizer(token):
                if sub_token.lower() not in langs and url_tokenizer.match(sub_token) is None:
                    for sub_sub_token in non_alphanum_tokenizer(sub_token):
                        yield sub_sub_token
                else:
                    yield sub_token 
        else:
            yield token
    yield None  # None to signal sentence terminals

def main():
    tokenize()

if __name__ == '__main__':
    main()