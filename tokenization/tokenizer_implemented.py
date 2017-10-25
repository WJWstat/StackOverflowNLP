import re
import pickle

with open('tokenization/programming_languages.txt', 'r') as file:
    langs = file.readlines()
langs = [lang.strip().lower() for lang in langs]

with open('tokenization/text_emoticons.txt', 'r') as file:
    emoticons = file.readlines()
emoticons = [emoticon.strip().lower() for emoticon in emoticons]

def tokenize():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    f = open('tokenization/tokenized_data.txt', 'w+')
        
    posts = posts[:400]
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

@_matches(r'([a-z][a-z0-9_]*(\.[a-z0-9_]+)+[0-9a-z_])')
def package_tokenizer(sentence):
    return [token for token in package_tokenizer.split(sentence) if token]

@_matches(r'([(){}\[\]])')
def bracket_tokenizer(sentence):
    return [token for token in bracket_tokenizer.split(sentence) if token]

def SimpleTokenizer(text):
    for token in code_tokenizer(text):
        if not code_tokenizer.match(token):
            for new_token in space_tokenizer(token):
                if new_token.lower() not in emoticons and new_token.lower() not in langs:
                    for sub_token in bracket_tokenizer(new_token):
                        if url_tokenizer.match(sub_token) is None and package_tokenizer.match(sub_token) is None:
                            for sub_sub_token in non_alphanum_tokenizer(sub_token):
                                yield sub_sub_token
                        else:
                            yield sub_token 
                else:
                    yield new_token
        else:
            yield token
    yield None  # None to signal sentence terminals

def main():
    tokenize()

if __name__ == '__main__':
    main()