import re
import pickle


def tokenize():
    with open('pickles/posts.pkl', 'rb') as f:
        posts = pickle.load(f)

    f = open('tokenization/ground_truth.txt', 'w+')

    posts = posts[:100]
    post_no = 1
    for post in posts:
        f.write('POST {}\n\n'.format(post_no))
        f.write('{}\n\n'.format(post))
        f.write('{}\n\n'.format('-' * 72))

        post = re.sub(r'\'s', ' \'s', post)
        post = re.sub(r'\'ve', ' \'ve', post)
        post = re.sub(r'n\'t', ' n\'t', post)
        post = re.sub(r'\'re', ' \'re', post)
        post = re.sub(r'\'d', ' \'d', post)
        post = re.sub(r'\'ll', ' \'ll', post)
        post = re.sub(r'\'m', ' \'m', post)
        post = re.sub(r'([^0-9a-zA-Z\'])', r' \1 ', post)
        post = re.sub(r'<\s*code\s*>', ' <code> ', post)
        post = re.sub(r'<\s*/\s*code\s*>', ' </code> ', post)
        post = re.sub(r'\s{2,}', ' ', post)

        tokens = []
        code_block = ''
        code_flag = False
        for word in post.split(' '):
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
            else:
                tokens.append(word.strip())

        f.write('[{}]\n\n'.format(', '.join(('"' + token + '"' for token in tokens))))
        f.write('{}\n\n\n\n'.format('=' * 72))

        post_no += 1

if __name__ == '__main__':
    tokenize()
