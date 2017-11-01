import re
import pickle

# load pickled data
with open('pickles/posts.pkl', 'rb') as f:
    posts = pickle.load(f)

# write preliminary tokenization results to a ground truth file for manual corrections
f = open('tokenization/annotation/ground_truth.txt', 'w+')

# extract 100 posts
posts = posts[:100]
post_no = 1
for post in posts:
    f.write('POST {}\n\n'.format(post_no))
    f.write('{}\n\n'.format(post))
    f.write('{}\n\n'.format('-' * 72))

    # regex rules for preliminary tokenization
    # clitics
    post = re.sub(r'\'s', ' \'s', post)
    post = re.sub(r'\'ve', ' \'ve', post)
    post = re.sub(r'n\'t', ' n\'t', post)
    post = re.sub(r'\'re', ' \'re', post)
    post = re.sub(r'\'d', ' \'d', post)
    post = re.sub(r'\'ll', ' \'ll', post)
    post = re.sub(r'\'m', ' \'m', post)
    # non-alphanumerals
    post = re.sub(r'([^0-9a-zA-Z\'])', r' \1 ', post)
    # code blocks
    post = re.sub(r'<\s*code\s*>', ' <code> ', post)
    post = re.sub(r'<\s*/\s*code\s*>', ' </code> ', post)
    # words separated by spaces
    post = re.sub(r'\s{2,}', ' ', post)

    tokens = []
    code_block = ''
    code_flag = False
    for word in post.split(' '):
        # add code blocks to list of tokens
        if code_flag and word == '</code>':
            code_block += word
            tokens.append(code_block.strip())
            code_block = ''
            code_flag = False
        elif word == '<code>':
            code_block += word
            code_flag = True
        elif code_flag:
            code_block += word
        # if not code block, add the word to list of tokens
        else:
            tokens.append(word.strip())

    # write results to the file
    f.write('[{}]\n\n'.format(', '.join(('"' + token + '"' for token in tokens))))
    f.write('{}\n\n\n\n'.format('=' * 72))

    post_no += 1

f.close()
