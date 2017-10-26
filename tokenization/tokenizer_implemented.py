import re
import pickle


with open('tokenization/programming_languages.txt', 'r') as file:
    langs = file.read().split()

with open('tokenization/text_emoticons.txt', 'r') as file:
    emoticons = file.read().split()


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
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in space_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(<code>.*?<\/code>)')
def code_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in code_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})')
def url_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in url_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(\W)')
def non_alphanum_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in non_alphanum_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'([a-z][a-z0-9_]*(\.[a-z0-9_]+)+[0-9a-z_])')
def package_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in package_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'((.*)?(\/[^/\n ]*)+\/?\n?)')
def filepath_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in filepath_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(([+|-]?\d+)?\.\d+)')
def decimal_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in decimal_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(\S+\'\S+)')
def constraction_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in constraction_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'([a-zA-z]\.([a-zA-z]\.)+)')
def abbreviation_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in abbreviation_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(\.\.\.|->|[(){}\[\],])')
def new_extra_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in new_extra_tokenizer.split(sentence) if token]
    else:
        return [sentence]

@_matches(r'(^\w+[\/]\w+$)')
def eitheror_tokenizer(sentence):
    if not re.match(r'.*(__FT__).*', sentence):
        return [token for token in eitheror_tokenizer.split(sentence) if token]
    else:
        return [sentence]


def mark_tokens(tokens, filter):
    return ["__FT__" + token if filter(token) and "__FT__" not in token else token for token in tokens]


def handle_clitics(token):
    tokens = []
    if token[-1].lower() == 's' and token[-2] in ["'"]:
        tokens.append(token[:-2])
        tokens.append(token[-2:])
    else:
        idx=0
        sub_tokens = [token]
        length = len(token)
        if length > 1:
            for pos in range(length - 1, 0, -1):
                if token[pos] in ["'"]:
                    if 2 < length and pos + 2 == length and token[-1] == 't' and token[pos - 1] == 'n':
                        pos -= 1
                    sub_tokens.insert(idx, token[:pos])
                    idx += 1
                    sub_tokens[idx] = token[pos:]
        tokens.extend(sub_tokens)
    return tokens


def simple_tokenizer(text):

    code_tokenized = code_tokenizer(text)

    space_tokenized = []
    for token in code_tokenized:
        if not code_tokenizer.match(token):
            space_tokenized_token = space_tokenizer(token)
            space_tokenized.extend(space_tokenized_token)
        else:
            space_tokenized.append(token)

    emoticon_and_lang_marked_tokens = mark_tokens(space_tokenized, lambda token : token.lower() in emoticons or token.lower() in langs or code_tokenizer.match(token) is not None)

    new_extra_tokenized = []
    for token in emoticon_and_lang_marked_tokens:
        new_extra_tokenized.extend(new_extra_tokenizer(token))

    emoticon_and_lang_marked_tokens = mark_tokens(new_extra_tokenized, lambda token : token.lower() in emoticons or token.lower() in langs or code_tokenizer.match(token) is not None)

    constraction_tokenized = []
    for token in emoticon_and_lang_marked_tokens:
        if constraction_tokenizer.match(token) is not None:
            constraction_tokenized.extend(["__FT__" + sub_token for sub_token in handle_clitics(token)])
        else:
            constraction_tokenized.append(token)

    def to_be_filtered(sub_token):
        checklist = [
            new_extra_tokenizer.match(sub_token) is None,
            abbreviation_tokenizer.match(sub_token) is None,
            decimal_tokenizer.match(sub_token) is None,
            url_tokenizer.match(sub_token) is None,
            package_tokenizer.match(sub_token) is None,
            filepath_tokenizer.match(sub_token) is None
        ]
        return False in checklist

    filter_marked_tokens = mark_tokens(constraction_tokenized, to_be_filtered)

    non_alphanum_tokenized = []
    for token in filter_marked_tokens:
        non_alphanum_tokenized.extend(non_alphanum_tokenizer(token))

    eitheror_tokenized = []
    for token in non_alphanum_tokenized:
        if eitheror_tokenizer.match(token) is not None:
            eitheror_tokenized.extend([token.split('/')[0], '/', token.split('/')[1]])
        else:
            eitheror_tokenized.append(token)

    clean_tokens = []
    for token in eitheror_tokenized:
        clean_tokens.append(token.replace("__FT__", ""))

    for token in clean_tokens:
        yield token


def tokenize():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    f = open('tokenization/tokenized_data.txt', 'w+')
    # posts = posts[:100]
    post_no = 1
    for post in posts:
        f.write('POST {}\n\n'.format(post_no))
        f.write('{}\n\n'.format(post))
        f.write('{}\n\n'.format('-' * 72))

        tokens = []
        for token in simple_tokenizer(post):
            if token:
                tokens.append(token)

        f.write('[{}]\n\n'.format(', '.join(('"' + token + '"' for token in tokens))))
        f.write('{}\n\n\n\n'.format('=' * 72))

        post_no += 1


def main():
    tokenize()


if __name__ == '__main__':
    main()
